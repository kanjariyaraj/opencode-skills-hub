#!/usr/bin/env python3
"""Generate catalog index, category pages and collection pages from source data.

Usage:
  python scripts/generate_indexes.py          # write generated files
  python scripts/generate_indexes.py --check  # fail if generated files are stale

Exit codes:
  0  generated or up to date
  1  --check found stale or missing generated files
  2  usage or IO error
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_DIR = ROOT / "catalog"
DATA_DIR = ROOT / "data"
CATEGORIES_DIR = ROOT / "categories"
COLLECTIONS_DIR = ROOT / "collections"
INDEX_PATH = CATALOG_DIR / "index.json"

TYPE_ORDER = ["skill", "agent", "plugin", "mcp", "command", "rule", "hook", "provider"]
TYPE_LABELS = {
    "skill": "Skills",
    "agent": "Agents",
    "plugin": "Plugins",
    "mcp": "MCP Servers",
    "command": "Commands",
    "rule": "Rules",
    "hook": "Hooks",
    "provider": "Providers",
}
STATUS_LABELS = {
    "SOURCE_VERIFIED": "source verified",
    "LICENSE_VERIFIED": "license verified",
    "COMPATIBILITY_VERIFIED": "compatibility verified",
    "INSTALLATION_TESTED": "installation tested",
    "FUNCTIONAL_TESTED": "functionally tested",
    "MAINTAINED": "active",
    "UNMAINTAINED": "low activity",
    "LICENSE_REVIEW_REQUIRED": "license review required",
    "SECURITY_REVIEW_REQUIRED": "security review required",
    "DISCOVERED": "discovered",
}


def load_json(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_data():
    taxonomy = load_json(DATA_DIR / "taxonomy.json")
    resources: list[dict] = []
    for path in sorted(CATALOG_DIR.glob("*.json")):
        if path.name in {"collections.json", "index.json"}:
            continue
        document = load_json(path)
        for resource in document.get("resources", []):
            resource = dict(resource)
            resource["_file"] = path.name
            resources.append(resource)
    collections_doc = load_json(CATALOG_DIR / "collections.json")
    collections = collections_doc.get("collections", [])
    return taxonomy, resources, collections


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def resource_link(resource: dict) -> str:
    url = (resource.get("source") or {}).get("url")
    name = md_escape(resource.get("name", resource.get("id", "")))
    if url and url.startswith(("http://", "https://")):
        return f"[{name}]({url})"
    return name


def status_text(resource: dict) -> str:
    statuses = (resource.get("verification") or {}).get("status", [])
    labels = [STATUS_LABELS.get(status, status.lower().replace("_", " ")) for status in statuses]
    return ", ".join(labels) if labels else "unverified"


def resource_row(resource: dict) -> str:
    source_kind = (resource.get("source") or {}).get("kind", "unknown")
    license_obj = resource.get("license") or {}
    security = resource.get("security") or {}
    return (
        f"| {resource_link(resource)} | {md_escape(resource.get('type', ''))} | "
        f"{md_escape(resource.get('description', ''))} | {md_escape(source_kind)} | "
        f"{md_escape(license_obj.get('spdx', 'UNKNOWN'))} | {md_escape(security.get('level', 'REVIEW REQUIRED'))} | "
        f"{md_escape(status_text(resource))} |"
    )


def resource_table(resources: list[dict]) -> str:
    lines = [
        "| Resource | Type | What it does | Source | License | Security | Verification |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for resource in sorted(resources, key=lambda item: item.get("name", "").lower()):
        lines.append(resource_row(resource))
    return "\n".join(lines)


def collection_table(collections: list[dict]) -> str:
    lines = [
        "| Collection | Kind | What it is | Source | Verification |",
        "| --- | --- | --- | --- | --- |",
    ]
    for collection in sorted(collections, key=lambda item: item.get("name", "").lower()):
        source = (collection.get("source") or {}).get("url") or ""
        name = md_escape(collection.get("name", collection.get("id", "")))
        linked = f"[{name}]({source})" if source.startswith(("http://", "https://")) else name
        statuses = (collection.get("verification") or {}).get("status", [])
        labels = [STATUS_LABELS.get(status, status.lower().replace("_", " ")) for status in statuses]
        lines.append(
            f"| {linked} | {md_escape(collection.get('kind', ''))} | "
            f"{md_escape(collection.get('description', ''))} | {md_escape((collection.get('source') or {}).get('kind', 'n/a'))} | "
            f"{md_escape(', '.join(labels) or 'unverified')} |"
        )
    return "\n".join(lines)


def build_index(taxonomy: dict, resources: list[dict], collections: list[dict]) -> dict:
    by_type = Counter(resource.get("type") for resource in resources)
    by_category: dict[str, list[str]] = defaultdict(list)
    for resource in resources:
        by_category[resource.get("primary_category", "")].append(resource.get("id"))
    for values in by_category.values():
        values.sort()
    return {
        "schema_version": "1.0.0",
        "counts": {
            "resources": len(resources),
            "collections": len(collections),
            "by_type": {type_name: by_type.get(type_name, 0) for type_name in TYPE_ORDER},
        },
        "categories": [
            {
                "id": category["id"],
                "label": category["label"],
                "resource_count": len(by_category.get(category["id"], [])),
                "resource_ids": by_category.get(category["id"], []),
            }
            for category in taxonomy["categories"]
        ],
        "resources": sorted(
            ({key: value for key, value in resource.items() if not key.startswith("_")} for resource in resources),
            key=lambda item: item.get("id", ""),
        ),
        "collections": sorted(collections, key=lambda item: item.get("id", "")),
    }


def build_categories_readme(taxonomy: dict, resources: list[dict], collections: list[dict]) -> str:
    by_category = Counter(resource.get("primary_category") for resource in resources)
    pack_counts = Counter()
    for collection in collections:
        for category in collection.get("categories", []):
            pack_counts[category] += 1
    lines = [
        "# Categories",
        "",
        "Browse the catalog by domain. Every category page is generated from the JSON catalog in [`catalog/`](../catalog/).",
        "",
        "| Category | Resources | Collections |",
        "| --- | ---: | ---: |",
    ]
    for category in taxonomy["categories"]:
        lines.append(
            f"| [{md_escape(category['label'])}]({category['id']}.md) | "
            f"{by_category.get(category['id'], 0)} | {pack_counts.get(category['id'], 0)} |"
        )
    lines.extend([
        "",
        "## How counts are produced",
        "",
        "Counts reflect entries in the structured catalog, not social-media popularity or upstream claims. A resource may appear on more than one category page through its secondary categories, but it is counted once under its primary category.",
        "",
    ])
    return "\n".join(lines)


def build_category_page(category: dict, resources: list[dict], collections: list[dict], taxonomy: dict) -> str:
    category_id = category["id"]
    primary = [resource for resource in resources if resource.get("primary_category") == category_id]
    secondary = [
        resource for resource in resources
        if resource.get("primary_category") != category_id
        and category_id in resource.get("secondary_categories", [])
    ]
    packs = [
        collection for collection in collections
        if collection.get("kind") in {"skill-pack", "toolkit"} and category_id in collection.get("categories", [])
    ]
    roles = [
        collection for collection in collections
        if collection.get("kind") == "role" and category_id in collection.get("categories", [])
    ]
    related = [item for item in taxonomy["categories"] if item["id"] in category.get("related", [])]

    lines = [
        f"# {category['label']}",
        "",
        f"> {category['description']}",
        "",
        f"**Catalog entries:** {len(primary)} primary, {len(secondary)} secondary. "
        f"**Collections:** {len(packs)} packs/toolkits, {len(roles)} role collections.",
        "",
    ]
    if category.get("subcategories"):
        lines.append("**Subcategories:** " + ", ".join(f"`{item}`" for item in category["subcategories"]))
        lines.append("")

    if primary or secondary:
        lines.extend([
            "## Recommended starting points",
            "",
            "Start with the entries marked *source verified* and *license verified*. "
            "Every entry keeps upstream claims separate from independent verification.",
            "",
            resource_table(primary + secondary),
            "",
        ])
    else:
        lines.extend([
            "## Recommended starting points",
            "",
            "No catalogued resource has this category as its primary or secondary category yet. "
            "See the collections below and the [contribution guide](../CONTRIBUTING.md) to add one.",
            "",
        ])

    by_type = defaultdict(list)
    for resource in primary:
        by_type[resource.get("type")].append(resource)
    for type_name in TYPE_ORDER:
        if by_type.get(type_name):
            lines.extend([f"## {TYPE_LABELS[type_name]}", "", resource_table(by_type[type_name]), ""])

    if packs:
        lines.extend(["## Skill packs and toolkits", "", collection_table(packs), ""])
    if roles:
        lines.extend([
            "## Role collections",
            "",
            "\n".join(f"- [{md_escape(role['name'])}](../collections/{role['id']}.md) — {md_escape(role['description'])}" for role in sorted(roles, key=lambda item: item["name"])),
            "",
        ])
    if related:
        lines.extend(["## Related categories", ""])
        for item in related:
            lines.append(f"- [{item['label']}]({item['id']}.md) — {item['description']}")
        lines.append("")

    lines.extend([
        "## Verification legend",
        "",
        "- **source verified**: repository, package or documentation URL confirmed against a registry.",
        "- **license verified**: a license was confirmed from registry metadata.",
        "- **license review required**: no recognized license was found; do not redistribute until resolved.",
        "- **active / low activity**: based on the most recent observed upstream push, not a quality claim.",
        "- **security level**: a project review label, not a guarantee of safety.",
        "",
        "See [Verification](../docs/verification.md) and [Security](../SECURITY.md).",
        "",
    ])
    return "\n".join(lines)


def build_collections_readme(collections: list[dict]) -> str:
    roles = [item for item in collections if item.get("kind") == "role"]
    packs = [item for item in collections if item.get("kind") in {"skill-pack", "toolkit"}]
    lines = [
        "# Collections",
        "",
        "Collections come in two forms:",
        "",
        "- **Role collections** map a user role to catalogued resources and packs.",
        "- **Skill packs / toolkits** are upstream repositories that bundle many resources.",
        "",
        "Inclusion is a discovery aid, not an endorsement or a security guarantee.",
        "",
        "## Role collections",
        "",
        collection_table(roles),
        "",
        "## Skill packs and toolkits",
        "",
        collection_table(packs),
        "",
    ]
    return "\n".join(lines)


def build_collection_page(collection: dict, resources_by_id: dict[str, dict], collections_by_id: dict[str, dict]) -> str:
    source = collection.get("source") or {}
    lines = [
        f"# {collection['name']}",
        "",
        f"> {collection['description']}",
        "",
        f"**Kind:** {collection.get('kind')}",
        "",
    ]
    if collection.get("audience"):
        lines.extend([f"**Audience:** {collection['audience']}", ""])
    if source.get("url"):
        label = "Upstream source" if source.get("kind") != "unknown" else "Reference"
        lines.extend([f"**{label}:** <{source['url']}>", ""])

    verification = collection.get("verification") or {}
    statuses = verification.get("status", [])
    labels = [STATUS_LABELS.get(status, status.lower().replace("_", " ")) for status in statuses]
    lines.extend([
        f"**Verification:** {', '.join(labels) or 'unverified'} ({verification.get('date', 'n/a')})",
        "",
        f"{verification.get('notes', '')}",
        "",
    ])

    if collection.get("kind") == "role" and collection.get("resources"):
        lines.extend([
            "## Resources in this collection",
            "",
            "| Resource | Type | What it does | Source | Security | Verification |",
            "| --- | --- | --- | --- | --- | --- |",
        ])
        for reference in collection["resources"]:
            resource = resources_by_id.get(reference)
            if resource:
                lines.append(
                    f"| {resource_link(resource)} | {md_escape(resource.get('type', ''))} | "
                    f"{md_escape(resource.get('description', ''))} | {md_escape((resource.get('source') or {}).get('kind', 'unknown'))} | "
                    f"{md_escape((resource.get('security') or {}).get('level', 'REVIEW REQUIRED'))} | {md_escape(status_text(resource))} |"
                )
                continue
            nested = collections_by_id.get(reference)
            if nested:
                nested_source = (nested.get("source") or {}).get("url") or ""
                name = md_escape(nested.get("name", reference))
                linked = f"[{name}]({nested_source})" if nested_source.startswith(("http://", "https://")) else name
                lines.append(
                    f"| {linked} (pack) | collection | {md_escape(nested.get('description', ''))} | "
                    f"{md_escape((nested.get('source') or {}).get('kind', 'unknown'))} | n/a | "
                    f"{md_escape(', '.join(STATUS_LABELS.get(s, s) for s in (nested.get('verification') or {}).get('status', [])))} |"
                )
        lines.append("")
    elif collection.get("kind") in {"skill-pack", "toolkit"}:
        lines.extend([
            "## What is inside",
            "",
            "This is an upstream bundle. It is catalogued as a single entry rather than decomposed into unverified sub-items. "
            "Read the upstream README and review the files before installing.",
            "",
        ])

    lines.extend([
        "## Safety",
        "",
        "Inclusion does not imply that the resource is safe. Check the security level, license and verification status before installing. "
        "For offensive-security resources, use only systems you own or have explicit written authorization to test.",
        "",
        "Back to [all collections](README.md) or the [category index](../categories/README.md).",
        "",
    ])
    return "\n".join(lines)


def render_outputs() -> dict[Path, str]:
    taxonomy, resources, collections = load_data()
    resources_by_id = {resource["id"]: resource for resource in resources}
    collections_by_id = {collection["id"]: collection for collection in collections}

    outputs: dict[Path, str] = {}
    outputs[INDEX_PATH] = json.dumps(build_index(taxonomy, resources, collections), indent=2, sort_keys=False) + "\n"
    outputs[CATEGORIES_DIR / "README.md"] = build_categories_readme(taxonomy, resources, collections)
    outputs[COLLECTIONS_DIR / "README.md"] = build_collections_readme(collections)
    for category in taxonomy["categories"]:
        outputs[CATEGORIES_DIR / f"{category['id']}.md"] = build_category_page(category, resources, collections, taxonomy)
    for collection in collections:
        outputs[COLLECTIONS_DIR / f"{collection['id']}.md"] = build_collection_page(collection, resources_by_id, collections_by_id)
    return outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if generated files differ from disk")
    args = parser.parse_args(argv)

    try:
        outputs = render_outputs()
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    stale: list[str] = []
    for path, content in sorted(outputs.items()):
        if args.check:
            if not path.exists():
                stale.append(f"missing: {path.relative_to(ROOT)}")
            elif path.read_text(encoding="utf-8") != content:
                stale.append(f"stale: {path.relative_to(ROOT)}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                path.write_text(content, encoding="utf-8")

    if args.check:
        for item in stale:
            print(f"STALE {item}")
        print(f"Checked {len(outputs)} generated file(s); {len(stale)} stale.")
        return 1 if stale else 0

    print(f"Wrote or refreshed {len(outputs)} generated file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
