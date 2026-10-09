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

import hosted_images


ROOT = Path(__file__).resolve().parents[1]
STYLES_PATH = ROOT / "STYLES.md"
PLACEHOLDER_PATTERN = re.compile(r"【([A-Za-z_\u3400-\u9fff][A-Za-z0-9_\u3400-\u9fff]*)】")
EMPTY_PARAMETER_NAMES = {"胡茬", "背景元素"}
STYLE_ALIASES = {
    "xkcd": "1",
    "stickman": "1",
    "minimal-line": "1",
    "极简线条": "1",
    "火柴人": "1",
    "crayon": "2",
    "kid-crayon": "2",
    "蜡笔童涂": "2",
    "ghibli": "3",
    "吉卜力": "3",
    "吉卜力风": "3",
    "rawkid": "3.1",
    "kid-scrawl": "3.1",
    "stick-kid": "3.1",
    "family-crayon-card": "3.1",
    "parent-child-crayon": "3.1",
    "submission-crayon": "3.1",
    "亲子手绘": "3.1",
    "家庭蜡笔画": "3.1",
    "亲子蜡笔故事": "3.1",
    "亲子投稿蜡笔故事卡": "3.1",
    "家庭投稿蜡笔卡": "3.1",
    "蜡笔童涂-潦草自画版": "3.1",
    "蜡笔童涂潦草版": "3.1",
    "潦草自画版": "3.1",
    "bean": "4",
    "blob": "4",
    "小豆人": "4",
    "小豆人涂鸦信息图": "4",
    "ms-paint": "5",
    "bad-doodle": "5",
    "ugly": "5",
    "ms paint": "5",
    "scribble": "6",
    "pen-scribble": "6",
    "ballpoint": "6",
    "圆珠笔": "6",
    "real-crayon": "7",
    "crayon-photo": "7",
    "蜡笔实拍": "7",
    "ink-wash": "8",
    "ink": "8",
    "shuimo": "8",
    "chinese-painting": "8",
    "水墨": "8",
    "pixel": "9",
    "pixel-art": "9",
    "8-bit": "9",
    "16-bit": "9",
    "像素": "9",
    "emo-sketch": "10",
    "story-sketch": "10",
    "watercolor-sketch": "10",
    "light-watercolor": "10",
    "情绪叙事": "10",
    "淡彩速写": "10",
    "retro-concept": "11",
    "mid-century": "11",
    "concept-art": "11",
    "gouache-concept": "11",
    "二维水彩": "11",
    "sunlit-storybook": "12",
    "vis-dev": "12",
    "storybook-visdev": "12",
    "暖光童画": "12",
    "paper-folk": "13",
    "papercraft": "13",
    "nordic-papercraft": "13",
    "paper-sculpture": "13",
    "quilling": "13",
    "北欧纸雕": "13",
    "剪纸民俗": "13",
    "nordic-storybook": "14",
    "scandi-gouache": "14",
    "scandinavian-storybook": "14",
    "soft-gouache": "14",
    "北欧绘本水粉": "14",
    "softnose": "15",
    "softnose-vinyl": "15",
    "bignose-toy": "15",
    "vinyl-toy": "15",
    "art-toy": "15",
    "大鼻软偶": "15",
    "gouache-spotlight": "16",
    "spotlight-gouache": "16",
    "character-spotlight": "16",
    "聚光水粉立绘": "16",
    "inked-storybook": "17",
    "ink-storybook": "17",
    "sketch-storybook": "17",
    "storybook-ink": "17",
    "墨线绘本": "17",
    "warm-flat-storybook": "18",
    "flat-storybook": "18",
    "geometric-storybook": "18",
    "warm-flat": "18",
    "暖色扁平绘本": "18",
    "roundhead-redline": "19",
    "redline-roundhead": "19",
    "graphite-redline": "19",
    "圆头红线": "19",
    "圆头红线极简童画": "19",
    "黑红白圆头童画": "19",
    "warm-yellow-ink-story": "20",
    "yellow-ink-story": "20",
    "mustard-ink-story": "20",
    "暖黄墨线": "20",
    "暖黄墨线情绪小剧场": "20",
}

STYLE_3_1_ANCHOR_PIXEL_SHA256 = "1ae67d0088d58f2527ae81aa05d8453ce1ccc9d4614342c0bb1ab71a5e4895cd"
STYLE_3_1_ANCHOR_SIZE = (1086, 1448)
STYLE_19_ANCHOR_PIXEL_SHA256 = "5170a941b4222be7c4acd13eb83b87689231ade46ac5db35a957632676efedfa"
STYLE_19_ANCHOR_SIZE = (1024, 1536)
STYLE_19_MODEL_SNAPSHOT = "gpt-image-2-2026-04-21"
STYLE_20_ANCHOR_PIXEL_SHA256 = "1190a2cc02cf6ccb0ab165ba2f5d80234544438f9653d0b17d918ca718fbe030"
STYLE_20_ANCHOR_SIZE = (1156, 1361)
STYLE_20_MODEL_SNAPSHOT = "gpt-image-2-2026-04-21"
STYLE_3_1_SCRIBBLE_CORRECTION_PROMPT = """Image 1 is the edit target. Image 2 is the approved style-only reference.
Change ONLY the crayon coloring marks inside and around the existing people, clothing, hair, furniture, books, and props in Image 1. Preserve the exact characters, faces, poses, actions, composition, object count, outlines, colors, white background, and framing.
Rework the coloring to match Image 2's genuinely clumsy child scribbling: coarse blunt wax-crayon strokes with abrupt starts and stops; visibly mixed horizontal, vertical, diagonal, looping, zigzag and crossing directions inside the SAME color area; uneven pressure; isolated heavy clumps next to large untouched white-paper holes; some strokes stop far before the black outline and some overshoot well beyond it. Each color area must have a different scribble rhythm.
Critical: NO neat diagonal hatching, NO fine dense parallel lines, NO even spacing, NO uniform coverage, NO repeated digital crayon texture. Make the coloring obviously messier, coarser, patchier, emptier and more misregistered than Image 1. Do not add text or new objects."""
STYLE_3_1_SCRIBBLE_CHAOS_PROMPT = """Image 1 is the edit target after the first scribble correction. Image 2 is the only approved style reference.
Perform a second, stricter correction on CRAYON COLORING MARKS ONLY. Preserve Image 1 exactly in characters, faces, expressions, poses, gestures, composition, object count, black outlines, existing color choices, white background, and framing.
The remaining coloring is still too neat wherever it forms fine, dense, or consistently diagonal hatching. Replace those ordered areas with Image 2's clumsy family scribbling, not a digital crayon texture.
For EACH color area, use a SMALL NUMBER of much thicker blunt wax-crayon strokes with visibly different lengths and pressure. Break the area into disconnected bouts: horizontal rubs, a vertical stab, an abrupt diagonal, a loop, a zigzag, and crossing retraced strokes, without repeating a sequence. Leave 35-55% of the white paper clearly untouched in irregular LARGE holes, including holes that reach the black outline. Put heavy opaque clumps directly beside totally blank areas. Many strokes must stop far before the boundary; several isolated strokes must overshoot far outside it. Adjacent color areas must have obviously different stroke direction and density.
Critical failure conditions: NO fine pencil-like hatch marks; NO field of mostly parallel diagonals; NO even spacing; NO uniform coverage; NO repeated texture; NO tidy edge-following; NO tiny evenly distributed white gaps. Make the result substantially rougher, emptier, coarser, more asymmetrical, and more accidentally misregistered than Image 1. Do not change any clothing or object color. Do not add text, symbols, objects, shadows, paper texture, or scenery."""
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
    normalized = value.strip().lower()
    if normalized in STYLE_ALIASES:
        return STYLE_ALIASES[normalized]
    for style_id, section in load_style_sections().items():
        heading = section.splitlines()[0]
        name = re.sub(r"^## \d+(?:\.\d+)?\.?\s+", "", heading)
        if normalized in {name.lower(), re.split(r"[（(]", name)[0].strip().lower()}:
            return style_id
    return value.strip()


def load_style_sections() -> dict[str, str]:
    source = STYLES_PATH.read_text(encoding="utf-8")
    headings = list(re.finditer(r"^## .+$", source, re.MULTILINE))
    sections: dict[str, str] = {}
    for index, heading in enumerate(headings):
        identity = re.match(r"## (\d+(?:\.\d+)?)\.?\s+", heading.group())
        if identity is None:
            continue
        style_id = identity.group(1)
        if style_id in sections:
            raise ValueError(f"STYLES.md 中画风编号重复: {style_id}")
        end = headings[index + 1].start() if index + 1 < len(headings) else len(source)
        sections[style_id] = source[heading.start():end]
    return sections


def extract_template(style_id: str) -> str:
    section = load_style_sections().get(style_id, "")
    templates = re.findall(r"^```(?:\w+)?[ \t]*\n(.*?)^```[ \t]*$", section, re.MULTILINE | re.DOTALL)
    if len(templates) != 1:
        raise ValueError(f"STYLES.md 中不存在画风 {style_id} 的代码块配方")
    return templates[0].strip()


def list_styles() -> list[dict[str, object]]:
    catalog = []
    for style_id, section in sorted(load_style_sections().items(), key=lambda pair: tuple(map(int, pair[0].split(".")))):
        name = re.sub(r"^## \d+(?:\.\d+)?\.?\s+", "", section.splitlines()[0])
        references = style_reference_urls(style_id)
        catalog.append({
            "style_id": style_id,
            "name": name,
            "aliases": sorted(alias for alias, target in STYLE_ALIASES.items() if target == style_id),
            "parameters": sorted(set(PLACEHOLDER_PATTERN.findall(extract_template(style_id)))),
            "references": references,
        })
    return catalog


def style_reference_urls(style_id: str) -> list[str]:
    section = load_style_sections().get(style_id, "")
    return sorted(set(re.findall(r"https://[^\s`<>\)\"']+\.(?:png|jpg|jpeg|webp)", section)))


def hosted_image_reference(key: str) -> dict[str, str]:
    record = hosted_images.image_record(key)
    path = hosted_images.resolve_image(key)
    return {"path": str(path), "url": record["url"], "sha256": record["sha256"], "role": "style-only"}


def parse_vars(items: list[str]) -> dict[str, str]:
    values: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"--var 必须使用 名称=内容 格式: {item}")
        key, value = item.split("=", 1)
        key = key.strip().removeprefix("【").removesuffix("】")
        if not key or (not value.strip() and key not in EMPTY_PARAMETER_NAMES):
            raise ValueError(f"--var 的名称和内容都不能为空: {item}")
        values[key] = value if key == "背景元素" else value.strip()
    return values


def render(template: str, values: dict[str, str], aspect: str | None) -> str:
    expected = set(PLACEHOLDER_PATTERN.findall(template))
    unknown = sorted(set(values) - expected)
    if unknown:
        raise ValueError(f"配方不包含这些占位符: {', '.join(unknown)}")

    missing = sorted(expected - set(values))
    if missing:
        raise ValueError(f"缺少占位符: {', '.join(missing)}")

    # Substitute template parameters once; bracketed user text is literal content.
    output = PLACEHOLDER_PATTERN.sub(lambda match: values[match.group(1)], template)

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


def decode_png_pixel_bytes(path: Path) -> tuple[tuple[int, int], int, int, bytes]:
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
    return (width, height), color_type, bytes_per_pixel, b"".join(rows)


def png_pixel_sha256(path: Path) -> tuple[tuple[int, int], str]:
    size, _, _, pixel_bytes = decode_png_pixel_bytes(path)
    return size, hashlib.sha256(pixel_bytes).hexdigest()


def png_size(path: Path) -> tuple[int, int]:
    chunks = png_chunks(path)
    ihdr_chunks = [chunk for chunk_type, chunk in chunks if chunk_type == b"IHDR"]
    if len(ihdr_chunks) != 1 or len(ihdr_chunks[0]) != 13:
        raise ValueError(f"参考图 PNG 缺少有效 IHDR: {path}")
    width, height = struct.unpack(">II", ihdr_chunks[0][:8])
    return width, height


def validate_style_3_1_anchor(anchor: Path) -> None:
    if not anchor.is_file():
        raise ValueError(f"画风 3.1 锚点不可用,停止正式生产: {anchor}")
    size, digest = png_pixel_sha256(anchor)
    if size != STYLE_3_1_ANCHOR_SIZE:
        raise ValueError(f"画风 3.1 锚点尺寸不匹配,停止正式生产: {anchor}")
    if digest != STYLE_3_1_ANCHOR_PIXEL_SHA256:
        raise ValueError(f"画风 3.1 锚点像素不匹配,停止正式生产: {anchor}")


def validate_style_19_anchor(anchor: Path) -> None:
    if not anchor.is_file():
        raise ValueError(f"画风 19 锚点不可用,停止正式生产: {anchor}")
    size, digest = png_pixel_sha256(anchor)
    if size != STYLE_19_ANCHOR_SIZE:
        raise ValueError(f"画风 19 锚点尺寸不匹配,停止正式生产: {anchor}")
    if digest != STYLE_19_ANCHOR_PIXEL_SHA256:
        raise ValueError(f"画风 19 锚点像素不匹配,停止正式生产: {anchor}")


def validate_style_20_anchor(anchor: Path) -> None:
    if not anchor.is_file():
        raise ValueError(f"画风 20 锚点不可用,停止正式生产: {anchor}")
    size, digest = png_pixel_sha256(anchor)
    if size != STYLE_20_ANCHOR_SIZE:
        raise ValueError(f"画风 20 锚点尺寸不匹配,停止正式生产: {anchor}")
    if digest != STYLE_20_ANCHOR_PIXEL_SHA256:
        raise ValueError(f"画风 20 锚点像素不匹配,停止正式生产: {anchor}")


def validate_locked_style_subject(style_id: str, subject: str) -> None:
    hits = [term for term in STYLE_INJECTION_TERMS if term in subject]
    pattern_hits = ["受控画风表达"] if any(pattern.search(subject) for pattern in STYLE_INJECTION_PATTERNS) else []
    if hits or pattern_hits:
        raise ValueError(
            f"画风 {style_id} 的主体字段只能描述人物、动作、关系和道具;"
            f"检测到疑似业务画风注入: {', '.join(hits + pattern_hits)}"
        )


def validate_style_3_1_subject(subject: str) -> None:
    validate_locked_style_subject("3.1", subject)


def validate_style_19_subject(subject: str) -> None:
    validate_locked_style_subject("19", subject)


def validate_style_20_subject(subject: str) -> None:
    validate_locked_style_subject("20", subject)


def style_3_1_title_instruction(title: str) -> str:
    clean = title.strip()
    if not clean or "\n" in clean or "\r" in clean:
        raise ValueError("--title 必须是一行非空的准确标题原文")
    return (
        "画面顶部的大片留白区写手写中文标题,逐字为“"
        f"{clean}”;字像普通家长用粗黑笔写的,大小略不齐但准确清楚"
    )


def validate_style_3_1_text(text: str, expected_title_instruction: str | None) -> None:
    allowed = {"不加任何文字"}
    if expected_title_instruction:
        allowed.add(expected_title_instruction)
    if text not in allowed:
        raise ValueError(
            "画风 3.1 的文字输入只允许 --text '不加任何文字' 或独立 --title '准确标题原文';"
            "不得把画风或排版指令塞进 --text/--var 文字"
        )


def validate_style_19_text(text: str) -> None:
    if text != "No text anywhere.":
        raise ValueError(
            "画风 19 正式生产固定为无字底图;请使用 --text '不加任何文字'"
            "或省略 --text,标题需在独立排版流程处理"
        )


def validate_style_20_text(text: str) -> None:
    if text != "No text anywhere.":
        raise ValueError(
            "画风 20 正式生产固定为无字底图;请使用 --text '不加任何文字'"
            "或省略 --text,标题需在独立排版流程处理"
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
    if style_id not in {"3.1", "19", "20"}:
        for url in style_reference_urls(style_id):
            reference = hosted_image_reference(hosted_images.key_for_url(url))
            reference_path = Path(reference["path"])
            if reference_path.suffix.lower() == ".png":
                png_size(reference_path)
            payload["references"].append({
                **reference,
                "must_not_copy": "characters, objects, composition, or story content",
            })
        payload["references"].extend({"path": str(reference), "role": "character"} for reference in character_references)
    if style_id == "3.1":
        anchor_reference = hosted_image_reference("assets/style-3.1/anchor-family.png")
        anchor = Path(anchor_reference["path"])
        validate_style_3_1_anchor(anchor)
        payload["style_contract"] = "family-crayon-card-v3"
        references: list[dict[str, str]] = [
            {
                **anchor_reference,
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
            "final_output_stage": "scribble-chaos-correction",
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
                    "prompt": STYLE_3_1_SCRIBBLE_CORRECTION_PROMPT,
                    "references": [
                        {
                            "input_index": 1,
                            "role": "edit-target",
                            "source": "base-generation.output",
                        },
                        {
                            "input_index": 2,
                            **anchor_reference,
                        },
                    ],
                    "must_preserve": (
                        "characters, faces, poses, actions, composition, object count, "
                        "outlines, colors, white background, and framing"
                    ),
                    "output_status": "intermediate-only",
                },
                {
                    "id": "scribble-chaos-correction",
                    "operation": "edit",
                    "required": True,
                    "output_status": "final",
                    "prompt": STYLE_3_1_SCRIBBLE_CHAOS_PROMPT,
                    "references": [
                        {
                            "input_index": 1,
                            "role": "edit-target",
                            "source": "scribble-correction.output",
                        },
                        {
                            "input_index": 2,
                            **anchor_reference,
                        },
                    ],
                    "must_preserve": (
                        "characters, faces, expressions, poses, gestures, composition, "
                        "object count, black outlines, existing color choices, white "
                        "background, and framing"
                    ),
                },
            ],
        }
    elif style_id == "19":
        anchor_reference = hosted_image_reference("assets/style-19/anchor-roundhead-redline.png")
        anchor = Path(anchor_reference["path"])
        validate_style_19_anchor(anchor)
        payload["style_contract"] = "roundhead-redline-v1"
        references = [
            {
                **anchor_reference,
                "priority": "primary-visual-truth",
                "required_for": "every production image",
                "must_not_copy": "people, animal, clothing, props, positions, or actions",
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
        payload["model_requirements"] = {
            "provider": "OpenAI",
            "model_snapshot": STYLE_19_MODEL_SNAPSHOT,
            "snapshot_lock_required": True,
            "high_fidelity_image_input_required": True,
            "production_fallback": "fail-closed",
            "preview_fallback": "allowed only when explicitly labeled non-production",
        }
        payload["validation_evidence"] = {
            "candidate_generator": "Codex built-in image generation",
            "candidate_c2pa_software_agent": "gpt-image 2.0",
            "exact_candidate_snapshot_observed": False,
            "snapshot_requirement_basis": "current official OpenAI model catalog",
        }
        payload["acceptance_contract"] = {
            "minimum_score": 30,
            "maximum_score": 35,
            "dimensions": [
                "shape-language",
                "face-language",
                "gesture-language",
                "material-language",
                "palette",
                "negative-space",
                "originality-boundary",
            ],
            "hard_failures": [
                "title, logo, watermark, credited name, or poster layout",
                "red-and-white striped shirt combined with black shorts",
                "commercial vector, generic cute storybook, chibi, anime, 3D, or realism",
                "uniform thick outline, smooth gradient, or airbrushed blush",
                "filled background, more than two props, perspective floor, or cast-shadow system",
                "any main hue outside near-white, graphite gray, charcoal black, and coral red",
                "clean digital outline without visible graphite pressure variation",
            ],
        }
        payload["workflow"] = {
            "final_output_stage": "style-contract-check",
            "stages": [
                {
                    "id": "base-generation",
                    "operation": "generate",
                    "prompt_source": "prompt",
                    "references_source": "references",
                    "output_status": "candidate-only",
                },
                {
                    "id": "style-contract-check",
                    "operation": "validate",
                    "required": True,
                    "acceptance_source": "acceptance_contract",
                    "input_source": "base-generation.output",
                    "pass_status": "final",
                    "fail_status": "rejected",
                },
            ],
        }
    elif style_id == "20":
        anchor_reference = hosted_image_reference("assets/style-20/anchor-warm-yellow-ink-story.png")
        anchor = Path(anchor_reference["path"])
        validate_style_20_anchor(anchor)
        payload["style_contract"] = "warm-yellow-ink-story-v3"
        references = [
            {
                **anchor_reference,
                "priority": "primary-visual-truth",
                "required_for": "every production image",
                "must_not_copy": "people, animal, hair, clothing, props, positions, or actions",
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
        payload["model_requirements"] = {
            "provider": "OpenAI",
            "model_snapshot": STYLE_20_MODEL_SNAPSHOT,
            "snapshot_lock_required": True,
            "high_fidelity_image_input_required": True,
            "production_fallback": "fail-closed",
            "preview_fallback": "allowed only when explicitly labeled non-production",
        }
        payload["validation_evidence"] = {
            "candidate_generator": "Codex built-in image generation",
            "candidate_c2pa_software_agent": "gpt-image 2.0",
            "exact_candidate_snapshot_observed": False,
            "snapshot_requirement_basis": "current official OpenAI model catalog",
        }
        payload["acceptance_contract"] = {
            "minimum_score": 34,
            "maximum_score": 40,
            "dimensions": [
                "shape-language",
                "face-language",
                "line-material",
                "directional-black-hatching",
                "mustard-yellow-material",
                "negative-space",
                "single-action-storytelling",
                "originality-boundary",
            ],
            "hard_failures": [
                "title, logo, watermark, account name, credited name, or copied caption",
                "recognizable supplied character, paired yellow hoodies, or copied composition",
                "commercial vector, generic cute storybook, chibi, anime, 3D, or realism",
                "uniform thick outline or smooth solid-black hair and lower garments",
                "fluorescent yellow, large blue or purple area, gradient, or colored background",
                "filled background, complete room or landscape, or more than two props",
                "long realistic anatomy, oversized or anatomically articulated hands, detailed shoes, repeated garment stripes, or decorative stitching",
                "missing warm-white dominance, dry ink pressure variation, or readable single action",
            ],
        }
        payload["workflow"] = {
            "final_output_stage": "style-contract-check",
            "stages": [
                {
                    "id": "base-generation",
                    "operation": "generate",
                    "prompt_source": "prompt",
                    "references_source": "references",
                    "output_status": "final-candidate",
                },
                {
                    "id": "style-contract-check",
                    "operation": "validate",
                    "required": True,
                    "input_source": "base-generation.output",
                    "acceptance_source": "acceptance_contract",
                    "validator": {
                        "command": [
                            "python3",
                            str(ROOT / "scripts/validate_style_20_asset.py"),
                            "--image",
                            "{candidate_path}",
                            "--source-image",
                            "{base_generation_path}",
                            "--scorecard",
                            "{scorecard_path}",
                        ],
                        "required_exit_code": 0,
                    },
                    "pass_status": "final",
                    "fail_status": "rejected",
                },
            ],
            "rejection_policy": "reject and regenerate from base-generation; do not repair a failed candidate by style-transfer editing",
        }
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="从 STYLES.md 原样提取配方、填占位符并输出最终 prompt。"
    )
    parser.add_argument("--style", help="画风编号、中文名称或已登记别名")
    parser.add_argument("--list", action="store_true", help="输出全部画风、别名、参数和参考图的 JSON 菜单")
    parser.add_argument("--subject", help="填入【主体】")
    parser.add_argument("--text", help="填入【文字】")
    parser.add_argument("--title", help="风格 3.1 的准确标题原文;渲染器负责生成固定文字指令")
    parser.add_argument("--aspect", help="可选画幅比例,例如 3:4")
    parser.add_argument(
        "--character-reference",
        action="append",
        default=[],
        metavar="PATH",
        help="可重复传入连续故事的角色参考图;不会替代锁定画风的 style-only 锚点",
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
        help="auto 对 3.1/19/20 输出正式 JSON、其他画风输出 text;json 含画风锚点或生成合同",
    )
    parser.add_argument(
        "--text-only-preview",
        action="store_true",
        help="只允许 3.1/19/20 的非生产预览显式输出纯 prompt;不得用于正式生图",
    )
    args = parser.parse_args()

    if args.list:
        try:
            print(json.dumps(list_styles(), ensure_ascii=False, indent=2))
        except (OSError, ValueError) as error:
            print(f"render_prompt: {error}", file=sys.stderr)
            return 2
        return 0
    if args.style is None:
        parser.error("必须提供 --style 或 --list")

    try:
        style_id = canonical_style_id(args.style)
        values = parse_vars(args.var)
        if args.title is not None and style_id != "3.1":
            raise ValueError("--title 只适用于画风 3.1;画风 19/20 的标题需走独立排版流程")
        if args.text is not None and args.title is not None:
            raise ValueError("--text 与 --title 不能同时使用")
        if args.subject is not None:
            values["主体"] = args.subject.strip()
        title_instruction = None
        if args.title is not None:
            title_instruction = style_3_1_title_instruction(args.title)
            values["文字"] = title_instruction
        if args.text is not None:
            values["文字"] = args.text.strip()
        if style_id == "3.1":
            validate_style_3_1_subject(values.get("主体", ""))
            validate_style_3_1_text(values.get("文字", ""), title_instruction)
        elif style_id == "19":
            validate_style_19_subject(values.get("主体", ""))
            if values.get("文字", "") in {"", "不加任何文字"}:
                values["文字"] = "No text anywhere."
            validate_style_19_text(values["文字"])
        elif style_id == "20":
            validate_style_20_subject(values.get("主体", ""))
            if values.get("文字", "") in {"", "不加任何文字"}:
                values["文字"] = "No text anywhere."
            validate_style_20_text(values["文字"])
        if style_id == "12":
            scene = values.get("场景", "")
            if "【背景元素】" in scene:
                values["场景"] = scene.replace("【背景元素】", values.pop("背景元素", ""))
            elif "背景元素" in values:
                raise ValueError("画风 12 的场景没有【背景元素】参数;请在留白纸边档场景中使用")
        character_references = validate_character_references(args.character_reference)
        template = extract_template(style_id)
        prompt = render(template, values, args.aspect)
        locked_style_ids = {"3.1", "19", "20"}
        output_format = "json" if args.format == "auto" and style_id in locked_style_ids else args.format
        if output_format == "auto":
            output_format = "text"
        if style_id in locked_style_ids and output_format == "text" and not args.text_only_preview:
            raise ValueError(
                f"画风 {style_id} 正式生产不能只输出 prompt;请使用 --format json,"
                "或仅在非生产预览时显式加 --text-only-preview"
            )
        payload = build_payload(style_id, prompt, values, args.aspect, character_references) if output_format == "json" else None
    except (OSError, ValueError) as error:
        print(f"render_prompt: {error}", file=sys.stderr)
        return 2

    if output_format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
