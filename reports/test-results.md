# Test Results

Date: 2026-11-05
Environment: Ubuntu 26.04.1 LTS, Python 3.14.4, Node v24.22.1, Docker 29.9.2

## Summary

| Check | Result |
| --- | --- |
| Catalog validation | PASS — 123 resources, 46 collections, 0 errors, 2 expected warnings |
| Generated index drift | PASS — 67 files checked, 0 stale |
| Generated report drift | PASS — 5 reports checked, 0 stale |
| Expansion report drift | PASS — 10 reports checked, 0 stale |
| Generated asset drift | PASS — 4 assets checked, 0 stale |
| Unit tests | PASS — 55 tests |
| Local Markdown links | PASS — 0 broken |
| Markdown lint | PASS — 121 files, 0 errors |
| External URL probe (soft) | PASS — 170 URLs probed, 0 hard-broken; npm returned 403 to automated requests |
| Isolated installation smoke tests | PASS — 4/4 cases; 3 resources promoted to `INSTALLATION_TESTED` |

## Commands and output

```text
$ python3 scripts/validate_catalog.py
WARN  catalog: source URL shared by superpowers-brainstorming, superpowers-systematic-debugging, superpowers-test-driven-development: https://github.com/obra/superpowers
WARN  catalog: source URL shared by devhive-backender, devhive-frontender: https://pypi.org/project/devhive/
Checked 123 resources and 46 collections: 0 error(s), 2 warning(s).

$ python3 scripts/generate_indexes.py --check
Checked 67 generated file(s); 0 stale.

$ python3 scripts/generate_reports.py --check
Checked 5 report(s); 0 stale.

$ python3 scripts/generate_expansion_reports.py --check
Checked 10 expansion report(s); 0 stale.

$ python3 scripts/generate_assets.py --check
Checked 4 asset(s); 0 stale.

$ python3 scripts/check_links.py
Local links checked. Broken local: 0; broken external: 0.

$ python3 -m unittest discover -s tests -v
Ran 55 tests in 0.319s
OK

$ npx --yes markdownlint-cli2@0.13.0 "**/*.md" "#node_modules" "#**/.github/ISSUE_TEMPLATE/**"
Linting: 121 file(s)
Summary: 0 error(s)
```

## Installation tests

Run with `python3 scripts/run_installation_tests.py --all --yes`. Each case runs in a disposable Docker container with a temporary work directory, no host config mount, dropped capabilities and `no-new-privileges`.

| Case | Resource | Status | Duration | Pinned |
| --- | --- | --- | ---: | --- |
| `theme-catppuccin` | `catppuccin-opencode` | PASS | 6.0s | commit `d5f4096` |
| `cli-design-md-generator` | `design-md-generator` | PASS | 6.7s | commit `41477cb` |
| `npm-skill-creator` | `opencode-skill-creator` | PASS | 34.5s | npm `0.3.6` |
| `plugin-opencode-websearch` | `opencode-websearch` | PASS | 277.8s | OpenCode `1.18.33`, plugin `0.7.1` |

`design-md-generator` was exercised in preview (`--list`) mode only, so its catalog entry remains `NOT_TESTED`. The other three cases installed the pinned artifact and passed their smoke assertions.

Full output: [`installation-results.md`](installation-results.md) and [`installation-results.json`](installation-results.json).

## Not executed

- Functional or model-dependent behavior for any resource.
- Authentication/OAuth consent flows.
- TUI interactions, browser automation and microphone capture.
- Source-code security audits.
