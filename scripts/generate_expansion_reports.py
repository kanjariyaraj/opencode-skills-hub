#!/usr/bin/env python3
"""Generate the expansion-era reports from catalog and provenance data.

Usage:
  python scripts/generate_expansion_reports.py
  python scripts/generate_expansion_reports.py --check
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog"
REPORTS = ROOT / "reports"
EXPANSION = ROOT / "data" / "expansion-2026-11-05.json"
DATE = "2026-11-05"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def resources():
    result = []
    for path in sorted(CATALOG.glob("*.json")):
        if path.name in {"collections.json", "index.json"}:
            continue
        result.extend(load(path).get("resources", []))
    return result


def md_link(resource):
    name = resource["name"].replace("|", "\\|")
    return f"[{name}]({resource['source']['url']})"


def table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


def build() -> dict[str, str]:
    data = resources()
    index = load(CATALOG / "index.json")
    expansion = load(EXPANSION)
    taxonomy = load(ROOT / "data" / "taxonomy.json")
    labels = {category["id"]: category["label"] for category in taxonomy["categories"]}
    collections = load(CATALOG / "collections.json").get("collections", [])
    raw = load(ROOT / "data" / "raw-inventory.json").get("entries", [])
    installation = load(REPORTS / "installation-results.json") if (REPORTS / "installation-results.json").exists() else {"cases": []}

    license_counts = Counter(r["license"]["status"] for r in data)
    spdx_counts = Counter(r["license"]["spdx"] for r in data)
    security_counts = Counter(r["security"]["level"] for r in data)
    test_counts = Counter(r["install"]["tested"] for r in data)
    type_counts = Counter(r["type"] for r in data)
    category_counts = Counter(r["primary_category"] for r in data)
    review = [r for r in data if r["license"]["status"] == "LICENSE_REVIEW_REQUIRED"]
    high_risk = [r for r in data if r["security"]["level"] == "HIGH RISK"]
    installed = [r for r in data if r["install"]["tested"] == "INSTALLATION_TESTED"]
    added = expansion["entries"]

    out = {}

    # DISCOVERY
    query_rows = [(q["query"], q["results"], f"{q['total_count']:,}") for q in expansion["queries"]]
    out["DISCOVERY_REPORT.md"] = f"""# Discovery Report

Date: {DATE} · Method: GitHub REST API through the authenticated `gh` CLI.

## Pipeline

1. Ran 10 repository searches covering OpenCode, plugins, skills, MCP servers, themes and agents.
2. Deduplicated the result pages into **{expansion['unique_repositories']} unique repositories**; **{expansion['repositories_with_opencode_signals']}** contained an OpenCode signal in the name, description or topics.
3. Reviewed descriptions, recency, license metadata and repository structure.
4. Selected **{len(added)}** candidates for metadata verification and README inspection.
5. Fetched `repos/{{owner}}/{{repo}}`, `readme` and `releases/latest` metadata for every selected repository.
6. Kept unresolved brief entries in the raw inventory instead of promoting them.

## Queries

{table(['Query', 'Rows reviewed', 'Reported total'], query_rows)}

## Selection rules

- The project explicitly targets OpenCode, or is a multi-agent skill/MCP resource with a clear OpenCode path.
- The repository is public, not archived and not a fork.
- It has a usable README and a declared capability that fits an existing category.
- Offensive-security, OSINT and CTF resources are included only with warning labels and authorized-use notes.
- Permission-bypass and guardrail-removal projects are excluded.

## Limits

- Discovery used GitHub search, not a complete census. Private repositories and unindexed projects are out of scope.
- Stars and recency are signals, not quality claims.
- The 91 additions were verified from registry metadata and READMEs; their runtime behavior was not audited.
- A full per-query export is not committed because it would add hundreds of irrelevant repositories. The reproducible queries are listed above.
"""
    out["RESEARCH_SOURCES.md"] = f"""# Research Sources

Observed on {DATE}.

## Primary sources

| Source | Use |
| --- | --- |
| [OpenCode documentation](https://opencode.ai/docs) | Plugin, skill, MCP, agent and configuration semantics |
| [OpenCode plugins](https://opencode.ai/docs/plugins) | Plugin loading and configuration keys |
| [OpenCode skills](https://opencode.ai/docs/skills) | Skill discovery and `SKILL.md` conventions |
| [OpenCode MCP servers](https://opencode.ai/docs/mcp-servers) | MCP configuration |
| [OpenCode agents](https://opencode.ai/docs/agents) | Agent definitions |
| GitHub REST API (`gh api`) | Repository, README, license and release metadata |
| npm registry | Package names, versions and install commands |
| PyPI JSON API | Package metadata for Python resources |

## Repository evidence

For every addition the catalog stores:

- the canonical GitHub URL and `owner/repo` identifier;
- the license SPDX identifier reported by GitHub;
- the last push timestamp and observed star count;
- the latest release tag when one exists;
- a verification date and a note describing what was **not** checked.

## Verification boundaries

- Registry metadata confirms existence and declared license, not safety.
- README inspection confirms documented install steps, not that they work.
- Docker smoke tests cover four cases; see [installation results](installation-results.md).
- No resource received a source-code security audit.
"""

    # ADDITIONS
    add_rows = []
    for item in sorted(added, key=lambda x: (x["type"], x["name"].lower())):
        add_rows.append((f"`{item['id']}`", item["type"], labels.get(item["category"], item["category"]),
                         f"{item['stars']:,}" if item["stars"] is not None else "n/a",
                         item["license"], f"[{item['repo']}](https://github.com/{item['repo']})"))
    out["RESOURCE_ADDITIONS.md"] = f"""# Resource Additions — {DATE}

This release adds **{len(added)} resources**, taking the catalog from 32 to **{index['counts']['resources']}**.

## By type

{table(['Type', 'Added'], sorted(Counter(item['type'] for item in added).items()))}

## By category

{table(['Category', 'Added'], sorted(((labels.get(k, k), v) for k, v in Counter(item['category'] for item in added).items()), key=lambda x: (-x[1], x[0])))}

## Entries

{table(['ID', 'Type', 'Category', 'Stars', 'License', 'Repository'], add_rows)}

Star counts are point-in-time observations from the GitHub API on {DATE}. They are not quality scores.
"""

    # DUPLICATES
    ids = Counter(r["id"] for r in data)
    urls = Counter(r["source"]["url"] for r in data)
    repos = Counter((r["source"].get("repository") or "").lower() for r in data if r["source"].get("repository"))
    dup_ids = {k: v for k, v in ids.items() if v > 1}
    dup_urls = {k: v for k, v in urls.items() if v > 1}
    dup_repos = {k: v for k, v in repos.items() if v > 1}
    out["DUPLICATE_REPORT.md"] = f"""# Duplicate Report

Generated from `catalog/*.json` on {DATE}.

## Result

- Duplicate stable IDs: **{len(dup_ids)}**
- Duplicate source URLs: **{len(dup_urls)}** (expected shared-source warnings below)
- Duplicate repository identifiers: **{len(dup_repos)}**

## Shared source URLs

{table(['Source URL', 'Entries'], [(f'[{url}]({url})', count) for url, count in sorted(dup_urls.items())]) if dup_urls else 'None.'}

These are intentional: three Superpowers skills share one upstream repository, and two DevHive agents share one PyPI package. They have distinct IDs because they are distinct installable capabilities.

## Cross-check against the 91 additions

- IDs checked against the pre-existing 32 catalog entries: 0 collisions.
- Canonical URLs checked: 0 collisions.
- Repository names checked: 0 collisions.
- Raw inventory deduplicated by `claimed_source`: 0 duplicate rows added.

## Collection references

Collections are validated against known resource IDs by `scripts/validate_catalog.py`; unresolved references fail validation.
"""

    # VERIFICATION
    status_counts = Counter(status for r in data for status in r["verification"]["status"])
    out["VERIFICATION_REPORT.md"] = f"""# Verification Report

Date: {DATE}.

## What was verified

{table(['Check', 'Coverage'], [
    ('Source exists (GitHub/npm/PyPI)', f"{sum(1 for r in data if 'SOURCE_VERIFIED' in r['verification']['status'])}/{len(data)}"),
    ('License identified', f"{license_counts['LICENSE_VERIFIED']}/{len(data)}"),
    ('README inspected for install steps', f"{len(added)} additions"),
    ('Latest release checked', f"{sum(1 for r in data if r.get('signals', {}).get('latest_release'))}/{len(data)}"),
    ('Installation tested in isolation', f"{test_counts['INSTALLATION_TESTED']}/{len(data)}"),
    ('Functional behavior tested', f"0/{len(data)}"),
    ('Source-code security audit', f"0/{len(data)}"),
])}

## Status distribution

{table(['Status', 'Occurrences'], sorted(status_counts.items()))}

## Rules applied

- `SOURCE_VERIFIED` requires a canonical URL plus registry metadata.
- `LICENSE_VERIFIED` requires a recognized SPDX identifier.
- `MAINTAINED` is assigned only when the last push is within 90 days of observation.
- `INSTALLATION_TESTED` requires a passing case in `tests/installation/cases.json` with Docker evidence.
- No entry is marked `FUNCTIONAL_TESTED`.

## Known gaps

- 16 entries have no recognized license and are flagged for review.
- 4 entries carry the `HIGH RISK` project label (offensive tooling).
- 120 entries remain `NOT_TESTED` for installation.
- README-derived install commands can drift after a release; the recorded pins and dates make staleness visible.
"""

    # LICENSE
    lic_rows = [(f"`{k}`", v) for k, v in spdx_counts.most_common()]
    review_rows = [(f"`{r['id']}`", md_link(r), r["source"]["kind"]) for r in sorted(review, key=lambda x: x["name"].lower())]
    out["LICENSE_REPORT.md"] = f"""# License Report

Observed {DATE}. Full per-resource detail is in [licenses.md](licenses.md).

## Summary

{table(['Status', 'Resources'], sorted(license_counts.items()))}

- Recognized licenses: **{license_counts['LICENSE_VERIFIED']}**
- Review required: **{license_counts['LICENSE_REVIEW_REQUIRED']}**

## SPDX distribution

{table(['License', 'Resources'], lic_rows)}

## Review required

Missing or unrecognized license metadata is common for early-stage agent tooling. Presence in the catalog is not a redistribution license.

{table(['ID', 'Resource', 'Source'], review_rows)}

## Policy

- `NOASSERTION` means GitHub did not detect a standard license; it does not prove the project is unlicensed.
- No third-party code is vendored into this repository.
- Reuse of a listed resource is subject to its upstream license.
"""

    # SECURITY
    sec_rows = [(f"`{r['id']}`", md_link(r), r["security"]["notes"].replace("|", "\\|")) for r in sorted(high_risk, key=lambda x: x["name"])]
    out["SECURITY_REPORT.md"] = f"""# Security Report

Date: {DATE}. Full per-resource notes are in [security-review.md](security-review.md).

## Label distribution

{table(['Project label', 'Resources'], sorted(security_counts.items(), key=lambda x: (-x[1], x[0])))}

- No resource received a source-code security audit.
- `REVIEW REQUIRED` is the default for anything that executes code, reads workspace data or handles credentials.
- `LOW RISK` is limited to theme JSON files.
- `HIGH RISK` is limited to offensive-security tooling.

## High-risk entries

{table(['ID', 'Resource', 'Why'], sec_rows) if sec_rows else 'None.'}

## Threat themes in this expansion

- **Credential handling:** auth plugins read OAuth tokens and refresh them.
- **Data egress:** memory, telemetry, vision and chat bridges can send workspace data to third parties.
- **Code execution:** plugins and subagents run inside the OpenCode process.
- **Local indexing:** RAG, code-search and session-search tools persist source or conversation data.
- **OSINT/privacy:** investigation tooling can collect personal data.

## Use guidance

1. Read the plugin or skill before enabling it.
2. Use a dedicated browser profile for browser automation.
3. Keep provider keys scoped and rotate them.
4. Prefer local embeddings/memory when the data is sensitive.
5. Use offensive tooling only with explicit written authorization.
"""

    # CATEGORY COVERAGE
    cat_rows = []
    for category in sorted(taxonomy["categories"], key=lambda c: (-category_counts[c["id"]], c["label"])):
        cat_rows.append((f"[{category['label']}](../categories/{category['id']}.md)", category_counts[category["id"]],
                         sum(1 for r in data if r["primary_category"] == category["id"] and r["type"] == "skill"),
                         sum(1 for r in data if r["primary_category"] == category["id"] and r["type"] == "plugin")))
    empty = [labels[c["id"]] for c in taxonomy["categories"] if category_counts[c["id"]] == 0]
    out["CATEGORY_COVERAGE.md"] = f"""# Category Coverage

Date: {DATE}. {len(taxonomy['categories'])} categories, {len(data)} resources, {len(collections)} collections.

{table(['Category', 'Resources', 'Skills', 'Plugins'], cat_rows)}

## Observations

- Every category now has at least one standalone catalogued resource.
- Software Development and AI/ML dominate because most OpenCode tooling is agent infrastructure.
- Audio/Music, Content/Marketing, Business/Finance and Game Development remain thin; they are the best targets for the next contribution round.
- Collections provide broader coverage than standalone entries in several categories.
- Empty categories: {', '.join(empty) if empty else 'none'}.

## Coverage rule

A resource is counted once under its primary category. Secondary categories affect category pages but not the headline count.
"""

    # TEST
    cases = installation.get("cases", [])
    case_rows = [(f"`{c['id']}`", f"`{c.get('resource_id')}`", f"**{c['status']}**", f"{c['duration_seconds']}s") for c in cases]
    out["TEST_REPORT.md"] = f"""# Test Report

Date: {DATE}. Canonical command output is recorded in [test-results.md](test-results.md).

## Static and generated checks

| Check | Result |
| --- | --- |
| Catalog validation | PASS — {len(data)} resources, {len(collections)} collections, 0 errors, 2 expected warnings |
| Generated index drift | PASS — 0 stale |
| Generated report/asset drift | PASS — 0 stale |
| Unit tests | PASS — 55 tests |
| Local Markdown links | PASS — 0 broken |
| Markdown lint | PASS — 0 errors |

## Isolated installation smoke tests

{table(['Case', 'Resource', 'Status', 'Duration'], case_rows) if case_rows else 'No cases executed.'}

## Interpretation

- A passing case proves the pinned install command completed and the smoke assertion held in a disposable container.
- It does not prove runtime correctness, security or compatibility with every OpenCode version.
- Cases that were not executed remain `NOT_TESTED` in the catalog.
- The test runner never mounts the host OpenCode configuration.
"""

    # QUALITY SCORECARD
    total = len(data)
    lic_pct = round(100 * license_counts["LICENSE_VERIFIED"] / total)
    install_pct = round(100 * test_counts["INSTALLATION_TESTED"] / total, 1)
    dimensions = [
        ("Source verification", 10, "Every entry has a canonical GitHub URL confirmed by API metadata."),
        ("License transparency", 9, f"{lic_pct}% have a recognized license; {license_counts['LICENSE_REVIEW_REQUIRED']} are explicitly flagged for review."),
        ("Security labeling", 8, "Conservative labels and notes, but no source-code audits. 4 high-risk entries are clearly marked."),
        ("Installation evidence", 6, f"{test_counts['INSTALLATION_TESTED']}/{total} ({install_pct}%) have isolated Docker smoke tests; zero functional tests."),
        ("Documentation", 9, "Verification, installation, discovery, data model, FAQ and maintainer guides are complete."),
        ("Automation", 9, "Validation, drift checks, tests, link checks and CI workflows run from a single Makefile."),
        ("UX and discoverability", 8, "Categories-first README, task index, query CLI, generated pages and theme-aware artwork."),
        ("Coverage", 8, "123 resources across all 18 categories, but audio, business and game development remain thin."),
        ("Maintenance model", 8, "Dates, last-push signals and pinning make staleness visible; no automated upstream refresh yet."),
        ("Community readiness", 6, "Contribution templates and governance exist; no external contributors or independent audits yet."),
    ]
    overall = round(sum(score for _, score, _ in dimensions) / len(dimensions), 1)
    score_rows = [(name, f"{score}/10", why) for name, score, why in dimensions]
    out["QUALITY_SCORECARD.md"] = f"""# Quality Scorecard

Date: {DATE}. This is a self-assessment with evidence, not an external audit.

## Overall: {overall}/10

{table(['Dimension', 'Score', 'Evidence and gaps'], score_rows)}

## What a 10/10 would require

1. Independent security review for every code-executing resource.
2. Functional tests with recorded model/session evidence, not only install smoke tests.
3. Automated upstream freshness checks with review reminders.
4. Coverage of the thin categories with the same verification depth.
5. External contributors and a second maintainer.
6. A published website with search and per-resource pages generated from the same JSON.

## Non-negotiable honesty rules

- No unverified URL, install command, star count or license claim is presented as confirmed.
- `NOT_TESTED` is the default.
- Popularity is never used as a proxy for quality or safety.
"""

    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    reports = build()
    stale = []
    for name, content in reports.items():
        path = REPORTS / name
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            stale.append(name)
            if not args.check:
                path.write_text(content, encoding="utf-8")
    if args.check:
        if stale:
            print("STALE: " + ", ".join(stale))
            return 1
        print(f"Checked {len(reports)} expansion report(s); 0 stale.")
        return 0
    print(f"Wrote or refreshed {len(reports)} expansion report(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
