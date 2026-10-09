#!/usr/bin/env python3
"""Exercise remote image integrity, cache reuse, and complete-site packaging."""

from __future__ import annotations

import copy
import hashlib
import io
import json
import os
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch
from urllib.error import URLError

import hosted_images


class HostedImageTests(unittest.TestCase):
    def setUp(self) -> None:
        environment = patch.dict(os.environ, {"HAND_DRAWN_OFFLINE": "0"})
        environment.start()
        self.addCleanup(environment.stop)
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)
        self.cache = self.root / "cache"
        self.content = b"unchanged image bytes"
        self.key = "examples/sample.png"
        self.base_url = "https://gentle-starburst-99bd99.netlify.app/hand-drawn"
        self.record = {"url": self.base_url + "/" + self.key, "bytes": len(self.content), "sha256": hashlib.sha256(self.content).hexdigest()}
        self.manifest = {"format_version": 1, "base_url": self.base_url, "images": {self.key: self.record}}

    def image_module(self):
        return hosted_images

    def test_download_preserves_bytes_and_reuses_cache_without_network(self) -> None:
        module = self.image_module()
        with patch.object(module, "urlopen", return_value=io.BytesIO(self.content)) as download:
            path = module.resolve_image(self.key, manifest=self.manifest, cache_root=self.cache)
        self.assertEqual(download.call_count, 1)
        self.assertEqual(path.read_bytes(), self.content)
        self.assertTrue(path.is_relative_to(self.cache.resolve()))
        with patch.object(module, "urlopen", side_effect=AssertionError("缓存命中时不得联网")):
            self.assertEqual(module.resolve_image(self.key, manifest=self.manifest, cache_root=self.cache, offline=True), path)

    def test_corrupt_cache_is_replaced_only_by_verified_download(self) -> None:
        module = self.image_module()
        with patch.object(module, "urlopen", return_value=io.BytesIO(self.content)):
            path = module.resolve_image(self.key, manifest=self.manifest, cache_root=self.cache)
        path.write_bytes(b"damaged")
        with patch.object(module, "urlopen", return_value=io.BytesIO(self.content)):
            self.assertEqual(module.resolve_image(self.key, manifest=self.manifest, cache_root=self.cache).read_bytes(), self.content)

    def test_wrong_hash_and_size_never_enter_cache(self) -> None:
        module = self.image_module()
        for content in (b"x" * len(self.content), b"too short", self.content + b"extra"):
            with self.subTest(content=content):
                with patch.object(module, "urlopen", return_value=io.BytesIO(content)):
                    with self.assertRaisesRegex(ValueError, "校验失败"):
                        module.resolve_image(self.key, manifest=self.manifest, cache_root=self.cache)
                self.assertFalse(any(path.is_file() for path in self.cache.rglob("*")))

    def test_missing_offline_image_fails_without_request(self) -> None:
        module = self.image_module()
        with patch.object(module, "urlopen", side_effect=AssertionError("离线模式不得联网")):
            with self.assertRaisesRegex(ValueError, "离线.*缺少.*sample.png"):
                module.resolve_image(self.key, manifest=self.manifest, cache_root=self.cache, offline=True)

    def test_network_failure_is_actionable_and_leaves_no_partial_image(self) -> None:
        module = self.image_module()
        with patch.object(module, "urlopen", side_effect=URLError("unavailable")):
            with self.assertRaisesRegex(ValueError, "下载失败.*sample.png"):
                module.resolve_image(self.key, manifest=self.manifest, cache_root=self.cache)
        self.assertFalse(any(path.is_file() for path in self.cache.rglob("*")))

    def test_remote_verification_downloads_even_when_cache_is_valid(self) -> None:
        module = self.image_module()
        with patch.object(module, "urlopen", return_value=io.BytesIO(self.content)):
            module.resolve_image(self.key, manifest=self.manifest, cache_root=self.cache)
        with patch.object(module, "urlopen", return_value=io.BytesIO(b"wrong")):
            with self.assertRaisesRegex(ValueError, "校验失败"):
                module.verify_remote_image(self.key, manifest=self.manifest)

    def test_manifest_rejects_unsafe_paths_and_inconsistent_urls(self) -> None:
        module = self.image_module()
        for key, url in (("../outside.png", self.base_url + "/../outside.png"), ("/absolute.png", self.base_url + "/absolute.png"), ("examples/../outside.png", self.base_url + "/examples/../outside.png"), (self.key, "http://example.com/image.png"), (self.key, "https://other.example.com/image.png")):
            with self.subTest(key=key, url=url):
                manifest = copy.deepcopy(self.manifest)
                manifest["images"] = {key: {**self.record, "url": url}}
                path = self.root / "manifest.json"
                path.write_text(json.dumps(manifest))
                with self.assertRaises(ValueError):
                    module.load_manifest(path)

    def test_manifest_rejects_invalid_integrity_records(self) -> None:
        module = self.image_module()
        for changes in ({"sha256": "not-a-hash"}, {"bytes": -1}, {"bytes": True}, {"bytes": "24"}):
            with self.subTest(changes=changes):
                manifest = copy.deepcopy(self.manifest)
                manifest["images"][self.key].update(changes)
                path = self.root / "manifest.json"
                path.write_text(json.dumps(manifest))
                with self.assertRaises(ValueError):
                    module.load_manifest(path)

    def test_cache_environment_selects_writable_location(self) -> None:
        module = self.image_module()
        with patch.dict(os.environ, {"HAND_DRAWN_IMAGE_CACHE": str(self.cache), "HAND_DRAWN_OFFLINE": "1"}):
            with patch.object(module, "urlopen", side_effect=AssertionError("离线模式不得联网")):
                with self.assertRaisesRegex(ValueError, "离线"):
                    module.resolve_image(self.key, manifest=self.manifest)

    def test_registration_preserves_file_and_refuses_to_replace_existing_identity(self) -> None:
        module = self.image_module()
        source = self.root / "source.png"
        source.write_bytes(self.content)
        manifest_path = self.root / "images.json"
        manifest_path.write_text(json.dumps({"format_version": 1, "base_url": self.base_url, "images": {}}))
        module.register_image(self.key, source, manifest_path=manifest_path, cache_root=self.cache)
        self.assertEqual(module.load_manifest(manifest_path)["images"][self.key], self.record)
        self.assertEqual(source.read_bytes(), self.content)
        source.write_bytes(b"a different final image")
        with self.assertRaisesRegex(ValueError, "已存在.*新名称"):
            module.register_image(self.key, source, manifest_path=manifest_path, cache_root=self.cache)

    def test_site_archive_preserves_existing_pages_and_all_images(self) -> None:
        module = self.image_module()
        baseline = self.root / "previous-site.zip"
        with zipfile.ZipFile(baseline, "w") as archive:
            archive.writestr("index.html", b"Existing home page")
            archive.writestr("other/project.css", b"body {color: green}")
        output = self.root / "next-site.zip"
        with patch.object(module, "urlopen", return_value=io.BytesIO(self.content)):
            module.build_site_archive(baseline, output, manifest=self.manifest, cache_root=self.cache)
        with zipfile.ZipFile(output) as archive:
            self.assertEqual(archive.read("index.html"), b"Existing home page")
            self.assertEqual(archive.read("other/project.css"), b"body {color: green}")
            self.assertEqual(archive.read("hand-drawn/" + self.key), self.content)

    def test_site_archive_rejects_baseline_zip_with_parent_paths(self) -> None:
        module = self.image_module()
        baseline = self.root / "unsafe.zip"
        with zipfile.ZipFile(baseline, "w") as archive:
            archive.writestr("../escape.txt", b"unsafe")
        with self.assertRaisesRegex(ValueError, "越界路径"):
            module.build_site_archive(baseline, self.root / "next.zip", manifest=self.manifest, cache_root=self.cache)


if __name__ == "__main__":
    unittest.main()
