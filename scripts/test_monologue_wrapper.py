#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


WRAPPER = Path(__file__).resolve().parent / "generate_monologue_card_with_codex.sh"
FAKE_TOOL = r'''
import json
import os
import sys
from pathlib import Path

tool = Path(sys.argv[0]).name
events = Path(os.environ["MONOLOGUE_TEST_EVENTS"])
with events.open("a", encoding="utf-8") as log:
    log.write(tool + ":" + sys.argv[1] + "\n")
if tool == "codex":
    if sys.argv[1:3] == ["features", "list"]:
        print("image_generation experimental true")
    else:
        directory = Path(sys.argv[sys.argv.index("-C") + 1])
        (directory / "out.png").write_bytes(b"test-output")
        if os.environ.get("MONOLOGUE_TEST_GENERATION_FAILURE"):
            raise SystemExit(1)
elif tool == "sips":
    output = Path(sys.argv[-1])
    output.write_bytes(output.read_bytes() + b"-resized")
elif tool == "bun":
    output = Path(sys.argv[2])
    if output.read_bytes() != b"test-output-resized":
        raise SystemExit("privacy audit must run after resizing")
    print(json.dumps([{"input": str(output), "output": str(output), "privacy": {
        "gpsPresent": bool(os.environ.get("MONOLOGUE_TEST_PRIVACY_FAILURE")),
        "sourceExifPresent": False,
        "requiredMacSourceXattrsPresent": [],
        "macSourceXattrsPresent": [],
    }}]))
'''


class MonologueWrapperTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workspace = tempfile.TemporaryDirectory(prefix="hand-drawn-wrapper-test-")
        self.root = Path(self.workspace.name)
        self.tools = self.root / "bin"
        self.tools.mkdir()
        for name in ("codex", "bun", "sips"):
            executable = self.tools / name
            executable.write_text(f"#!{sys.executable}\n" + FAKE_TOOL, encoding="utf-8")
            executable.chmod(0o755)
        self.privacy_script = self.root / "main.ts"
        self.privacy_script.write_text("// privacy-tool test entrypoint\n", encoding="utf-8")
        self.output = self.root / "card.png"
        self.events = self.root / "events.txt"
        self.environment = {**os.environ, "PATH": str(self.tools) + os.pathsep + os.environ["PATH"], "MONOLOGUE_TEST_EVENTS": str(self.events)}

    def tearDown(self) -> None:
        self.workspace.cleanup()

    def run_wrapper(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["bash", str(WRAPPER), *arguments], env=self.environment, capture_output=True, text=True)

    def generation_arguments(self) -> list[str]:
        return ["--text", "今天慢一点，也能走到想去的地方。", "--out", str(self.output), "--privacy-script", str(self.privacy_script)]

    def test_help_and_shell_syntax_need_no_generation(self) -> None:
        self.assertEqual(self.run_wrapper("--help").returncode, 0)
        self.assertEqual(subprocess.run(["bash", "-n", str(WRAPPER)], capture_output=True).returncode, 0)
        self.assertFalse(self.events.exists())

    def test_missing_argument_is_reported(self) -> None:
        result = self.run_wrapper("--text")
        self.assertEqual(result.returncode, 2)
        self.assertIn("缺少值", result.stderr)
        self.assertFalse(self.events.exists())

    def test_missing_privacy_skill_stops_before_generation(self) -> None:
        arguments = self.generation_arguments()
        arguments[-1] = str(self.root / "missing.ts")
        result = self.run_wrapper(*arguments)
        self.assertEqual(result.returncode, 3)
        self.assertIn("sweety-image-privacy 不可用", result.stderr)
        self.assertFalse(self.events.exists())
        self.assertFalse(self.output.exists())

    def test_success_preserves_resize_then_privacy_order_and_audit(self) -> None:
        result = self.run_wrapper(*self.generation_arguments())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.output.read_bytes(), b"test-output-resized")
        audit = json.loads(Path(str(self.output) + ".privacy.json").read_text())
        self.assertFalse(audit[0]["privacy"]["gpsPresent"])
        self.assertEqual(self.events.read_text().splitlines(), ["codex:features", "codex:exec", "sips:-z", "bun:" + str(self.privacy_script)])

    def test_failed_privacy_audit_preserves_existing_delivery(self) -> None:
        self.output.write_bytes(b"existing-delivery")
        self.environment["MONOLOGUE_TEST_PRIVACY_FAILURE"] = "1"
        result = self.run_wrapper(*self.generation_arguments())
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("隐私审计未通过", result.stderr)
        self.assertEqual(self.output.read_bytes(), b"existing-delivery")
        self.assertFalse(Path(str(self.output) + ".privacy.json").exists())

    def test_failed_generation_does_not_deliver_partial_file(self) -> None:
        self.environment["MONOLOGUE_TEST_GENERATION_FAILURE"] = "1"
        result = self.run_wrapper(*self.generation_arguments())
        self.assertEqual(result.returncode, 4)
        self.assertFalse(self.output.exists())
        self.assertNotIn("bun:", self.events.read_text())

    def test_metadata_bypass_is_rejected(self) -> None:
        result = self.run_wrapper("--keep-metadata")
        self.assertEqual(result.returncode, 2)
        self.assertFalse(self.events.exists())


if __name__ == "__main__":
    unittest.main()
