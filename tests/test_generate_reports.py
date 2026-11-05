"""Tests for scripts/generate_reports.py."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import generate_reports as reports  # noqa: E402


class ReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.taxonomy, cls.resources, cls.collections, cls.raw = reports.load_data()

    def test_stats_contains_totals(self):
        text = reports.build_stats(self.taxonomy, self.resources, self.collections, self.raw)
        self.assertIn("# Catalog Statistics", text)
        self.assertIn(f"Catalogued resources: **{len(self.resources)}**", text)

    def test_missing_sources_lists_unresolved(self):
        text = reports.build_missing_sources(self.raw)
        unresolved = [entry for entry in self.raw if entry.get("resolution") != "VERIFIED"]
        self.assertIn(f"Unresolved raw entries: **{len(unresolved)}**", text)

    def test_licenses_marks_review_required(self):
        text = reports.build_licenses(self.resources)
        self.assertIn("# License Report", text)
        self.assertIn("Review required", text)

    def test_compatibility_lists_every_resource(self):
        text = reports.build_compatibility(self.resources)
        for resource in self.resources:
            self.assertIn(resource["name"], text)

    def test_security_report_includes_policy(self):
        text = reports.build_security(self.resources)
        self.assertIn("Authorization policy", text)
        self.assertIn("Restricted archive", text)

    def test_generated_reports_are_current(self):
        self.assertEqual(0, reports.main(["--check"]))


if __name__ == "__main__":
    unittest.main()
