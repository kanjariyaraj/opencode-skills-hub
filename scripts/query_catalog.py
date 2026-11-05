#!/usr/bin/env python3
"""Filter, sort and print catalog resources.

Usage:
  python3 scripts/query_catalog.py --category design-ui-ux --sort name
  python3 scripts/query_catalog.py --type plugin --sort security --reverse
  python3 scripts/query_catalog.py --search design --format json
  python3 scripts/query_catalog.py --license LICENSE_REVIEW_REQUIRED

Filters combine with AND. Repeated values within one filter combine with OR.

Exit codes:
  0  results printed
  2  usage or IO error
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_indexes as indexes  # noqa: E402

SORT_FIELDS = [
    "name",
    "id",
    "type",
    "category",
    "license",
    "security",
    "verification",
    "source",
    "last-push",
]

SECURITY_ORDER = {
    "LOW RISK": 0,
    "REVIEWED": 1,
    "REVIEW REQUIRED": 2,
    "HIGH RISK": 3,
    "UNSAFE": 4,
    "DEPRECATED": 5,
}

VERIFICATION_STATUSES = [
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

LICENSE_STATUSES = [
    "LICENSE_VERIFIED",
    "LICENSE_REVIEW_REQUIRED",
    "NOASSERTION",
    "UNKNOWN",
]

SOURCE_KINDS = ["github", "npm", "pypi", "website", "docs", "unknown"]


def _name(resource: dict) -> str:
    return str(resource.get("name") or resource.get("id") or "").casefold()


def _security_rank(resource: dict) -> int:
    level = (resource.get("security") or {}).get("level", "REVIEW REQUIRED")
    return SECURITY_ORDER.get(level, len(SECURITY_ORDER))


def _last_push(resource: dict) -> str:
    value = (resource.get("signals") or {}).get("last_push")
    return value or "0000-00-00T00:00:00Z"


SORT_KEYS = {
    "name": _name,
    "id": lambda resource: str(resource.get("id", "")),
    "type": lambda resource: (
        indexes.TYPE_ORDER.index(resource["type"])
        if resource.get("type") in indexes.TYPE_ORDER
        else len(indexes.TYPE_ORDER)
    ),
    "category": lambda resource: (str(resource.get("primary_category", "")), _name(resource)),
    "license": lambda resource: (str((resource.get("license") or {}).get("status", "")), _name(resource)),
    "security": lambda resource: (_security_rank(resource), _name(resource)),
    "verification": lambda resource: (indexes.status_text(resource), _name(resource)),
    "source": lambda resource: (str((resource.get("source") or {}).get("kind", "")), _name(resource)),
    "last-push": lambda resource: (_last_push(resource), _name(resource)),
}


def filter_resources(
    resources: list[dict],
    *,
    categories: list[str] | None = None,
    types: list[str] | None = None,
    statuses: list[str] | None = None,
    security: list[str] | None = None,
    licenses: list[str] | None = None,
    source_kinds: list[str] | None = None,
    maintenance: str = "any",
    search: str | None = None,
) -> list[dict]:
    categories = categories or []
    types = types or []
    statuses = statuses or []
    security = security or []
    licenses = licenses or []
    source_kinds = source_kinds or []
    needle = (search or "").casefold().strip()

    result = []
    for resource in resources:
        primary = resource.get("primary_category")
        secondary = resource.get("secondary_categories", [])
        resource_statuses = (resource.get("verification") or {}).get("status", [])
        license_status = (resource.get("license") or {}).get("status")
        security_level = (resource.get("security") or {}).get("level")
        source_kind = (resource.get("source") or {}).get("kind")

        if categories and primary not in categories and not set(secondary) & set(categories):
            continue
        if types and resource.get("type") not in types:
            continue
        if statuses and not set(resource_statuses) & set(statuses):
            continue
        if security and security_level not in security:
            continue
        if licenses and license_status not in licenses:
            continue
        if source_kinds and source_kind not in source_kinds:
            continue
        if maintenance == "maintained" and "MAINTAINED" not in resource_statuses:
            continue
        if maintenance == "unmaintained" and "UNMAINTAINED" not in resource_statuses:
            continue
        if needle:
            haystack = " ".join(
                [
                    str(resource.get("id", "")),
                    str(resource.get("name", "")),
                    str(resource.get("description", "")),
                    " ".join(str(tag) for tag in resource.get("tags", [])),
                ]
            ).casefold()
            if needle not in haystack:
                continue
        result.append(resource)
    return result


def sort_resources(resources: list[dict], field: str, reverse: bool = False) -> list[dict]:
    return sorted(resources, key=SORT_KEYS[field], reverse=reverse)


def _source_url(resource: dict) -> str:
    return str((resource.get("source") or {}).get("url") or "")


def render_table(resources: list[dict]) -> str:
    lines = [
        "| ID | Name | Type | Category | License | Security | Verification |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for resource in resources:
        name = indexes.md_escape(resource.get("name", resource.get("id", "")))
        url = _source_url(resource)
        linked = f"[{name}]({url})" if url.startswith(("http://", "https://")) else name
        license_obj = resource.get("license") or {}
        security = (resource.get("security") or {}).get("level", "")
        lines.append(
            f"| {indexes.md_escape(resource.get('id', ''))} | {linked} | "
            f"{indexes.md_escape(resource.get('type', ''))} | "
            f"{indexes.md_escape(resource.get('primary_category', ''))} | "
            f"{indexes.md_escape(license_obj.get('status', ''))} | "
            f"{indexes.md_escape(security)} | {indexes.md_escape(indexes.status_text(resource))} |"
        )
    return "\n".join(lines)


def render_json(resources: list[dict]) -> str:
    clean = [{key: value for key, value in resource.items() if not key.startswith("_")} for resource in resources]
    return json.dumps({"count": len(clean), "resources": clean}, indent=2) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--category", action="append", metavar="ID", help="primary or secondary category ID; repeatable")
    parser.add_argument("--type", action="append", choices=indexes.TYPE_ORDER, help="resource type; repeatable")
    parser.add_argument("--status", action="append", choices=VERIFICATION_STATUSES, help="verification status; repeatable")
    parser.add_argument("--security", action="append", choices=list(SECURITY_ORDER), help="security level; repeatable")
    parser.add_argument("--license", action="append", choices=LICENSE_STATUSES, help="license status; repeatable")
    parser.add_argument("--source-kind", action="append", choices=SOURCE_KINDS, help="source kind; repeatable")
    parser.add_argument("--maintenance", choices=["any", "maintained", "unmaintained"], default="any")
    parser.add_argument("--search", metavar="TEXT", help="case-insensitive text search over id, name, description and tags")
    parser.add_argument("--sort", choices=SORT_FIELDS, default="name", help="sort field (default: name)")
    parser.add_argument("--reverse", action="store_true", help="reverse the sort order")
    parser.add_argument("--limit", type=int, metavar="N", help="show at most N results")
    parser.add_argument("--format", choices=["table", "json", "ids"], default="table")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        _, resources, _ = indexes.load_data()
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    filtered = filter_resources(
        resources,
        categories=args.category,
        types=args.type,
        statuses=args.status,
        security=args.security,
        licenses=args.license,
        source_kinds=args.source_kind,
        maintenance=args.maintenance,
        search=args.search,
    )
    ordered = sort_resources(filtered, args.sort, reverse=args.reverse)
    if args.limit is not None:
        ordered = ordered[: max(args.limit, 0)]

    if args.format == "json":
        sys.stdout.write(render_json(ordered))
    elif args.format == "ids":
        for resource in ordered:
            print(resource.get("id", ""))
    else:
        print(render_table(ordered))
        print(f"\n{len(ordered)} result(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
