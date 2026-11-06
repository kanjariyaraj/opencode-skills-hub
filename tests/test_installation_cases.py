import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASES = json.loads((ROOT / "tests" / "installation" / "cases.json").read_text())["cases"]
CATALOG_IDS = set()
for path in (ROOT / "catalog").glob("*.json"):
    if path.name in {"collections.json", "index.json"}:
        continue
    CATALOG_IDS.update(r["id"] for r in json.loads(path.read_text())["resources"])


class InstallationCaseTests(unittest.TestCase):
    def test_case_ids_are_unique(self):
        ids = [case["id"] for case in CASES]
        self.assertEqual(len(ids), len(set(ids)))

    def test_every_case_is_pinned_and_bounded(self):
        for case in CASES:
            self.assertTrue(case.get("pinned"), case["id"])
            self.assertGreater(case.get("timeout_seconds", 0), 0, case["id"])
            self.assertLessEqual(case["timeout_seconds"], 900, case["id"])

    def test_resource_ids_exist(self):
        for case in CASES:
            if case.get("resource_id"):
                self.assertIn(case["resource_id"], CATALOG_IDS, case["id"])

    def test_no_privileged_or_host_mount_flags(self):
        for case in CASES:
            script = case["script"]
            self.assertNotIn("--privileged", script, case["id"])
            self.assertNotIn("/home/raj", script, case["id"])
            self.assertNotIn("~/.config/opencode", script, case["id"])


if __name__ == "__main__":
    unittest.main()
