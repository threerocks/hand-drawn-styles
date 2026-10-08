#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

import build_skill_package
import check_skill


ROOT = Path(__file__).resolve().parents[1]


class InstallationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workspace = tempfile.TemporaryDirectory(prefix="hand-drawn-package-test-")
        cls.archive = Path(cls.workspace.name) / "skill.zip"
        cls.package = build_skill_package.build_archive(cls.archive)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.workspace.cleanup()

    def test_dependency_check_detects_backtick_and_gallery_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "STYLES.md").write_text("查看 `examples/missing.png`。\n运行 `scripts/missing.py --out sample.png`。\n", encoding="utf-8")
            (root / "README.md").write_text('<img src="examples/gallery.png">\n', encoding="utf-8")
            failures = check_skill.check_document_dependencies(root)
        self.assertEqual(len(failures), 3)
        self.assertTrue(any("examples/missing.png" in failure for failure in failures))
        self.assertTrue(any("scripts/missing.py" in failure for failure in failures))

    def test_archive_excludes_development_assets_and_preserves_references(self) -> None:
        with zipfile.ZipFile(self.archive) as archive:
            names = archive.namelist()
            self.assertTrue(all(name.startswith("hand-drawn/") for name in names))
            self.assertFalse(any(part in name for name in names for part in ("/.git/", "/benchmarks/", "/artifacts/", "/__pycache__/")))
            self.assertFalse(any("monologue" in name or "style-21" in name for name in names))
            references = {reference for style in check_skill.render_prompt.list_styles() for reference in style["references"]}
            self.assertEqual(len(references), 5)
            for reference in references:
                with self.subTest(reference=reference):
                    self.assertEqual(archive.read(f"hand-drawn/{reference}"), (ROOT / reference).read_bytes())
            self.assertLess(self.archive.stat().st_size, build_skill_package.MAXIMUM_PACKAGE_BYTES)

    def test_installed_archive_exercises_all_styles_outside_checkout(self) -> None:
        report = build_skill_package.verify_archive(self.archive)
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["smoke_checked"], 21)
        self.assertTrue(all(style["status"] == "pass" for style in report["styles"]))

    def test_package_manifest_rejects_changed_and_missing_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "recipe.md").write_text("changed", encoding="utf-8")
            (root / "PACKAGE-MANIFEST.json").write_text(json.dumps({"format_version": 1, "files": {
                "recipe.md": {"sha256": hashlib.sha256(b"original").hexdigest()},
                "absent.md": {"sha256": hashlib.sha256(b"missing").hexdigest()},
            }}), encoding="utf-8")
            failures = check_skill.check_package_manifest(root)
        self.assertEqual(len(failures), 2)

    def test_verifier_rejects_paths_outside_installation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            archive = Path(temp_dir) / "bad.zip"
            with zipfile.ZipFile(archive, "w") as package:
                package.writestr("../outside.txt", b"invalid")
            with self.assertRaisesRegex(ValueError, "越界路径"):
                build_skill_package.verify_archive(archive)

    def test_installed_checker_reports_missing_reference(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            installation = Path(temp_dir)
            with zipfile.ZipFile(self.archive) as archive:
                archive.extractall(installation)
            root = installation / "hand-drawn"
            (root / "examples/13-paper-folk-musician.png").unlink()
            completed = subprocess.run([sys.executable, "-B", str(root / "scripts/check_skill.py"), "--json"], cwd=installation, capture_output=True, text=True)
        self.assertEqual(completed.returncode, 2)
        report = json.loads(completed.stdout)
        self.assertEqual(report["smoke_checked"], 0)
        self.assertTrue(any("13-paper-folk-musician.png" in failure for failure in report["failures"]))

    def test_repeated_builds_have_identical_bytes(self) -> None:
        second = Path(self.workspace.name) / "second.zip"
        build_skill_package.build_archive(second)
        self.assertEqual(self.archive.read_bytes(), second.read_bytes())


if __name__ == "__main__":
    unittest.main()
