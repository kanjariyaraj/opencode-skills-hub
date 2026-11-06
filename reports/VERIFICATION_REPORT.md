# Verification Report

Date: 2026-11-05.

## What was verified

| Check | Coverage |
| --- | --- |
| Source exists (GitHub/npm/PyPI) | 123/123 |
| License identified | 107/123 |
| README inspected for install steps | 91 additions |
| Latest release checked | 82/123 |
| Installation tested in isolation | 3/123 |
| Functional behavior tested | 0/123 |
| Source-code security audit | 0/123 |

## Status distribution

| Status | Occurrences |
| --- | --- |
| INSTALLATION_TESTED | 3 |
| LICENSE_REVIEW_REQUIRED | 16 |
| LICENSE_VERIFIED | 107 |
| MAINTAINED | 75 |
| SECURITY_REVIEW_REQUIRED | 4 |
| SOURCE_VERIFIED | 123 |
| UNMAINTAINED | 6 |

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
