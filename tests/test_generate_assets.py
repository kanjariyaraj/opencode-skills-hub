"""Tests for scripts/generate_assets.py."""

from __future__ import annotations

import html
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import generate_assets as assets  # noqa: E402


class AssetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.taxonomy, cls.resources, cls.collections = assets.indexes.load_data()

    def test_outputs_cover_all_themes(self):
        outputs = assets.render_outputs()
        names = {path.name for path in outputs}
        self.assertEqual(
            {"banner-light.svg", "banner-dark.svg", "coverage-light.svg", "coverage-dark.svg"},
            names,
        )

    def test_banner_contains_counts_and_title(self):
        svg = assets.banner_svg("light", 32, 46, 18)
        self.assertIn("OpenCode Skills Hub", svg)
        self.assertIn("32 RESOURCES", svg)
        self.assertIn("46 COLLECTIONS", svg)
        self.assertIn("18 CATEGORIES", svg)

    def test_coverage_contains_every_category(self):
        counts = assets.Counter(resource["primary_category"] for resource in self.resources)
        ordered = sorted(
            self.taxonomy["categories"],
            key=lambda item: (-counts.get(item["id"], 0), item["label"].casefold()),
        )
        svg = assets.coverage_svg("dark", ordered, counts, "2026-11-05")
        for category in self.taxonomy["categories"]:
            self.assertIn(html.escape(category["label"]), svg)

    def test_coverage_is_sorted_by_count(self):
        counts = assets.Counter(resource["primary_category"] for resource in self.resources)
        ordered = sorted(
            self.taxonomy["categories"],
            key=lambda item: (-counts.get(item["id"], 0), item["label"].casefold()),
        )
        svg = assets.coverage_svg("light", ordered, counts, "2026-11-05")
        self.assertLess(svg.index("Software Development"), svg.index("Design &amp; UI/UX"))

    def test_output_is_deterministic(self):
        first = assets.render_outputs()
        second = assets.render_outputs()
        self.assertEqual(
            {path: content for path, content in first.items()},
            {path: content for path, content in second.items()},
        )

    def test_outputs_are_well_formed_xml(self):
        import xml.etree.ElementTree as element_tree

        for path, content in assets.render_outputs().items():
            element_tree.fromstring(content)


if __name__ == "__main__":
    unittest.main()
