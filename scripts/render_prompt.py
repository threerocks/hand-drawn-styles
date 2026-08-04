#!/usr/bin/env python3
"""Render one hand-drawn style recipe without paraphrasing it."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import sys
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STYLES_PATH = ROOT / "STYLES.md"
PLACEHOLDER_PATTERN = re.compile(r"【([^】]+)】")
STYLE_ALIASES = {
    "family-crayon-card": "1.2",
    "parent-child-crayon": "1.2",
    "submission-crayon": "1.2",
    "亲子手绘": "1.2",
    "家庭蜡笔画": "1.2",
    "亲子蜡笔故事": "1.2",
    "亲子投稿蜡笔故事卡": "1.2",
    "家庭投稿蜡笔卡": "1.2",
}
STYLE_1_2_ANCHOR_PIXEL_SHA256 = "1ae67d0088d58f2527ae81aa05d8453ce1ccc9d4614342c0bb1ab71a5e4895cd"
STYLE_1_2_ANCHOR_SIZE = (1086, 1448)
STYLE_1_2_SCRIBBLE_CORRECTION_PROMPT = """Image 1 is the edit target. Image 2 is the approved style-only reference.
Change ONLY the crayon coloring marks inside and around the existing people, clothing, hair, furniture, books, and props in Image 1. Preserve the exact characters, faces, poses, actions, composition, object count, outlines, colors, white background, and framing.
Rework the coloring to match Image 2's genuinely clumsy child scribbling: coarse blunt wax-crayon strokes with abrupt starts and stops; visibly mixed horizontal, vertical, diagonal, looping, zigzag and crossing directions inside the SAME color area; uneven pressure; isolated heavy clumps next to large untouched white-paper holes; some strokes stop far before the black outline and some overshoot well beyond it. Each color area must have a different scribble rhythm.
Critical: NO neat diagonal hatching, NO fine dense parallel lines, NO even spacing, NO uniform coverage, NO repeated digital crayon texture. Make the coloring obviously messier, coarser, patchier, emptier and more misregistered than Image 1. Do not add text or new objects."""
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
    "平行排线",
    "均匀斜线",
    "等间距排线",
    "统一笔刷",
    "覆盖均匀",
    "蜡笔滤镜",
    "材质",
    "质感",
    "外轮廓",
    "内轮廓",
)
STYLE_RATIO_EXPRESSION = (
    r"(?:\d+(?:\.\d+)?\s*%|百分之[零一二三四五六七八九十百两〇\d]+|"
    r"[一二三四五六七八九十两\d]+成|"
    r"[零一二三四五六七八九十百两〇\d]+分之[零一二三四五六七八九十百两〇\d]+)"
)
STYLE_LENGTH_EXPRESSION = r"[零一二三四五六七八九十百两〇\d]+(?:\.\d+)?\s*(?:毫米|厘米|mm|cm)"
STYLE_INJECTION_PATTERNS = (
    re.compile(r"(?:加粗|变粗|粗一点|减细|变细).{0,8}(?:轮廓|边线|线)"),
    re.compile(r"(?:轮廓|边线|线).{0,8}(?:加粗|变粗|粗一点|减细|变细)"),
    re.compile(r"(?:只用|限制为|控制在).{0,16}(?:种|个).{0,10}(?:色|颜色|色调)"),
    re.compile(r"(?:改成|画成|采用|使用|渲染成).{0,24}(?:画风|风格|线稿|描边|配色|色调|质感|笔触|插画|绘本|水彩|蜡笔)"),
    re.compile(
        rf"(?:严格|固定|精确|统一|每块|每件|每处|全部).{{0,16}}"
        rf"(?:留白|露白|越界|出界|涂色|空出|超出边缘).{{0,10}}{STYLE_RATIO_EXPRESSION}"
    ),
    re.compile(
        rf"(?:留白|露白|越界|出界|涂色|空出|超出边缘).{{0,10}}{STYLE_RATIO_EXPRESSION}"
    ),
    re.compile(
        rf"(?:每块|每件|每处|全部).{{0,16}}(?:空出|保留).{{0,8}}"
        rf"{STYLE_RATIO_EXPRESSION}.{{0,4}}(?:白|空白)"
    ),
    re.compile(
        r"(?:人物|角色|所有人|每个人|眼睛|五官|脸型|头型|肩宽|姿势).{0,20}"
        r"(?:同一|统一|固定|标准).{0,8}(?:尺寸|模板|骨架|比例)"
    ),
    re.compile(
        rf"(?:衣服|头发|肤色|蜡笔|色块|涂色).{{0,14}}(?:覆盖率|填色率).{{0,12}}"
        rf"{STYLE_RATIO_EXPRESSION}"
    ),
    re.compile(
        r"(?:每张|人物|角色|姿势).{0,14}(?:套用|使用|采用).{0,8}"
        r"(?:同一|统一|固定|标准)?(?:人物|角色)?模板"
    ),
    re.compile(r"(?:姿势|人物|轮廓|五官).{0,14}(?:对称规整|尽量对称|统一规整|标准化)"),
    re.compile(
        rf"(?:越界|出界|色痕|线条).{{0,14}}(?:平均|统一|固定|精确).{{0,8}}"
        rf"(?:控制|设为|定为)?(?:在)?{STYLE_LENGTH_EXPRESSION}"
    ),
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


def png_chunks(path: Path) -> list[tuple[bytes, bytes]]:
    data = path.read_bytes()
    if len(data) < 33 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"参考图不是有效 PNG: {path}")

    chunks: list[tuple[bytes, bytes]] = []
    offset = 8
    while offset < len(data):
        if offset + 12 > len(data):
            raise ValueError(f"参考图 PNG 数据不完整: {path}")
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        chunk_type = data[offset + 4 : offset + 8]
        chunk_data = data[offset + 8 : offset + 8 + length]
        crc_offset = offset + 8 + length
        if crc_offset + 4 > len(data):
            raise ValueError(f"参考图 PNG 数据不完整: {path}")
        expected_crc = struct.unpack(">I", data[crc_offset : crc_offset + 4])[0]
        actual_crc = zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF
        if actual_crc != expected_crc:
            raise ValueError(f"参考图 PNG 校验失败: {path}")
        chunks.append((chunk_type, chunk_data))
        offset = crc_offset + 4
        if chunk_type == b"IEND":
            break
    if not chunks or chunks[-1][0] != b"IEND" or offset != len(data):
        raise ValueError(f"参考图 PNG 结构不完整: {path}")
    return chunks


def png_pixel_sha256(path: Path) -> tuple[tuple[int, int], str]:
    chunks = png_chunks(path)
    ihdr_chunks = [chunk for chunk_type, chunk in chunks if chunk_type == b"IHDR"]
    if len(ihdr_chunks) != 1 or len(ihdr_chunks[0]) != 13:
        raise ValueError(f"参考图 PNG 缺少有效 IHDR: {path}")
    width, height, bit_depth, color_type, compression, filtering, interlace = struct.unpack(
        ">IIBBBBB", ihdr_chunks[0]
    )
    bytes_per_pixel = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}.get(color_type)
    if (
        bit_depth != 8
        or bytes_per_pixel is None
        or compression != 0
        or filtering != 0
        or interlace != 0
    ):
        raise ValueError(f"参考图 PNG 编码不受支持,停止正式生产: {path}")

    compressed = b"".join(chunk for chunk_type, chunk in chunks if chunk_type == b"IDAT")
    try:
        raw = zlib.decompress(compressed)
    except zlib.error as error:
        raise ValueError(f"参考图 PNG 像素数据损坏: {path}") from error

    stride = width * bytes_per_pixel
    if len(raw) != (stride + 1) * height:
        raise ValueError(f"参考图 PNG 像素长度不匹配: {path}")

    rows: list[bytes] = []
    previous = bytearray(stride)
    offset = 0
    for _ in range(height):
        filter_type = raw[offset]
        offset += 1
        scanline = raw[offset : offset + stride]
        offset += stride
        reconstructed = bytearray(stride)
        for index, value in enumerate(scanline):
            left = reconstructed[index - bytes_per_pixel] if index >= bytes_per_pixel else 0
            above = previous[index]
            upper_left = previous[index - bytes_per_pixel] if index >= bytes_per_pixel else 0
            if filter_type == 0:
                predictor = 0
            elif filter_type == 1:
                predictor = left
            elif filter_type == 2:
                predictor = above
            elif filter_type == 3:
                predictor = (left + above) // 2
            elif filter_type == 4:
                candidate = left + above - upper_left
                left_distance = abs(candidate - left)
                above_distance = abs(candidate - above)
                upper_left_distance = abs(candidate - upper_left)
                predictor = (
                    left
                    if left_distance <= above_distance and left_distance <= upper_left_distance
                    else above
                    if above_distance <= upper_left_distance
                    else upper_left
                )
            else:
                raise ValueError(f"参考图 PNG 使用未知过滤器: {path}")
            reconstructed[index] = (value + predictor) & 0xFF
        rows.append(bytes(reconstructed))
        previous = reconstructed
    return (width, height), hashlib.sha256(b"".join(rows)).hexdigest()


def png_size(path: Path) -> tuple[int, int]:
    chunks = png_chunks(path)
    ihdr_chunks = [chunk for chunk_type, chunk in chunks if chunk_type == b"IHDR"]
    if len(ihdr_chunks) != 1 or len(ihdr_chunks[0]) != 13:
        raise ValueError(f"参考图 PNG 缺少有效 IHDR: {path}")
    width, height = struct.unpack(">II", ihdr_chunks[0][:8])
    return width, height


def validate_style_1_2_anchor(anchor: Path) -> None:
    if not anchor.is_file():
        raise ValueError(f"画风 1.2 锚点不可用,停止正式生产: {anchor}")
    size, digest = png_pixel_sha256(anchor)
    if size != STYLE_1_2_ANCHOR_SIZE:
        raise ValueError(f"画风 1.2 锚点尺寸不匹配,停止正式生产: {anchor}")
    if digest != STYLE_1_2_ANCHOR_PIXEL_SHA256:
        raise ValueError(f"画风 1.2 锚点像素不匹配,停止正式生产: {anchor}")


def validate_style_1_2_subject(subject: str) -> None:
    hits = [term for term in STYLE_INJECTION_TERMS if term in subject]
    pattern_hits = ["受控画风表达"] if any(pattern.search(subject) for pattern in STYLE_INJECTION_PATTERNS) else []
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
        payload["style_contract"] = "family-crayon-card-v2"
        references: list[dict[str, str]] = [
            {
                "path": str(anchor),
                "role": "style-only",
                "priority": "primary-visual-truth",
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
        payload["workflow"] = {
            "final_output_stage": "scribble-correction",
            "stages": [
                {
                    "id": "base-generation",
                    "operation": "generate",
                    "prompt_source": "prompt",
                    "references_source": "references",
                    "output_status": "intermediate-only",
                },
                {
                    "id": "scribble-correction",
                    "operation": "edit",
                    "required": True,
                    "prompt": STYLE_1_2_SCRIBBLE_CORRECTION_PROMPT,
                    "references": [
                        {
                            "input_index": 1,
                            "role": "edit-target",
                            "source": "base-generation.output",
                        },
                        {
                            "input_index": 2,
                            "role": "style-only",
                            "path": str(anchor),
                        },
                    ],
                    "must_preserve": (
                        "characters, faces, poses, actions, composition, object count, "
                        "outlines, colors, white background, and framing"
                    ),
                },
            ],
        }
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
