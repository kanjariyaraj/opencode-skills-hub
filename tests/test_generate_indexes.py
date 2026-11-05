"""Tests for scripts/generate_indexes.py."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import generate_indexes as indexes  # noqa: E402


class IndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.taxonomy, cls.resources, cls.collections = indexes.load_data()

    def test_counts_match_source_data(self):
        index = indexes.build_index(self.taxonomy, self.resources, self.collections)
        self.assertEqual(len(self.resources), index["counts"]["resources"])
        self.assertEqual(len(self.collections), index["counts"]["collections"])

    def test_index_is_deterministic(self):
        first = indexes.build_index(self.taxonomy, self.resources, self.collections)
        second = indexes.build_index(self.taxonomy, self.resources, self.collections)
        self.assertEqual(json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True))

    def test_internal_keys_are_not_exported(self):
        index = indexes.build_index(self.taxonomy, self.resources, self.collections)
        for resource in index["resources"]:
            self.assertFalse(any(key.startswith("_") for key in resource))

    def test_every_category_has_a_page(self):
        outputs = indexes.render_outputs()
        for category in self.taxonomy["categories"]:
            self.assertIn(indexes.CATEGORIES_DIR / f"{category['id']}.md", outputs)

    def test_every_collection_has_a_page(self):
        outputs = indexes.render_outputs()
        for collection in self.collections:
            self.assertIn(indexes.COLLECTIONS_DIR / f"{collection['id']}.md", outputs)

    def test_category_page_contains_related_links(self):
        category = next(item for item in self.taxonomy["categories"] if item["id"] == "software-development")
        page = indexes.build_category_page(category, self.resources, self.collections, self.taxonomy)
        self.assertIn("# Software Development", page)
        self.assertIn("Related categories", page)

    def test_generated_files_are_current(self):
        self.assertEqual(0, indexes.main(["--check"]))


if __name__ == "__main__":
    unittest.main()
