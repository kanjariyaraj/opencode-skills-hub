"""Tests for scripts/query_catalog.py."""

from __future__ import annotations

import contextlib
import io
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import query_catalog as query  # noqa: E402


class QueryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _, cls.resources, _ = query.indexes.load_data()

    def test_filter_by_secondary_category(self):
        results = query.filter_resources(self.resources, categories=["image-generation"])
        self.assertTrue(results)
        self.assertTrue(
            any("image-generation" in resource.get("secondary_categories", []) for resource in results)
        )

    def test_filter_by_type(self):
        results = query.filter_resources(self.resources, types=["plugin"])
        self.assertTrue(results)
        self.assertTrue(all(resource["type"] == "plugin" for resource in results))

    def test_filter_by_verification_status(self):
        results = query.filter_resources(self.resources, statuses=["LICENSE_REVIEW_REQUIRED"])
        self.assertTrue(results)
        self.assertTrue(
            all(
                "LICENSE_REVIEW_REQUIRED" in resource["verification"]["status"]
                for resource in results
            )
        )

    def test_search_matches_tags(self):
        results = query.filter_resources(self.resources, search="ffmpeg")
        self.assertTrue(results)
        self.assertTrue(
            any("ffmpeg" in " ".join(resource.get("tags", [])).casefold() for resource in results)
        )

    def test_maintenance_filter(self):
        results = query.filter_resources(self.resources, maintenance="maintained")
        self.assertTrue(results)
        self.assertTrue(all("MAINTAINED" in r["verification"]["status"] for r in results))

    def test_sort_by_name(self):
        ordered = query.sort_resources(self.resources, "name")
        names = [resource["name"].casefold() for resource in ordered]
        self.assertEqual(sorted(names), names)

    def test_security_reverse_puts_high_risk_first(self):
        ordered = query.sort_resources(self.resources, "security", reverse=True)
        self.assertEqual("HIGH RISK", ordered[0]["security"]["level"])

    def test_json_render_strips_internal_keys(self):
        payload = json.loads(query.render_json(self.resources[:2]))
        self.assertEqual(2, payload["count"])
        for resource in payload["resources"]:
            self.assertFalse(any(key.startswith("_") for key in resource))

    def test_cli_limit_and_ids(self):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = query.main(["--type", "plugin", "--sort", "name", "--limit", "2", "--format", "ids"])
        self.assertEqual(0, code)
        self.assertEqual(2, len(buffer.getvalue().strip().splitlines()))

    def test_cli_rejects_unknown_sort(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as raised:
                query.main(["--sort", "not-a-field"])
        self.assertEqual(2, raised.exception.code)


if __name__ == "__main__":
    unittest.main()
