#!/usr/bin/env python3
"""Render one hand-drawn style recipe without paraphrasing it."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STYLES_PATH = ROOT / "STYLES.md"
PLACEHOLDER_PATTERN = re.compile(r"【([^】]+)】")
STYLE_ALIASES = {
    "family-crayon-card": "1.2",
    "parent-child-crayon": "1.2",
    "submission-crayon": "1.2",
    "亲子投稿蜡笔故事卡": "1.2",
    "家庭投稿蜡笔卡": "1.2",
}
STYLE_1_2_ANCHOR_SHA256 = "d1eb06abd3e81115483b6d6227746ad1811f6c2bc8e0670f573fd4d6f9eaafc3"
STYLE_1_2_ANCHOR_SIZE = (1086, 1448)
STYLE_INJECTION_TERMS = (
    "画风",
    "风格",
    "线稿",
    "线条",
    "描边",
    "配色",
    "色板",
    "低饱和",
    "高饱和",
    "蜡笔质感",
    "水彩质感",
    "粗黑轮廓",
    "留白比例",
    "数字插画",
    "商业绘本",
    "渐变",
    "体积光",
    "纸张纹理",
    "参考图风格",
    "灰调",
    "暖调",
    "冷调",
    "调色",
    "笔触",
    "材质",
    "质感",
    "外轮廓",
    "内轮廓",
)
STYLE_INJECTION_PATTERNS = (
    re.compile(r"(?:加粗|变粗|粗一点|减细|变细).{0,8}(?:轮廓|边线|线)"),
    re.compile(r"(?:轮廓|边线|线).{0,8}(?:加粗|变粗|粗一点|减细|变细)"),
    re.compile(r"(?:只用|限制为|控制在).{0,16}(?:种|个).{0,10}(?:色|颜色|色调)"),
    re.compile(r"(?:改成|画成|采用|使用|渲染成).{0,24}(?:画风|风格|线稿|描边|配色|色调|质感|笔触|插画|绘本|水彩|蜡笔)"),
)


def canonical_style_id(value: str) -> str:
    return STYLE_ALIASES.get(value.strip().lower(), value.strip())


def extract_template(style_id: str) -> str:
    source = STYLES_PATH.read_text(encoding="utf-8")
    heading = re.compile(
        rf"^## {re.escape(style_id)}(?:\s|$).*?^```(?:\w+)?\s*$\n(.*?)^```\s*$",
        re.MULTILINE | re.DOTALL,
    )
    match = heading.search(source)
    if not match:
        raise ValueError(f"STYLES.md 中不存在画风 {style_id} 的代码块配方")
    return match.group(1).strip()


def parse_vars(items: list[str]) -> dict[str, str]:
    values: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"--var 必须使用 名称=内容 格式: {item}")
        key, value = item.split("=", 1)
        key = key.strip().removeprefix("【").removesuffix("】")
        if not key or not value.strip():
            raise ValueError(f"--var 的名称和内容都不能为空: {item}")
        values[key] = value.strip()
    return values


def render(template: str, values: dict[str, str], aspect: str | None) -> str:
    expected = set(PLACEHOLDER_PATTERN.findall(template))
    unknown = sorted(set(values) - expected)
    if unknown:
        raise ValueError(f"配方不包含这些占位符: {', '.join(unknown)}")

    missing = sorted(expected - set(values))
    if missing:
        raise ValueError(f"缺少占位符: {', '.join(missing)}")

    output = template
    for key, value in values.items():
        output = output.replace(f"【{key}】", value)

    unresolved = sorted(set(PLACEHOLDER_PATTERN.findall(output)))
    if unresolved:
        raise ValueError(f"仍有未替换占位符: {', '.join(unresolved)}")

    if aspect:
        output = f"{output}\n\n画幅比例:{aspect.strip()}。"
    return output


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"参考图不是有效 PNG: {path}")
    return struct.unpack(">II", data[16:24])


def validate_style_1_2_anchor(anchor: Path) -> None:
    if not anchor.is_file():
        raise ValueError(f"画风 1.2 锚点不可用,停止正式生产: {anchor}")
    if png_size(anchor) != STYLE_1_2_ANCHOR_SIZE:
        raise ValueError(f"画风 1.2 锚点尺寸不匹配,停止正式生产: {anchor}")
    digest = hashlib.sha256(anchor.read_bytes()).hexdigest()
    if digest != STYLE_1_2_ANCHOR_SHA256:
        raise ValueError(f"画风 1.2 锚点哈希不匹配,停止正式生产: {anchor}")


def validate_style_1_2_subject(subject: str) -> None:
    hits = [term for term in STYLE_INJECTION_TERMS if term in subject]
    pattern_hits = [pattern.pattern for pattern in STYLE_INJECTION_PATTERNS if pattern.search(subject)]
    if hits or pattern_hits:
        raise ValueError(
            "画风 1.2 的主体字段只能描述人物、动作、关系和道具;"
            f"检测到疑似业务画风注入: {', '.join(hits + pattern_hits)}"
        )


def style_1_2_title_instruction(title: str) -> str:
    clean = title.strip()
    if not clean or "\n" in clean or "\r" in clean:
        raise ValueError("--title 必须是一行非空的准确标题原文")
    return (
        "画面顶部的大片留白区写手写中文标题,逐字为“"
        f"{clean}”;字像普通家长用粗黑笔写的,大小略不齐但准确清楚"
    )


def validate_style_1_2_text(text: str, expected_title_instruction: str | None) -> None:
    allowed = {"不加任何文字"}
    if expected_title_instruction:
        allowed.add(expected_title_instruction)
    if text not in allowed:
        raise ValueError(
            "画风 1.2 的文字输入只允许 --text '不加任何文字' 或独立 --title '准确标题原文';"
            "不得把画风或排版指令塞进 --text/--var 文字"
        )


def validate_character_references(items: list[str]) -> list[Path]:
    paths: list[Path] = []
    for item in items:
        path = Path(item).expanduser().resolve()
        if not path.is_file():
            raise ValueError(f"角色参考图不可用: {path}")
        if path.suffix.lower() == ".png":
            png_size(path)
        elif path.suffix.lower() not in {".jpg", ".jpeg", ".webp"}:
            raise ValueError(f"角色参考图格式不受支持: {path}")
        paths.append(path)
    return paths


def build_payload(
    style_id: str,
    prompt: str,
    values: dict[str, str],
    aspect: str | None,
    character_references: list[Path],
) -> dict[str, object]:
    payload: dict[str, object] = {
        "style_id": style_id,
        "prompt": prompt,
        "references": [],
        "inputs": {"variables": values, "aspect": aspect or None},
    }
    if style_id == "1.2":
        anchor = ROOT / "assets/style-1.2/anchor-family.png"
        validate_style_1_2_anchor(anchor)
        payload["style_contract"] = "family-crayon-card-v1"
        references: list[dict[str, str]] = [
            {
                "path": str(anchor),
                "role": "style-only",
                "required_for": "every production image",
                "must_not_copy": "people, clothing, positions, or story content",
            }
        ]
        references.extend(
            {
                "path": str(path),
                "role": "character",
                "required_for": "every image containing this recurring character",
                "must_not_replace": "the style-only reference",
            }
            for path in character_references
        )
        payload["references"] = references
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="从 STYLES.md 原样提取配方、填占位符并输出最终 prompt。"
    )
    parser.add_argument("--style", required=True, help="画风编号或已登记别名")
    parser.add_argument("--subject", help="填入【主体】")
    parser.add_argument("--text", help="填入【文字】")
    parser.add_argument("--title", help="风格 1.2 的准确标题原文;渲染器负责生成固定文字指令")
    parser.add_argument("--aspect", help="可选画幅比例,例如 3:4")
    parser.add_argument(
        "--character-reference",
        action="append",
        default=[],
        metavar="PATH",
        help="可重复传入连续故事的角色参考图;不会替代 1.2 画风锚点",
    )
    parser.add_argument(
        "--var",
        action="append",
        default=[],
        metavar="名称=内容",
        help="填充任意占位符;可重复使用",
    )
    parser.add_argument(
        "--format",
        choices=("auto", "text", "json"),
        default="auto",
        help="auto 对 1.2 输出正式 JSON、其他画风输出 text;json 含画风锚点等调用合同",
    )
    parser.add_argument(
        "--text-only-preview",
        action="store_true",
        help="只允许 1.2 的非生产预览显式输出纯 prompt;不得用于正式生图",
    )
    args = parser.parse_args()

    try:
        style_id = canonical_style_id(args.style)
        values = parse_vars(args.var)
        if args.text is not None and args.title is not None:
            raise ValueError("--text 与 --title 不能同时使用")
        if args.subject is not None:
            values["主体"] = args.subject.strip()
        title_instruction = None
        if args.title is not None:
            title_instruction = style_1_2_title_instruction(args.title)
            values["文字"] = title_instruction
        if args.text is not None:
            values["文字"] = args.text.strip()
        if style_id == "1.2":
            validate_style_1_2_subject(values.get("主体", ""))
            validate_style_1_2_text(values.get("文字", ""), title_instruction)
        character_references = validate_character_references(args.character_reference)
        template = extract_template(style_id)
        prompt = render(template, values, args.aspect)
        payload = build_payload(
            style_id,
            prompt,
            values,
            args.aspect,
            character_references,
        )
        output_format = "json" if args.format == "auto" and style_id == "1.2" else args.format
        if output_format == "auto":
            output_format = "text"
        if style_id == "1.2" and output_format == "text" and not args.text_only_preview:
            raise ValueError(
                "画风 1.2 正式生产不能只输出 prompt;请使用 --format json,"
                "或仅在非生产预览时显式加 --text-only-preview"
            )
    except ValueError as error:
        print(f"render_prompt: {error}", file=sys.stderr)
        return 2

    if output_format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
