# Reports

Two kinds of files live here:

- **Generated snapshots** — rebuilt from `catalog/*.json`, `data/raw-inventory.json` and `data/expansion-2026-11-05.json`. Do not edit by hand.
- **Evidence records** — command output from a specific run. Do not rewrite history; add a new dated run instead.

## Catalog snapshots

| Report | Contents |
| --- | --- |
| [stats.md](stats.md) | Counts by type, category, verification, security and license |
| [missing-sources.md](missing-sources.md) | Raw inventory entries that are not verified |
| [licenses.md](licenses.md) | Per-resource license status |
| [compatibility.md](compatibility.md) | OpenCode compatibility, platforms and dependencies |
| [security-review.md](security-review.md) | Per-resource security labels and capability notes |
| [documentation-checklist.md](documentation-checklist.md) | Maintainer documentation checklist |

## Expansion and quality reports

| Report | Contents |
| --- | --- |
| [DISCOVERY_REPORT.md](DISCOVERY_REPORT.md) | Search queries, deduplication and selection rules |
| [RESEARCH_SOURCES.md](RESEARCH_SOURCES.md) | Official docs and registry evidence used |
| [RESOURCE_ADDITIONS.md](RESOURCE_ADDITIONS.md) | The 91 resources added in this release |
| [DUPLICATE_REPORT.md](DUPLICATE_REPORT.md) | ID, URL and repository duplicate checks |
| [VERIFICATION_REPORT.md](VERIFICATION_REPORT.md) | What was and was not verified |
| [LICENSE_REPORT.md](LICENSE_REPORT.md) | License summary and review-required list |
| [SECURITY_REPORT.md](SECURITY_REPORT.md) | Security labels, high-risk entries and threat themes |
| [CATEGORY_COVERAGE.md](CATEGORY_COVERAGE.md) | Coverage by category and thin areas |
| [TEST_REPORT.md](TEST_REPORT.md) | Static checks and isolated installation results |
| [QUALITY_SCORECARD.md](QUALITY_SCORECARD.md) | Evidence-based self-assessment and gaps |

## Evidence records

| Report | Contents |
| --- | --- |
| [test-results.md](test-results.md) | Exact command output for the recorded verification run |
| [installation-results.md](installation-results.md) | Docker installation smoke-test output |
| [installation-results.json](installation-results.json) | Machine-readable installation evidence |

## Regenerate

```bash
python3 scripts/generate_reports.py
python3 scripts/generate_expansion_reports.py
```

Check for drift with:

```bash
python3 scripts/generate_reports.py --check
python3 scripts/generate_expansion_reports.py --check
```

Installation evidence is refreshed only by running:

```bash
python3 scripts/run_installation_tests.py --all --yes
```
