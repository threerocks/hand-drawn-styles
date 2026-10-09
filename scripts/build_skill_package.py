#!/usr/bin/env python3
"""Build a minimal, relocatable skill archive and verify it outside the checkout."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

import check_skill


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIRECTORY = "hand-drawn"
MAXIMUM_PACKAGE_BYTES = 1024 * 1024


def build_archive(output: Path) -> dict[str, object]:
    report = check_skill.build_check_report(ROOT, smoke=False)
    if report["status"] != "pass":
        raise ValueError("安装依赖检查失败: " + "; ".join(report["failures"]))
    manifest = {"format_version": 1, "files": {}}
    contents = {}
    for name in check_skill.collect_runtime_paths():
        source = ROOT / name
        if not source.resolve().is_relative_to(ROOT):
            raise ValueError(f"运行文件位于仓库之外: {name}")
        contents[name] = source.read_bytes()
        manifest["files"][name] = {"bytes": len(contents[name]), "sha256": hashlib.sha256(contents[name]).hexdigest()}
    contents["PACKAGE-MANIFEST.json"] = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(prefix="hand-drawn-package-", suffix=".zip", dir=output.parent, delete=False) as temporary:
        temporary_path = Path(temporary.name)
    try:
        with zipfile.ZipFile(temporary_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for name, content in sorted(contents.items()):
                entry = zipfile.ZipInfo(f"{PACKAGE_DIRECTORY}/{name}", date_time=(2020, 1, 1, 0, 0, 0))
                executable = name.endswith(".sh")
                entry.external_attr = (0o100755 if executable else 0o100644) << 16
                entry.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(entry, content)
        if temporary_path.stat().st_size > MAXIMUM_PACKAGE_BYTES:
            raise ValueError("安装包超过 1 MiB;图片必须托管并登记链接，禁止打包图片缓存")
        temporary_path.replace(output)
    finally:
        temporary_path.unlink(missing_ok=True)
    return {"archive": str(output.resolve()), "archive_bytes": output.stat().st_size, "file_count": len(contents), "sha256": hashlib.sha256(output.read_bytes()).hexdigest()}


def verify_archive(archive_path: Path) -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="hand-drawn-install-") as temporary_directory:
        install_root = Path(temporary_directory).resolve()
        with zipfile.ZipFile(archive_path) as archive:
            for name in archive.namelist():
                if not (install_root / name).resolve().is_relative_to(install_root):
                    raise ValueError(f"安装包包含越界路径: {name}")
            archive.extractall(install_root)
        installed_checker = install_root / PACKAGE_DIRECTORY / "scripts/check_skill.py"
        completed = subprocess.run([sys.executable, "-B", str(installed_checker), "--json"], cwd=install_root, capture_output=True, text=True, timeout=120)
        if completed.returncode:
            raise ValueError("独立安装验证失败: " + (completed.stderr.strip() or completed.stdout.strip()))
        return json.loads(completed.stdout)


def main() -> int:
    parser = argparse.ArgumentParser(description="构建轻量 Skill ZIP,默认在独立临时目录验证安装")
    parser.add_argument("--output", type=Path, default=ROOT / "dist/hand-drawn-skill.zip")
    parser.add_argument("--skip-verify", action="store_true", help="只构建候选包;未经验证不可作为发布包")
    args = parser.parse_args()
    try:
        report = build_archive(args.output.resolve())
        if not args.skip_verify:
            report["verification"] = verify_archive(args.output.resolve())
        report["status"] = "candidate-only" if args.skip_verify else "verified"
    except (OSError, ValueError, zipfile.BadZipFile, subprocess.TimeoutExpired) as error:
        print(f"build_skill_package: {error}", file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
