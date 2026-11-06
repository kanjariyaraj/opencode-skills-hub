# Test Report

Date: 2026-11-05. Canonical command output is recorded in [test-results.md](test-results.md).

## Static and generated checks

| Check | Result |
| --- | --- |
| Catalog validation | PASS — 123 resources, 46 collections, 0 errors, 2 expected warnings |
| Generated index drift | PASS — 0 stale |
| Generated report/asset drift | PASS — 0 stale |
| Unit tests | PASS — 55 tests |
| Local Markdown links | PASS — 0 broken |
| Markdown lint | PASS — 0 errors |

## Isolated installation smoke tests

| Case | Resource | Status | Duration |
| --- | --- | --- | --- |
| `theme-catppuccin` | `catppuccin-opencode` | **PASS** | 6.0s |
| `cli-design-md-generator` | `design-md-generator` | **PASS** | 6.7s |
| `npm-skill-creator` | `opencode-skill-creator` | **PASS** | 34.5s |
| `plugin-opencode-websearch` | `opencode-websearch` | **PASS** | 277.8s |

## Interpretation

- A passing case proves the pinned install command completed and the smoke assertion held in a disposable container.
- It does not prove runtime correctness, security or compatibility with every OpenCode version.
- Cases that were not executed remain `NOT_TESTED` in the catalog.
- The test runner never mounts the host OpenCode configuration.
