"""Tests for scripts/validate_catalog.py."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import validate_catalog as validator  # noqa: E402

CATEGORIES = {"software-development", "design-ui-ux", "cybersecurity"}


def valid_resource(**overrides):
    resource = {
        "id": "sample-skill",
        "name": "Sample Skill",
        "type": "skill",
        "description": "A factual description that is long enough to pass validation.",
        "primary_category": "software-development",
        "secondary_categories": ["design-ui-ux"],
        "tags": ["sample", "testing"],
        "source": {
            "url": "https://github.com/example/sample-skill",
            "kind": "github",
            "documentation": None,
            "repository": "example/sample-skill",
        },
        "install": {
            "instructions": ["Follow the upstream README."],
            "requires_api_key": False,
            "tested": "NOT_TESTED",
            "notes": "Not tested.",
        },
        "compatibility": {
            "opencode": "compatible",
            "platforms": ["linux"],
            "dependencies": [],
        },
        "license": {"spdx": "MIT", "status": "LICENSE_VERIFIED"},
        "security": {"level": "REVIEW REQUIRED", "notes": "Not audited."},
        "verification": {
            "status": ["SOURCE_VERIFIED", "LICENSE_VERIFIED"],
            "date": "2026-11-05",
            "notes": "Source and license confirmed.",
        },
    }
    resource.update(overrides)
    return resource


class ResourceValidationTests(unittest.TestCase):
    def test_valid_resource_passes(self):
        report = validator.Report()
        validator.validate_resource(report, "test", valid_resource(), "skill", CATEGORIES)
        self.assertEqual([], report.errors)

    def test_unknown_category_fails(self):
        report = validator.Report()
        validator.validate_resource(
            report, "test", valid_resource(primary_category="not-a-category"), "skill", CATEGORIES
        )
        self.assertTrue(any("primary_category" in error for error in report.errors))

    def test_type_mismatch_fails(self):
        report = validator.Report()
        validator.validate_resource(report, "test", valid_resource(), "plugin", CATEGORIES)
        self.assertTrue(any("does not match catalog file type" in error for error in report.errors))

    def test_unknown_property_fails(self):
        report = validator.Report()
        resource = valid_resource()
        resource["surprise"] = True
        validator.validate_resource(report, "test", resource, "skill", CATEGORIES)
        self.assertTrue(any("unknown properties" in error for error in report.errors))

    def test_missing_source_fails(self):
        report = validator.Report()
        resource = valid_resource()
        resource["source"] = {"kind": "github"}
        validator.validate_resource(report, "test", resource, "skill", CATEGORIES)
        self.assertTrue(any("source.url" in error for error in report.errors))

    def test_invalid_verification_date_fails(self):
        report = validator.Report()
        resource = valid_resource()
        resource["verification"] = {"status": ["SOURCE_VERIFIED"], "date": "05-11-2026", "notes": "x"}
        validator.validate_resource(report, "test", resource, "skill", CATEGORIES)
        self.assertTrue(any("verification.date" in error for error in report.errors))

    def test_installation_claim_is_an_enum(self):
        report = validator.Report()
        resource = valid_resource()
        resource["install"]["tested"] = "YES"
        validator.validate_resource(report, "test", resource, "skill", CATEGORIES)
        self.assertTrue(any("install.tested" in error for error in report.errors))

    def test_high_risk_is_allowed(self):
        report = validator.Report()
        resource = valid_resource(
            primary_category="cybersecurity",
            security={"level": "HIGH RISK", "notes": "Authorized targets only."},
        )
        validator.validate_resource(report, "test", resource, "skill", CATEGORIES)
        self.assertEqual([], report.errors)


class RepositoryValidationTests(unittest.TestCase):
    def test_repository_catalog_has_no_errors(self):
        report = validator.run()
        self.assertEqual([], report.errors)
        self.assertGreater(report.counts["resources"], 0)

    def test_cli_json_mode_succeeds(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_catalog.py"), "--json"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual([], payload["errors"])


class RawInventoryTests(unittest.TestCase):
    def test_known_resolution_values(self):
        payload = json.loads((ROOT / "data" / "raw-inventory.json").read_text(encoding="utf-8"))
        report = validator.Report()
        validator.validate_raw_inventory(report, payload)
        self.assertEqual([], report.errors)

    def test_bad_resolution_fails(self):
        report = validator.Report()
        validator.validate_raw_inventory(report, {"entries": [{"name": "x", "resolution": "MAYBE"}]})
        self.assertTrue(report.errors)


if __name__ == "__main__":
    unittest.main()
