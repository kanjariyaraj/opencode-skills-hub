#!/usr/bin/env python3
"""Validate the OpenCode Skills Hub catalog.

Checks:
  * required fields and enum values for every resource
  * resource type matches the catalog file
  * unique IDs and unique source URLs
  * categories exist in data/taxonomy.json
  * collection references resolve to known resources or collections
  * raw inventory entries use a known resolution value

Exit codes:
  0  all checks passed (warnings may be present)
  1  validation errors
  2  usage or IO error
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_DIR = ROOT / "catalog"
TAXONOMY_PATH = ROOT / "data" / "taxonomy.json"
RAW_INVENTORY_PATH = ROOT / "data" / "raw-inventory.json"

RESOURCE_TYPES = ["skill", "agent", "plugin", "mcp", "theme", "command", "rule", "hook", "provider"]
SOURCE_KINDS = ["github", "npm", "pypi", "docs", "website", "unknown"]
INSTALL_TEST = ["INSTALLATION_TESTED", "NOT_TESTED", "NOT_APPLICABLE", "BLOCKED"]
COMPAT = ["native", "compatible", "unknown", "incompatible"]
LICENSE_STATUS = ["LICENSE_VERIFIED", "LICENSE_REVIEW_REQUIRED", "NOASSERTION", "UNKNOWN"]
SECURITY_LEVELS = ["LOW RISK", "REVIEWED", "REVIEW REQUIRED", "HIGH RISK", "UNSAFE", "DEPRECATED"]
VERIFICATION_STATUS = [
    "DISCOVERED",
    "SOURCE_VERIFIED",
    "LICENSE_VERIFIED",
    "COMPATIBILITY_VERIFIED",
    "INSTALLATION_TESTED",
    "FUNCTIONAL_TESTED",
    "MAINTAINED",
    "UNAVAILABLE",
    "DUPLICATE",
    "UNMAINTAINED",
    "INCOMPATIBLE",
    "LICENSE_REVIEW_REQUIRED",
    "SECURITY_REVIEW_REQUIRED",
]
COLLECTION_KINDS = ["role", "skill-pack", "toolkit"]
RESOLUTIONS = ["VERIFIED", "SOURCE_UNRESOLVED", "NOT_FOUND", "RESTRICTED", "DUPLICATE"]

ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,63}$")
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")

RESOURCE_KEYS = {
    "$schema", "id", "name", "type", "description", "primary_category",
    "secondary_categories", "tags", "source", "install", "compatibility",
    "license", "security", "verification", "signals", "requires_alias_of",
}
SOURCE_KEYS = {"url", "kind", "documentation", "repository"}
INSTALL_KEYS = {"instructions", "requires_api_key", "tested", "notes"}
COMPAT_KEYS = {"opencode", "platforms", "dependencies"}
LICENSE_KEYS = {"spdx", "status"}
SECURITY_KEYS = {"level", "notes"}
VERIFICATION_KEYS = {"status", "date", "notes"}
SIGNAL_KEYS = {"github_stars_observed", "observed_at", "latest_release", "last_push"}
COLLECTION_KEYS = {"id", "name", "kind", "description", "audience", "categories", "resources", "source", "verification"}


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.counts: Counter = Counter()

    def error(self, where: str, message: str) -> None:
        self.errors.append(f"{where}: {message}")

    def warn(self, where: str, message: str) -> None:
        self.warnings.append(f"{where}: {message}")


def load_json(path: Path) -> object:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def is_nonempty_str(value: object) -> bool:
    return isinstance(value, str) and len(value.strip()) > 0


def check_keys(report: Report, where: str, obj: dict, allowed: set[str]) -> None:
    unknown = sorted(set(obj) - allowed)
    if unknown:
        report.error(where, f"unknown properties: {', '.join(unknown)}")


def check_string_list(report: Report, where: str, value: object, field: str, min_items: int = 0) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        report.error(where, f"{field} must be a list of strings")
        return []
    if len(value) < min_items:
        report.error(where, f"{field} must contain at least {min_items} item(s)")
    if len(set(value)) != len(value):
        report.error(where, f"{field} contains duplicates")
    return value


def validate_resource(report: Report, where: str, resource: dict, expected_type: str, category_ids: set[str]) -> None:
    check_keys(report, where, resource, RESOURCE_KEYS)

    for field in ["id", "name", "type", "description", "primary_category"]:
        if field not in resource:
            report.error(where, f"missing required field '{field}'")
    if report.errors and any(where in e for e in report.errors):
        # Keep validating when possible; the checks below guard on presence.
        pass

    rid = resource.get("id")
    if not is_nonempty_str(rid) or not ID_RE.match(rid):
        report.error(where, "id must match ^[a-z0-9][a-z0-9-]{1,63}$")
    if not is_nonempty_str(resource.get("name")) or len(resource.get("name", "")) > 120:
        report.error(where, "name must be a non-empty string of at most 120 characters")
    if resource.get("type") not in RESOURCE_TYPES:
        report.error(where, f"type must be one of {RESOURCE_TYPES}")
    elif resource.get("type") != expected_type:
        report.error(where, f"type '{resource.get('type')}' does not match catalog file type '{expected_type}'")
    desc = resource.get("description")
    if not is_nonempty_str(desc) or not 20 <= len(desc) <= 600:
        report.error(where, "description must be 20-600 characters")
    primary = resource.get("primary_category")
    if primary not in category_ids:
        report.error(where, f"primary_category '{primary}' is not in taxonomy")
    for category in check_string_list(report, where, resource.get("secondary_categories", []), "secondary_categories"):
        if category not in category_ids:
            report.error(where, f"secondary category '{category}' is not in taxonomy")
    tags = check_string_list(report, where, resource.get("tags"), "tags", min_items=1)
    for tag in tags:
        if not re.match(r"^[a-z0-9][a-z0-9+.#-]*$", tag):
            report.error(where, f"invalid tag '{tag}'")

    source = resource.get("source")
    if not isinstance(source, dict):
        report.error(where, "source must be an object")
        source = {}
    else:
        check_keys(report, where, source, SOURCE_KEYS)
        if source.get("kind") not in SOURCE_KINDS:
            report.error(where, f"source.kind must be one of {SOURCE_KINDS}")
        url = source.get("url")
        if not is_nonempty_str(url):
            report.error(where, "source.url is required")
        elif not (url.startswith("https://") or url.startswith("http://") or url == "SOURCE_URL_MISSING"):
            report.error(where, "source.url must be an http(s) URL or SOURCE_URL_MISSING")
        for optional in ["documentation"]:
            value = source.get(optional)
            if value is not None and not is_nonempty_str(value):
                report.error(where, f"source.{optional} must be a non-empty string or null")

    install = resource.get("install")
    if not isinstance(install, dict):
        report.error(where, "install must be an object")
    else:
        check_keys(report, where, install, INSTALL_KEYS)
        check_string_list(report, where, install.get("instructions"), "install.instructions")
        if not isinstance(install.get("requires_api_key"), bool):
            report.error(where, "install.requires_api_key must be a boolean")
        if install.get("tested") not in INSTALL_TEST:
            report.error(where, f"install.tested must be one of {INSTALL_TEST}")

    compatibility = resource.get("compatibility")
    if not isinstance(compatibility, dict):
        report.error(where, "compatibility must be an object")
    else:
        check_keys(report, where, compatibility, COMPAT_KEYS)
        if compatibility.get("opencode") not in COMPAT:
            report.error(where, f"compatibility.opencode must be one of {COMPAT}")
        check_string_list(report, where, compatibility.get("platforms"), "compatibility.platforms")
        check_string_list(report, where, compatibility.get("dependencies"), "compatibility.dependencies")

    license_obj = resource.get("license")
    if not isinstance(license_obj, dict):
        report.error(where, "license must be an object")
    else:
        check_keys(report, where, license_obj, LICENSE_KEYS)
        if not is_nonempty_str(license_obj.get("spdx")):
            report.error(where, "license.spdx is required")
        if license_obj.get("status") not in LICENSE_STATUS:
            report.error(where, f"license.status must be one of {LICENSE_STATUS}")

    security = resource.get("security")
    if not isinstance(security, dict):
        report.error(where, "security must be an object")
    else:
        check_keys(report, where, security, SECURITY_KEYS)
        if security.get("level") not in SECURITY_LEVELS:
            report.error(where, f"security.level must be one of {SECURITY_LEVELS}")
        if not is_nonempty_str(security.get("notes")):
            report.error(where, "security.notes is required")

    verification = resource.get("verification")
    if not isinstance(verification, dict):
        report.error(where, "verification must be an object")
    else:
        check_keys(report, where, verification, VERIFICATION_KEYS)
        statuses = check_string_list(report, where, verification.get("status"), "verification.status", min_items=1)
        for status in statuses:
            if status not in VERIFICATION_STATUS:
                report.error(where, f"unknown verification status '{status}'")
        if not is_nonempty_str(verification.get("date")) or not DATE_RE.match(verification.get("date", "")):
            report.error(where, "verification.date must be YYYY-MM-DD")
        if not is_nonempty_str(verification.get("notes")):
            report.error(where, "verification.notes is required")

    signals = resource.get("signals")
    if signals is not None:
        if not isinstance(signals, dict):
            report.error(where, "signals must be an object")
        else:
            check_keys(report, where, signals, SIGNAL_KEYS)
            stars = signals.get("github_stars_observed")
            if stars is not None and (not isinstance(stars, int) or stars < 0):
                report.error(where, "signals.github_stars_observed must be a non-negative integer or null")


def validate_collection(report: Report, where: str, collection: dict, category_ids: set[str]) -> None:
    check_keys(report, where, collection, COLLECTION_KEYS)
    collection_id = collection.get("id")
    if not is_nonempty_str(collection_id) or not ID_RE.match(collection_id):
        report.error(where, "id must match ^[a-z0-9][a-z0-9-]{1,63}$")
    if not is_nonempty_str(collection.get("name")):
        report.error(where, "name is required")
    if collection.get("kind") not in COLLECTION_KINDS:
        report.error(where, f"kind must be one of {COLLECTION_KINDS}")
    if not is_nonempty_str(collection.get("description")):
        report.error(where, "description is required")
    categories = check_string_list(report, where, collection.get("categories"), "categories", min_items=1)
    for category in categories:
        if category not in category_ids:
            report.error(where, f"category '{category}' is not in taxonomy")
    check_string_list(report, where, collection.get("resources"), "resources")
    source = collection.get("source")
    if source is not None:
        if not isinstance(source, dict):
            report.error(where, "source must be an object or null")
        else:
            check_keys(report, where, source, SOURCE_KEYS)
            if source.get("kind") not in SOURCE_KINDS:
                report.error(where, f"source.kind must be one of {SOURCE_KINDS}")
    verification = collection.get("verification")
    if not isinstance(verification, dict):
        report.error(where, "verification must be an object")
    else:
        check_keys(report, where, verification, VERIFICATION_KEYS)
        statuses = check_string_list(report, where, verification.get("status"), "verification.status", min_items=1)
        for status in statuses:
            if status not in VERIFICATION_STATUS:
                report.error(where, f"unknown verification status '{status}'")
        if not is_nonempty_str(verification.get("date")) or not DATE_RE.match(verification.get("date", "")):
            report.error(where, "verification.date must be YYYY-MM-DD")
        if not is_nonempty_str(verification.get("notes")):
            report.error(where, "verification.notes is required")


def validate_raw_inventory(report: Report, data: object) -> None:
    if not isinstance(data, dict) or not isinstance(data.get("entries"), list):
        report.error("data/raw-inventory.json", "must contain an 'entries' array")
        return
    seen: set[str] = set()
    for index, entry in enumerate(data["entries"]):
        where = f"data/raw-inventory.json[entries[{index}]]"
        if not isinstance(entry, dict):
            report.error(where, "entry must be an object")
            continue
        name = entry.get("name")
        if not is_nonempty_str(name):
            report.error(where, "name is required")
        elif name in seen:
            report.warn(where, f"duplicate raw inventory name '{name}'")
        seen.add(name or "")
        if entry.get("resolution") not in RESOLUTIONS:
            report.error(where, f"resolution must be one of {RESOLUTIONS}")


def run() -> Report:
    report = Report()
    taxonomy = load_json(TAXONOMY_PATH)
    category_ids = {category["id"] for category in taxonomy["categories"]}

    resource_ids: list[str] = []
    source_urls: defaultdict[str, list[str]] = defaultdict(list)
    all_resources: list[dict] = []

    for path in sorted(CATALOG_DIR.glob("*.json")):
        if path.name in {"collections.json", "index.json"}:
            continue
        document = load_json(path)
        where_file = f"catalog/{path.name}"
        if not isinstance(document, dict):
            report.error(where_file, "catalog file must be an object")
            continue
        if document.get("schema_version") != "1.0.0":
            report.error(where_file, "schema_version must be '1.0.0'")
        expected_type = document.get("resource_type")
        if expected_type not in RESOURCE_TYPES:
            report.error(where_file, f"resource_type must be one of {RESOURCE_TYPES}")
        resources = document.get("resources")
        if not isinstance(resources, list):
            report.error(where_file, "resources must be an array")
            continue
        report.counts["catalog_files"] += 1
        for index, resource in enumerate(resources):
            where = f"{where_file}[{index}]"
            if not isinstance(resource, dict):
                report.error(where, "resource must be an object")
                continue
            validate_resource(report, where, resource, expected_type, category_ids)
            all_resources.append(resource)
            if is_nonempty_str(resource.get("id")):
                resource_ids.append(resource["id"])
            url = (resource.get("source") or {}).get("url")
            if is_nonempty_str(url) and url != "SOURCE_URL_MISSING":
                source_urls[url].append(str(resource.get("id")))

    duplicates = {rid for rid, count in Counter(resource_ids).items() if count > 1}
    for rid in sorted(duplicates):
        report.error("catalog", f"duplicate resource id '{rid}'")

    for url, ids in sorted(source_urls.items()):
        if len(ids) > 1:
            report.warn("catalog", f"source URL shared by {', '.join(sorted(ids))}: {url}")

    collections_path = CATALOG_DIR / "collections.json"
    collection_ids: list[str] = []
    if collections_path.exists():
        document = load_json(collections_path)
        collections = document.get("collections") if isinstance(document, dict) else None
        if not isinstance(collections, list):
            report.error("catalog/collections.json", "collections must be an array")
        else:
            known = set(resource_ids)
            for index, collection in enumerate(collections):
                where = f"catalog/collections.json[{index}]"
                if not isinstance(collection, dict):
                    report.error(where, "collection must be an object")
                    continue
                validate_collection(report, where, collection, category_ids)
                if is_nonempty_str(collection.get("id")):
                    collection_ids.append(collection["id"])
                for reference in collection.get("resources") or []:
                    if isinstance(reference, str) and reference not in known and reference not in collection_ids:
                        report.error(where, f"unknown resource reference '{reference}'")
            known.update(collection_ids)
    duplicate_collections = {cid for cid, count in Counter(collection_ids).items() if count > 1}
    for cid in sorted(duplicate_collections):
        report.error("catalog/collections.json", f"duplicate collection id '{cid}'")

    if RAW_INVENTORY_PATH.exists():
        validate_raw_inventory(report, load_json(RAW_INVENTORY_PATH))

    report.counts["resources"] = len(resource_ids)
    report.counts["collections"] = len(collection_ids)
    report.counts["resource_ids_unique"] = len(set(resource_ids))
    report.counts["errors"] = len(report.errors)
    report.counts["warnings"] = len(report.warnings)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print a machine-readable report")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = parser.parse_args(argv)

    try:
        report = run()
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.strict and report.warnings:
        report.errors.extend(f"(strict) {warning}" for warning in report.warnings)

    if args.json:
        print(json.dumps({
            "ok": not report.errors,
            "counts": dict(report.counts),
            "errors": report.errors,
            "warnings": report.warnings,
        }, indent=2))
    else:
        for warning in report.warnings:
            print(f"WARN  {warning}")
        for error in report.errors:
            print(f"ERROR {error}")
        print(
            f"Checked {report.counts['resources']} resources and "
            f"{report.counts['collections']} collections: "
            f"{report.counts['errors']} error(s), {report.counts['warnings']} warning(s)."
        )

    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
