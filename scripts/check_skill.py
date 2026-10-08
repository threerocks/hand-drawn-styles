#!/usr/bin/env python3
"""Check installed dependencies and exercise every style without generating images."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

import render_prompt


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_FILES = (
    "SKILL.md", "AGENTS.md", "PROTOCOL.md", "STYLES.md", "LICENSE", "INSTALL.md",
    "scripts/render_prompt.py", "scripts/check_skill.py",
    "scripts/validate_style_20_asset.py", "scripts/generate_monologue_card_with_codex.sh",
)
DEFAULT_SCENE = (
    "SCENE: background painted with long rough vertical and diagonal dry-brush streaks "
    "in pastel sky-blue with soft cream-yellow scuffed patches【背景元素】, bristle marks "
    "and broken paint edges visible, deliberately unfinished with raw white paper "
    "showing around the border like a concept sketch."
)
SMOKE_PARAMETERS = {
    "1": {"N": "3", "分镜列表": "第一格：番茄计时。第二格：专注工作。第三格：休息。"},
    "2": {"主体": "a child holding a book", "主色调": "blue and orange", "标题词": "READ"},
    "3": {"主体": "a cat holding an umbrella in the rain"},
    "3.1": {"主体": "妈妈和孩子一起看书", "文字": "不加任何文字"},
    "4": {"N": "3", "分镜列表": "第一格：准备。第二格：尝试。第三格：复盘。"},
    "5": {"主体": "一只猫抱着书"},
    "6": {"主体": "a cat reading a book"},
    "7": {"主体": "a child holding a book", "主色调": "blue and orange", "标题词": "READ"},
    "8": {"主体": "a bird resting on a branch"},
    "9": {"主体": "a cat holding a book", "主色调": "blue and orange"},
    "10": {"主体": "妈妈和孩子一起看书", "橙色关键物": "书", "文字": "不加任何文字"},
    "11": {"主体": "a child holding a book", "背景浓度": "白纸上人物身后一侧轻扫几笔淡奶油/杏色干刷痕", "焦点物件": "无", "构图": "单人半身立绘", "文字": "不加任何文字"},
    "12": {"主体": "a child holding a book", "构图": "waist-up portrait", "场景": DEFAULT_SCENE, "文字": "No text anywhere."},
    "13": {"主体": "a musician holding a violin", "构图": "centered, waist-up", "底色": "warm ochre-brown", "点缀元素": "one stylized folk cloud, a few stylized leaves and one rolled paper spiral"},
    "14": {"主体": "a child holding a book", "构图": "standing full-body, centered", "纸底色": "warm off-white (≈#F8F7F2)", "光影": "One single soft pale-blue oval shadow under the feet, no other shading or shadows anywhere."},
    "15": {"主体": "a woman holding a book", "构图": "full-body standing, front view, centered, symmetrical, square composition", "眼型": "tiny half-lidded bored sleepy eyes", "穿搭": "a blue hoodie", "胡茬": "", "肤色": "blush pink", "背景底色": "warm blush-peach"},
    "16": {"主体": "a child holding a book", "构图": "waist-up centered portrait facing the viewer", "背景色": "warm amber-orange", "文字": "No text anywhere."},
    "17": {"主体": "a child holding a book", "构图": "head-and-shoulders portrait", "背景色": "warm peach fading to pale cream near the top", "配色": "blue shirt and warm peach background", "文字": "No text anywhere."},
    "18": {"主体": "a child holding a book", "构图": "full-body, centered in the lower-middle with huge calm negative space", "文字": "No text anywhere."},
    "19": {"主体": "a small elephant lifting one paper lantern with its trunk", "文字": "No text anywhere."},
    "20": {"主体": "a grandmother and child repairing one kite together", "文字": "No text anywhere."},
    "21": {"文字": "今天慢一点，\n也能走到想去的地方。"},
}


def collect_runtime_paths() -> list[str]:
    paths = set(RUNTIME_FILES)
    for style in render_prompt.list_styles():
        for reference in style["references"]:
            paths.add(reference)
            for suffix in (".privacy.json", ".provenance.json"):
                if (ROOT / f"{reference}{suffix}").is_file():
                    paths.add(f"{reference}{suffix}")
    return sorted(paths)


def check_document_dependencies(root: Path) -> list[str]:
    failures = []
    for name in ("SKILL.md", "AGENTS.md", "PROTOCOL.md", "STYLES.md", "INSTALL.md", "README.md"):
        document = root / name
        if not document.is_file():
            continue
        for number, line in enumerate(document.read_text(encoding="utf-8").splitlines(), 1):
            references = re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", line)
            references += re.findall(r'<img\b[^>]*\bsrc=[\"\']([^\"\']+)', line)
            references += re.findall(r"`((?:assets|examples|scripts)/[^\s`]+\.(?:png|jpg|jpeg|webp|py|sh))(?=[\s`])", line)
            for reference in references:
                target = reference.strip().strip("<>")
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                dependency = document.parent / unquote(parsed.path)
                if not dependency.exists():
                    failures.append(f"{name}:{number}: 缺少依赖 {target}")
    return failures


def check_package_manifest(root: Path) -> list[str]:
    manifest_path = root / "PACKAGE-MANIFEST.json"
    if not manifest_path.is_file():
        return []
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or manifest.get("format_version") != 1 or not isinstance(manifest.get("files"), dict):
        return ["安装包清单格式不受支持"]
    failures = []
    for name, expected in manifest["files"].items():
        if not isinstance(name, str) or not isinstance(expected, dict) or not isinstance(expected.get("sha256"), str):
            failures.append("安装包清单包含无效文件记录")
            continue
        dependency = (root / name).resolve()
        if not dependency.is_relative_to(root.resolve()):
            failures.append(f"安装包清单包含越界路径: {name}")
            continue
        if not dependency.is_file():
            failures.append(f"安装包缺少文件: {name}")
        elif hashlib.sha256(dependency.read_bytes()).hexdigest() != expected["sha256"]:
            failures.append(f"安装包文件校验失败: {name}")
    return failures


def run_smoke_checks(root: Path) -> list[dict[str, object]]:
    checks = []
    with tempfile.TemporaryDirectory(prefix="hand-drawn-calls-") as working_directory:
        for style in render_prompt.list_styles():
            style_id = style["style_id"]
            parameters = SMOKE_PARAMETERS.get(style_id)
            if parameters is None:
                checks.append({"style_id": style_id, "status": "failed", "error": "缺少完整调用场景"})
                continue
            command = [sys.executable, "-B", str(root / "scripts/render_prompt.py"), "--style", style_id]
            for name, value in parameters.items():
                command.extend(("--var", f"{name}={value}"))
            try:
                completed = subprocess.run(command, cwd=working_directory, capture_output=True, text=True, timeout=60)
            except subprocess.TimeoutExpired:
                checks.append({"style_id": style_id, "status": "failed", "error": "调用超过 60 秒"})
                continue
            failure = completed.stderr.strip() if completed.returncode else ""
            if not failure and completed.returncode:
                failure = f"退出码 {completed.returncode}"
            prompt = completed.stdout
            json_output = completed.stdout
            if not failure and style_id not in {"3.1", "19", "20"}:
                try:
                    json_completed = subprocess.run(command + ["--format", "json"], cwd=working_directory, capture_output=True, text=True, timeout=60)
                    json_output = json_completed.stdout
                    if json_completed.returncode:
                        failure = json_completed.stderr.strip() or f"JSON 调用退出码 {json_completed.returncode}"
                except subprocess.TimeoutExpired:
                    failure = "JSON 调用超过 60 秒"
            if not failure:
                try:
                    payload = json.loads(json_output)
                    if style_id not in {"3.1", "19", "20"} and payload["prompt"] != prompt.rstrip("\n"):
                        failure = "纯文本与 JSON 的 prompt 不一致"
                    prompt = payload["prompt"]
                    if payload["style_id"] != style_id:
                        failure = "JSON 调用包缺少画风身份"
                    style_references = set()
                    for reference in payload["references"]:
                        reference_path = Path(reference["path"]).resolve()
                        if not reference_path.is_relative_to(root.resolve()) or not reference_path.is_file():
                            failure = "JSON 调用包未引用安装目录内的参考图"
                        elif reference["role"] == "style-only":
                            style_references.add(reference_path.relative_to(root.resolve()).as_posix())
                    if style_references != set(style["references"]):
                        failure = "JSON 参考图与配方引用不一致"
                except (ValueError, TypeError, KeyError):
                    failure = "JSON 调用包格式无效"
            if not failure and (not prompt.strip() or render_prompt.PLACEHOLDER_PATTERN.search(prompt)):
                failure = "输出为空或仍包含待填参数"
            checks.append({"style_id": style_id, "status": "failed" if failure else "pass", **({"error": failure} if failure else {})})
    return checks


def build_check_report(root: Path, *, smoke: bool = True) -> dict[str, object]:
    failures = [f"缺少运行文件: {name}" for name in collect_runtime_paths() if not (root / name).is_file()]
    failures += check_document_dependencies(root)
    failures += check_package_manifest(root)
    catalog = render_prompt.list_styles()
    style_ids = {style["style_id"] for style in catalog}
    for alias, style_id in render_prompt.STYLE_ALIASES.items():
        if style_id not in style_ids or render_prompt.canonical_style_id(alias) != style_id:
            failures.append(f"别名未对应有效画风: {alias}")
    protocol = (root / "PROTOCOL.md").read_text(encoding="utf-8") if (root / "PROTOCOL.md").is_file() else ""
    for aliases, style_id in re.findall(r"((?:`[^`]+`\s*)+)\((\d+(?:\.\d+)?)\)", protocol):
        for alias in re.findall(r"`([^`]+)`", aliases):
            if render_prompt.canonical_style_id(alias) != style_id:
                failures.append(f"协议别名不可调用: {alias}")
    style_checks = run_smoke_checks(root) if smoke and not failures else []
    failures += [f"画风 {check['style_id']}: {check['error']}" for check in style_checks if check["status"] == "failed"]
    return {
        "status": "failed" if failures else "pass",
        "style_count": len(catalog),
        "alias_count": len(render_prompt.STYLE_ALIASES),
        "runtime_file_count": len(collect_runtime_paths()),
        "smoke_checked": len(style_checks),
        "styles": style_checks,
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="检查安装文件、资源引用、别名和所有画风的完整调用;不生图")
    parser.add_argument("--json", action="store_true", help="输出 JSON 报告")
    parser.add_argument("--skip-smoke", action="store_true", help="只检查文件和引用,不执行画风调用")
    args = parser.parse_args()
    try:
        report = build_check_report(ROOT, smoke=not args.skip_smoke)
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired) as error:
        print(f"check_skill: {error}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"{report['status']}: {report['style_count']} 套配方, {report['alias_count']} 个别名, {report['smoke_checked']} 项完整调用")
        for failure in report["failures"]:
            print(f"- {failure}")
    return 0 if report["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
