#!/usr/bin/env python3

from __future__ import annotations

import json
import importlib.util
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "scripts/render_prompt.py"
SPEC = importlib.util.spec_from_file_location("render_prompt", RENDERER)
RENDER_PROMPT = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(RENDER_PROMPT)


class RenderPromptTests(unittest.TestCase):
    def run_renderer(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(RENDERER), *args],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_style_1_2_json_contains_required_anchor(self) -> None:
        result = self.run_renderer(
            "--style",
            "family-crayon-card",
            "--subject",
            "爸爸把零食袋放回柜子,男孩站在旁边看着",
            "--text",
            "不加任何文字",
            "--aspect",
            "3:4",
            "--format",
            "json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["style_id"], "1.2")
        self.assertEqual(payload["style_contract"], "family-crayon-card-v1")
        self.assertEqual(payload["references"][0]["role"], "style-only")
        self.assertEqual(payload["references"][0]["priority"], "primary-visual-truth")
        self.assertTrue(Path(payload["references"][0]["path"]).is_file())
        self.assertIn("画面内容:爸爸把零食袋放回柜子", payload["prompt"])
        self.assertIn("画幅比例:3:4。", payload["prompt"])
        self.assertNotIn("【主体】", payload["prompt"])
        self.assertNotIn("【文字】", payload["prompt"])
        self.assertEqual(payload["inputs"]["variables"]["主体"], "爸爸把零食袋放回柜子,男孩站在旁边看着")

    def test_parent_child_natural_language_alias_routes_to_style_1_2(self) -> None:
        result = self.run_renderer(
            "--style",
            "亲子手绘",
            "--subject",
            "妈妈坐着听女儿讲学校里的事",
            "--text",
            "不加任何文字",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["style_id"], "1.2")
        self.assertEqual(payload["references"][0]["priority"], "primary-visual-truth")

    def test_style_1_2_auto_defaults_to_formal_json(self) -> None:
        result = self.run_renderer(
            "--style",
            "1.2",
            "--subject",
            "妈妈牵着孩子走过一把歪倒的小椅子",
            "--text",
            "不加任何文字",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["references"][0]["role"], "style-only")

    def test_style_1_2_plain_text_requires_explicit_preview(self) -> None:
        result = self.run_renderer(
            "--style",
            "1.2",
            "--subject",
            "妈妈牵着孩子",
            "--text",
            "不加任何文字",
            "--format",
            "text",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("正式生产不能只输出 prompt", result.stderr)

    def test_style_1_2_rejects_style_terms_in_subject(self) -> None:
        result = self.run_renderer(
            "--style",
            "1.2",
            "--subject",
            "妈妈牵着孩子,统一粗黑轮廓并使用低饱和四色配色",
            "--text",
            "不加任何文字",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("疑似业务画风注入", result.stderr)

    def test_style_1_2_rejects_synonym_style_injection(self) -> None:
        result = self.run_renderer(
            "--style",
            "1.2",
            "--subject",
            "妈妈牵着孩子,外轮廓加粗,只用四种灰调颜色",
            "--text",
            "不加任何文字",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("疑似业务画风注入", result.stderr)

    def test_style_1_2_rejects_numeric_fill_defect_injection(self) -> None:
        injections = (
            "每块衣服都严格留白30%",
            "每块衣服都严格留白百分之三十",
            "每件衣服都空出三成白色",
            "每处涂色都超出边缘十分之一",
        )
        for injection in injections:
            with self.subTest(injection=injection):
                result = self.run_renderer(
                    "--style",
                    "1.2",
                    "--subject",
                    f"妈妈牵着孩子,{injection}",
                    "--text",
                    "不加任何文字",
                )
                self.assertEqual(result.returncode, 2)
                self.assertIn("疑似业务画风注入", result.stderr)

    def test_style_1_2_rejects_character_standardization_injection(self) -> None:
        injections = (
            "所有人的眼睛和脸型都按同一尺寸模板绘制",
            "衣服的蜡笔覆盖率统一定为七成",
            "每张都套用固定人物模板,姿势尽量对称规整",
            "所有越界色痕平均控制在两毫米",
        )
        for injection in injections:
            with self.subTest(injection=injection):
                result = self.run_renderer(
                    "--style",
                    "1.2",
                    "--subject",
                    f"妈妈牵着孩子,{injection}",
                    "--text",
                    "不加任何文字",
                )
                self.assertEqual(result.returncode, 2)
                self.assertIn("疑似业务画风注入", result.stderr)

    def test_style_1_2_rejects_freeform_text_instruction(self) -> None:
        result = self.run_renderer(
            "--style",
            "1.2",
            "--subject",
            "妈妈牵着孩子",
            "--text",
            "改成低饱和四色配色",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("只允许 --text '不加任何文字' 或独立 --title", result.stderr)

    def test_style_1_2_title_is_wrapped_by_renderer(self) -> None:
        result = self.run_renderer(
            "--style",
            "1.2",
            "--subject",
            "妈妈牵着孩子",
            "--title",
            "摔倒以后，妈妈先做什么？",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertIn("逐字为“摔倒以后，妈妈先做什么？”", payload["prompt"])

    def test_character_reference_is_appended_after_style_anchor(self) -> None:
        character_reference = ROOT / "assets/style-1.2/anchor-family.png"
        result = self.run_renderer(
            "--style",
            "1.2",
            "--subject",
            "妈妈蹲下帮男孩整理裤脚",
            "--text",
            "不加任何文字",
            "--character-reference",
            str(character_reference),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["references"][0]["role"], "style-only")
        self.assertEqual(payload["references"][1]["role"], "character")
        self.assertEqual(payload["references"][1]["must_not_replace"], "the style-only reference")

    def test_metadata_only_change_preserves_anchor_identity(self) -> None:
        original = ROOT / "assets/style-1.2/anchor-family.png"
        with tempfile.TemporaryDirectory() as temp_dir:
            candidate = Path(temp_dir) / "anchor.png"
            data = original.read_bytes()
            iend_offset = data.rfind(b"\x00\x00\x00\x00IEND")
            self.assertGreater(iend_offset, 0)
            chunk_type = b"tEXt"
            chunk_data = b"audit=metadata-only-change"
            metadata_chunk = (
                struct.pack(">I", len(chunk_data))
                + chunk_type
                + chunk_data
                + struct.pack(">I", zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF)
            )
            candidate.write_bytes(data[:iend_offset] + metadata_chunk + data[iend_offset:])
            self.assertNotEqual(candidate.read_bytes(), original.read_bytes())
            RENDER_PROMPT.validate_style_1_2_anchor(candidate)

    def test_modified_anchor_pixels_fail_closed(self) -> None:
        original = ROOT / "assets/style-1.2/anchor-family.png"
        with tempfile.TemporaryDirectory() as temp_dir:
            candidate = Path(temp_dir) / "anchor.png"
            data = bytearray(original.read_bytes())
            idat_offset = data.find(b"IDAT")
            self.assertGreater(idat_offset, 0)
            data[idat_offset + 8] ^= 1
            candidate.write_bytes(data)
            with self.assertRaisesRegex(ValueError, "PNG 校验失败|像素不匹配|像素数据损坏"):
                RENDER_PROMPT.validate_style_1_2_anchor(candidate)

    def test_missing_placeholder_fails_closed(self) -> None:
        result = self.run_renderer(
            "--style",
            "1.2",
            "--subject",
            "一位妈妈牵着孩子",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("只允许 --text '不加任何文字' 或独立 --title", result.stderr)

    def test_unknown_placeholder_is_rejected(self) -> None:
        result = self.run_renderer(
            "--style",
            "1.2",
            "--subject",
            "一位妈妈牵着孩子",
            "--text",
            "不加任何文字",
            "--var",
            "业务画风=再加粗线稿",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("配方不包含这些占位符", result.stderr)


if __name__ == "__main__":
    unittest.main()
