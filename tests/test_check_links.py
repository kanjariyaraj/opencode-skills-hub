"""Tests for scripts/check_links.py."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_links  # noqa: E402


class ExtractLinksTests(unittest.TestCase):
    def test_extracts_markdown_links_and_images(self):
        links = check_links.extract_links(
            "See [docs](docs/a.md) and ![img](assets/x.png) and <https://example.com>."
        )
        self.assertIn("docs/a.md", links)
        self.assertIn("assets/x.png", links)

    def test_ignores_plain_text(self):
        self.assertEqual([], check_links.extract_links("No links here."))


class LocalLinkTests(unittest.TestCase):
    def test_missing_local_link_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a.md").write_text("[missing](missing.md)\n", encoding="utf-8")
            broken = check_links.check_local(root)
            self.assertEqual(1, len(broken))
            self.assertIn("missing.md", broken[0])

    def test_existing_local_link_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a.md").write_text("[b](b.md)\n", encoding="utf-8")
            (root / "b.md").write_text("# B\n", encoding="utf-8")
            self.assertEqual([], check_links.check_local(root))

    def test_anchor_only_and_external_links_are_ignored(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a.md").write_text(
                "[top](#top)\n[web](https://example.com)\n[mail](mailto:x@example.com)\n",
                encoding="utf-8",
            )
            self.assertEqual([], check_links.check_local(root))

    def test_escaping_repository_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a.md").write_text("[escape](../../etc/passwd)\n", encoding="utf-8")
            broken = check_links.check_local(root)
            self.assertEqual(1, len(broken))
            self.assertIn("escapes repository", broken[0])

    def test_cli_local_mode_succeeds_on_repository(self):
        self.assertEqual(0, check_links.main(["--root", str(ROOT)]))


if __name__ == "__main__":
    unittest.main()
