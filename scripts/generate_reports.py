#!/usr/bin/env python3
"""Generate evidence-based reports from the catalog and raw inventory.

Generated reports:
  reports/stats.md
  reports/missing-sources.md
  reports/licenses.md
  reports/compatibility.md
  reports/security-review.md

Usage:
  python scripts/generate_reports.py          # write reports
  python scripts/generate_reports.py --check  # fail if reports are stale

Exit codes:
  0  generated or up to date
  1  --check found stale or missing reports
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
REPORTS_DIR = ROOT / "reports"

RESOURCE_TYPES = ["skill", "agent", "plugin", "mcp", "command", "rule", "hook", "provider"]
TYPE_LABELS = {
    "skill": "Skills", "agent": "Agents", "plugin": "Plugins", "mcp": "MCP Servers",
    "command": "Commands", "rule": "Rules", "hook": "Hooks", "provider": "Providers",
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
        resources.extend(load_json(path).get("resources", []))
    collections = load_json(CATALOG_DIR / "collections.json").get("collections", [])
    raw = load_json(DATA_DIR / "raw-inventory.json").get("entries", [])
    return taxonomy, resources, collections, raw


def md(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def autolink(value: object) -> str:
    text = md(value)
    if text.startswith(("http://", "https://")):
        return f"<{text}>"
    return text


def link(resource: dict) -> str:
    url = (resource.get("source") or {}).get("url")
    name = md(resource.get("name", resource.get("id", "")))
    return f"[{name}]({url})" if url and url.startswith(("http://", "https://")) else name


def build_stats(taxonomy, resources, collections, raw) -> str:
    by_type = Counter(resource.get("type") for resource in resources)
    by_category = Counter(resource.get("primary_category") for resource in resources)
    by_security = Counter((resource.get("security") or {}).get("level") for resource in resources)
    by_license = Counter((resource.get("license") or {}).get("status") for resource in resources)
    by_spdx = Counter((resource.get("license") or {}).get("spdx") for resource in resources)
    by_install = Counter((resource.get("install") or {}).get("tested") for resource in resources)
    verification = Counter()
    for resource in resources:
        for status in (resource.get("verification") or {}).get("status", []):
            verification[status] += 1
    active = sum(1 for resource in resources if "MAINTAINED" in (resource.get("verification") or {}).get("status", []))
    low_activity = sum(1 for resource in resources if "UNMAINTAINED" in (resource.get("verification") or {}).get("status", []))
    raw_resolution = Counter(entry.get("resolution") for entry in raw)

    lines = [
        "# Catalog Statistics",
        "",
        "Generated from `catalog/*.json` and `data/raw-inventory.json`. These numbers describe catalog entries, not upstream project popularity.",
        "",
        "## Totals",
        "",
        f"- Catalogued resources: **{len(resources)}**",
        f"- Collections (role collections plus skill packs/toolkits): **{len(collections)}**",
        f"- Raw inventory entries preserved: **{len(raw)}**",
        f"- Active resources (recent upstream push observed): **{active}**",
        f"- Low-activity resources (older upstream push): **{low_activity}**",
        "",
        "## Resources by type",
        "",
        "| Type | Count |",
        "| --- | ---: |",
    ]
    for type_name in RESOURCE_TYPES:
        lines.append(f"| {TYPE_LABELS[type_name]} | {by_type.get(type_name, 0)} |")

    lines.extend(["", "## Resources by primary category", "", "| Category | Count |", "| --- | ---: |"])
    labels = {category["id"]: category["label"] for category in taxonomy["categories"]}
    for category in taxonomy["categories"]:
        lines.append(f"| [{labels[category['id']]}](../categories/{category['id']}.md) | {by_category.get(category['id'], 0)} |")

    lines.extend(["", "## Verification status coverage", "", "| Status | Resources |", "| --- | ---: |"])
    for status, count in sorted(verification.items()):
        lines.append(f"| `{status}` | {count} |")

    lines.extend(["", "## Security review labels", "", "| Label | Resources |", "| --- | ---: |"])
    for level in ["LOW RISK", "REVIEWED", "REVIEW REQUIRED", "HIGH RISK", "UNSAFE", "DEPRECATED"]:
        lines.append(f"| {level} | {by_security.get(level, 0)} |")

    lines.extend(["", "## License status", "", "| Status | Resources |", "| --- | ---: |"])
    for status in ["LICENSE_VERIFIED", "LICENSE_REVIEW_REQUIRED", "NOASSERTION", "UNKNOWN"]:
        lines.append(f"| {status} | {by_license.get(status, 0)} |")

    lines.extend(["", "## SPDX identifiers observed", "", "| SPDX | Resources |", "| --- | ---: |"])
    for spdx, count in sorted(by_spdx.items(), key=lambda item: str(item[0])):
        lines.append(f"| {md(spdx)} | {count} |")

    lines.extend(["", "## Installation testing", "", "| Status | Resources |", "| --- | ---: |"])
    for status, count in sorted(by_install.items()):
        lines.append(f"| `{status}` | {count} |")
    lines.extend([
        "",
        "> No third-party resource was installed on the host during cataloging. `NOT_TESTED` is the honest default; "
        "upstream README claims are not treated as independent test results.",
        "",
        "## Raw inventory resolution",
        "",
        "| Resolution | Entries |",
        "| --- | ---: |",
    ])
    for status in ["VERIFIED", "SOURCE_UNRESOLVED", "NOT_FOUND", "RESTRICTED", "DUPLICATE"]:
        lines.append(f"| {status} | {raw_resolution.get(status, 0)} |")
    lines.append("")
    return "\n".join(lines)


def build_missing_sources(raw) -> str:
    unresolved = [entry for entry in raw if entry.get("resolution") != "VERIFIED"]
    by_resolution = defaultdict(list)
    for entry in unresolved:
        by_resolution[entry.get("resolution", "UNKNOWN")].append(entry)
    lines = [
        "# Missing and Unresolved Sources",
        "",
        "Every entry from the original discovery brief is preserved in `data/raw-inventory.json`. "
        "This report lists entries that could not be promoted to the verified catalog because the source was missing, unresolved, not found, or restricted.",
        "",
        f"Unresolved raw entries: **{len(unresolved)}** of **{len(raw)}**.",
        "",
    ]
    for resolution in ["SOURCE_UNRESOLVED", "NOT_FOUND", "RESTRICTED", "DUPLICATE"]:
        entries = by_resolution.get(resolution, [])
        if not entries:
            continue
        lines.extend([f"## {resolution.replace('_', ' ').title()} ({len(entries)})", "", "| Entry | Claimed source | Category | Notes |", "| --- | --- | --- | --- |"])
        for entry in sorted(entries, key=lambda item: item.get("name", "")):
            lines.append(
                f"| {md(entry.get('name'))} | {autolink(entry.get('claimed_source'))} | "
                f"{md(entry.get('category'))} | {md(entry.get('notes'))} |"
            )
        lines.append("")
    lines.extend([
        "## How to resolve an entry",
        "",
        "1. Find the canonical upstream repository, package registry page or official documentation.",
        "2. Confirm the license and compatibility.",
        "3. Add a full entry to the correct `catalog/<type>.json` file.",
        "4. Change the raw inventory resolution to `VERIFIED` and note the evidence.",
        "",
        "Never guess a repository owner, package name or install command.",
        "",
    ])
    return "\n".join(lines)


def build_licenses(resources) -> str:
    review = [resource for resource in resources if (resource.get("license") or {}).get("status") != "LICENSE_VERIFIED"]
    lines = [
        "# License Report",
        "",
        "License status is taken from registry metadata observed on 2026-11-05. A missing SPDX identifier is not proof that a project is unlicensed; it means the catalog could not confirm a license.",
        "",
        "| Resource | License | Status | Source |",
        "| --- | --- | --- | --- |",
    ]
    for resource in sorted(resources, key=lambda item: item.get("name", "")):
        license_obj = resource.get("license") or {}
        lines.append(
            f"| {link(resource)} | {md(license_obj.get('spdx', 'UNKNOWN'))} | "
            f"{md(license_obj.get('status', 'UNKNOWN'))} | {md((resource.get('source') or {}).get('kind', 'unknown'))} |"
        )
    lines.extend([
        "",
        f"## Review required ({len(review)})",
        "",
        "The following resources do not have a verified license and must not be redistributed until resolved:",
        "",
    ])
    if review:
        for resource in sorted(review, key=lambda item: item.get("name", "")):
            lines.append(f"- {link(resource)} — {(resource.get('license') or {}).get('status', 'UNKNOWN')}")
    else:
        lines.append("- None.")
    lines.extend([
        "",
        "## Special notes",
        "",
        "- `termux-skill` uses CC-BY-NC-4.0, a non-commercial license. Verify that your use is permitted.",
        "- Resources without a detected license are kept in the catalog for discovery but are flagged for review.",
        "",
    ])
    return "\n".join(lines)


def build_compatibility(resources) -> str:
    lines = [
        "# Compatibility Report",
        "",
        "Compatibility is recorded from the catalog entry, not from an installation test unless explicitly marked `INSTALLATION_TESTED`.",
        "",
        "| Resource | OpenCode | Platforms | Dependencies | API key | Install test |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for resource in sorted(resources, key=lambda item: item.get("name", "")):
        compatibility = resource.get("compatibility") or {}
        install = resource.get("install") or {}
        lines.append(
            f"| {link(resource)} | {md(compatibility.get('opencode', 'unknown'))} | "
            f"{md(', '.join(compatibility.get('platforms', [])) or 'unspecified')} | "
            f"{md(', '.join(compatibility.get('dependencies', [])) or 'none declared')} | "
            f"{'yes' if install.get('requires_api_key') else 'no'} | {md(install.get('tested', 'NOT_TESTED'))} |"
        )
    lines.extend([
        "",
        "## Interpretation",
        "",
        "- `native`: built specifically for OpenCode.",
        "- `compatible`: the upstream project states compatibility or uses a portable skill/plugin format.",
        "- `unknown`: no compatibility evidence was collected.",
        "- `incompatible`: known not to work with OpenCode.",
        "",
        "No entry in this catalog has been end-to-end tested in a disposable OpenCode environment. "
        "Treat `NOT_TESTED` as a call to verify in your own environment.",
        "",
    ])
    return "\n".join(lines)


def build_security(resources) -> str:
    high = [resource for resource in resources if (resource.get("security") or {}).get("level") in {"HIGH RISK", "UNSAFE"}]
    review = [resource for resource in resources if (resource.get("security") or {}).get("level") == "REVIEW REQUIRED"]
    lines = [
        "# Security Review Report",
        "",
        "These are project review labels, not guarantees. No resource was executed during cataloging.",
        "",
        "## Method",
        "",
        "1. Confirm the source against GitHub, npm or PyPI metadata.",
        "2. Record the declared license and last observed push.",
        "3. Assign a conservative security label based on capability (instruction-only, shell execution, database access, browser control, offensive tooling).",
        "4. Keep permission-bypass and guardrail-removal tools out of the main catalog.",
        "",
        "## High-risk and restricted-capability entries",
        "",
        "| Resource | Level | Capability | Notes |",
        "| --- | --- | --- | --- |",
    ]
    if high:
        for resource in sorted(high, key=lambda item: item.get("name", "")):
            security = resource.get("security") or {}
            lines.append(f"| {link(resource)} | {md(security.get('level'))} | {md(resource.get('type'))} | {md(security.get('notes'))} |")
    else:
        lines.append("| None | n/a | n/a | No high-risk entries catalogued. |")
    lines.extend([
        "",
        f"## Review required ({len(review)})",
        "",
        "These entries were not security-audited. Review them before use, especially anything that executes shell commands, accesses databases, controls a browser or handles credentials.",
        "",
        "| Resource | Notes |",
        "| --- | --- |",
    ])
    if review:
        for resource in sorted(review, key=lambda item: item.get("name", "")):
            lines.append(f"| {link(resource)} | {md((resource.get('security') or {}).get('notes'))} |")
    else:
        lines.append("| None | n/a |")
    lines.extend([
        "",
        "## Restricted archive",
        "",
        "Permission-bypass, guardrail-removal and jailbreak-style tools are documented only in [`restricted/README.md`](../restricted/README.md). They are excluded from the catalog and are not recommended.",
        "",
        "## Authorization policy",
        "",
        "Offensive-security resources may only be used against systems you own or for which you have explicit written authorization. Never scan, exploit or disrupt third-party systems.",
        "",
        "## Credential policy",
        "",
        "No secrets are stored in the catalog or reports. API keys must be supplied through environment variables and never committed.",
        "",
    ])
    return "\n".join(lines)


def render_outputs() -> dict[Path, str]:
    taxonomy, resources, collections, raw = load_data()
    return {
        REPORTS_DIR / "stats.md": build_stats(taxonomy, resources, collections, raw),
        REPORTS_DIR / "missing-sources.md": build_missing_sources(raw),
        REPORTS_DIR / "licenses.md": build_licenses(resources),
        REPORTS_DIR / "compatibility.md": build_compatibility(resources),
        REPORTS_DIR / "security-review.md": build_security(resources),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if reports differ from disk")
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
        print(f"Checked {len(outputs)} report(s); {len(stale)} stale.")
        return 1 if stale else 0

    print(f"Wrote or refreshed {len(outputs)} report(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
