"""Structural tests for JSON schema files and catalog files."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "schemas"


class SchemaTests(unittest.TestCase):
    def test_schemas_are_valid_json(self):
        for path in sorted(SCHEMAS.glob("*.json")):
            with self.subTest(schema=path.name):
                payload = json.loads(path.read_text(encoding="utf-8"))
                self.assertIn("$schema", payload)
                self.assertEqual("object", payload.get("type"))

    def test_resource_schema_required_fields(self):
        schema = json.loads((SCHEMAS / "resource.schema.json").read_text(encoding="utf-8"))
        required = set(schema["required"])
        for field in ["id", "name", "type", "description", "primary_category", "source", "verification"]:
            self.assertIn(field, required)

    def test_catalog_files_match_resource_type(self):
        for path in sorted((ROOT / "catalog").glob("*.json")):
            if path.name in {"collections.json", "index.json"}:
                continue
            with self.subTest(catalog=path.name):
                payload = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual("1.0.0", payload["schema_version"])
                for resource in payload["resources"]:
                    self.assertEqual(payload["resource_type"], resource["type"])


if __name__ == "__main__":
    unittest.main()
