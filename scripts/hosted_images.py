#!/usr/bin/env python3
"""Resolve hosted images by checksum and prepare complete Netlify deployments."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from http.client import HTTPException
from pathlib import Path, PurePosixPath
from urllib.error import URLError
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "assets/image-manifest.json"
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".avif"}
DOWNLOAD_TIMEOUT_SECONDS = 30


def validate_manifest(manifest: dict) -> dict:
    if not isinstance(manifest, dict) or manifest.get("format_version") != 1 or not isinstance(manifest.get("images"), dict):
        raise ValueError("图片清单格式不受支持")
    base_url = manifest.get("base_url", "")
    if not isinstance(base_url, str):
        raise ValueError("图片清单缺少 HTTPS 基础地址")
    parsed = urlsplit(base_url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment or base_url.endswith("/"):
        raise ValueError("图片清单必须使用不含凭据和查询参数的 HTTPS 基础地址")
    for key, record in manifest["images"].items():
        if not isinstance(key, str) or not key or "\\" in key:
            raise ValueError("图片清单包含无效路径")
        path = PurePosixPath(key)
        if path.is_absolute() or ".." in path.parts or str(path) != key or path.suffix.lower() not in IMAGE_SUFFIXES:
            raise ValueError(f"图片清单包含无效路径: {key}")
        if not isinstance(record, dict) or record.get("url") != f"{base_url}/{quote(key, safe='/')}":
            raise ValueError(f"图片地址与清单路径不一致: {key}")
        size = record.get("bytes")
        digest = record.get("sha256")
        if type(size) is not int or size <= 0 or not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError(f"图片清单缺少有效的大小或 SHA-256: {key}")
    return manifest


def load_manifest(path: Path | None = None) -> dict:
    return validate_manifest(json.loads((path or MANIFEST_PATH).read_text(encoding="utf-8")))


def key_for_url(url: str, manifest: dict | None = None) -> str:
    for key, record in (manifest or load_manifest())["images"].items():
        if record["url"] == url:
            return key
    raise ValueError(f"参考图链接未登记: {url}")


def image_record(key: str, manifest: dict | None = None) -> dict:
    records = validate_manifest(manifest or load_manifest())["images"]
    if key not in records:
        raise ValueError(f"图片未登记: {key}")
    return records[key]


def cache_directory() -> Path:
    configured = os.environ.get("HAND_DRAWN_IMAGE_CACHE")
    if configured:
        return Path(configured).expanduser().resolve()
    base = Path(os.environ.get("XDG_CACHE_HOME", str(Path.home() / ".cache"))).expanduser()
    return (base / "hand-drawn/images").resolve()


def cache_path(key: str, record: dict, cache_root: Path | None = None) -> Path:
    root = (cache_root or cache_directory()).resolve()
    target = (root / record["sha256"] / key).resolve()
    if not target.is_relative_to(root):
        raise ValueError(f"图片缓存包含越界路径: {key}")
    return target


def verify_image_bytes(content: bytes, record: dict, key: str) -> None:
    if len(content) != record["bytes"] or hashlib.sha256(content).hexdigest() != record["sha256"]:
        raise ValueError(f"图片校验失败: {key};大小或 SHA-256 与清单不一致")


def download_image(key: str, record: dict) -> bytes:
    request = Request(record["url"], headers={"User-Agent": "hand-drawn-styles", "Cache-Control": "no-cache"})
    try:
        with urlopen(request, timeout=DOWNLOAD_TIMEOUT_SECONDS) as response:
            content = response.read(record["bytes"] + 1)
    except (OSError, URLError, HTTPException) as error:
        raise ValueError(f"图片下载失败: {key};请检查网络后重试 hosted_images.py fetch") from error
    verify_image_bytes(content, record, key)
    return content


def write_atomic(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".image-", delete=False) as temporary:
        temporary_path = Path(temporary.name)
        try:
            temporary.write(content)
            temporary.flush()
        except BaseException:
            temporary_path.unlink(missing_ok=True)
            raise
    try:
        temporary_path.replace(path)
    finally:
        temporary_path.unlink(missing_ok=True)


def resolve_image(key: str, *, manifest: dict | None = None, cache_root: Path | None = None, offline: bool | None = None) -> Path:
    record = image_record(key, manifest)
    target = cache_path(key, record, cache_root)
    if target.is_file():
        try:
            verify_image_bytes(target.read_bytes(), record, key)
            return target
        except ValueError:
            pass
    if offline is None:
        offline = os.environ.get("HAND_DRAWN_OFFLINE") == "1"
    if offline:
        raise ValueError(f"离线缓存缺少有效图片: {key};请联网运行 hosted_images.py fetch")
    # A partial or substituted response must never become a usable reference.
    content = download_image(key, record)
    write_atomic(target, content)
    return target


def verify_remote_image(key: str, *, manifest: dict | None = None) -> dict:
    record = image_record(key, manifest)
    download_image(key, record)
    return {"key": key, "status": "pass", **record}


def register_image(key: str, source: Path, *, manifest_path: Path | None = None, cache_root: Path | None = None) -> dict:
    path = manifest_path or MANIFEST_PATH
    manifest = load_manifest(path)
    content = source.read_bytes()
    record = {"url": f"{manifest['base_url']}/{quote(key, safe='/')}", "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}
    previous = manifest["images"].get(key)
    if previous and previous != record:
        raise ValueError(f"图片名称已存在: {key};修改后的图片必须使用新名称")
    manifest["images"][key] = record
    validate_manifest(manifest)
    write_atomic(cache_path(key, record, cache_root), content)
    write_atomic(path, (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode())
    return record


def build_site_archive(baseline: Path, output: Path, *, manifest: dict | None = None, cache_root: Path | None = None) -> dict:
    manifest = validate_manifest(manifest or load_manifest())
    prefix = urlsplit(manifest["base_url"]).path.strip("/")
    if not prefix or ".." in PurePosixPath(prefix).parts:
        raise ValueError("图片托管必须使用独立目录")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="hand-drawn-site-") as temporary:
        staging = Path(temporary) / "site"
        staging.mkdir()
        with zipfile.ZipFile(baseline) as archive:
            for name in archive.namelist():
                if not (staging / name).resolve().is_relative_to(staging.resolve()):
                    raise ValueError(f"原站点 ZIP 包含越界路径: {name}")
            archive.extractall(staging)
        if not (staging / "index.html").is_file():
            raise ValueError("原站点 ZIP 缺少根目录 index.html;停止部署，避免替换错误站点")
        for key in manifest["images"]:
            source = resolve_image(key, manifest=manifest, cache_root=cache_root)
            target = staging / prefix / key
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        (staging / prefix / "image-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary_archive = Path(temporary) / "site.zip"
        with zipfile.ZipFile(temporary_archive, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(staging.rglob("*")):
                if path.is_file():
                    archive.write(path, path.relative_to(staging).as_posix())
        shutil.copyfile(temporary_archive, output)
    return {"archive": str(output.resolve()), "archive_bytes": output.stat().st_size, "image_count": len(manifest["images"])}


def runtime_image_keys() -> list[str]:
    import render_prompt
    manifest = load_manifest()
    return sorted({key_for_url(reference, manifest) if reference.startswith("https://") else reference for style in render_prompt.list_styles() for reference in style["references"]})


def main() -> int:
    parser = argparse.ArgumentParser(description="登记、下载、验证托管图片；构建保留原站点的 Netlify ZIP")
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("fetch", "verify"):
        selection = commands.add_parser(command)
        selection.add_argument("keys", nargs="*", help="清单中的图片路径；省略时选择运行参考图")
        selection.add_argument("--all", action="store_true", help="处理清单中的全部图片")
    registration = commands.add_parser("register")
    registration.add_argument("key", help="新的稳定路径，例如 examples/new-style.png")
    registration.add_argument("source", type=Path, help="完成隐私清理的原始图片")
    site = commands.add_parser("build-site")
    site.add_argument("--base-zip", type=Path, required=True, help="从 Netlify 下载的当前完整部署 ZIP")
    site.add_argument("--output", type=Path, default=ROOT / "dist/netlify-images/hand-drawn-netlify.zip")
    args = parser.parse_args()
    try:
        if args.command == "register":
            result = {"status": "registered-not-published", **register_image(args.key, args.source)}
        elif args.command == "build-site":
            result = {"status": "candidate-not-published", **build_site_archive(args.base_zip, args.output)}
        else:
            manifest = load_manifest()
            keys = sorted(manifest["images"]) if args.all else args.keys or runtime_image_keys()
            if args.command == "fetch":
                result = {"status": "pass", "images": [{"key": key, "path": str(resolve_image(key, manifest=manifest))} for key in keys]}
            else:
                checks = []
                with ThreadPoolExecutor(max_workers=4) as executor:
                    pending = {executor.submit(verify_remote_image, key, manifest=manifest): key for key in keys}
                    for future in as_completed(pending):
                        key = pending[future]
                        try:
                            checks.append(future.result())
                        except ValueError as error:
                            checks.append({"key": key, "status": "failed", "error": str(error)})
                result = {"status": "pass" if all(item["status"] == "pass" for item in checks) else "failed", "images": sorted(checks, key=lambda item: item["key"])}
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
        print(f"hosted_images: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if result["status"] == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
