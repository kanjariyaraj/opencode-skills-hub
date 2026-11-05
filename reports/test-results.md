# Test Results

Date: 2026-11-05
Environment: Ubuntu 26.04.1 LTS, Python 3.14.4, Node v24.22.1

## Summary

| Check | Result |
| --- | --- |
| Catalog validation | PASS — 32 resources, 46 collections, 0 errors, 2 expected warnings |
| Generated index drift | PASS — 67 files checked, 0 stale |
| Generated report drift | PASS — 5 reports checked, 0 stale |
| Local Markdown links | PASS — 0 broken |
| Unit tests | PASS — 35 tests |
| Markdown lint | PASS — 108 files, 0 errors |
| External URL probe (soft) | PASS — 79 URLs probed, 0 hard-broken; npm returned 403 to automated requests |

## Commands and output

```text
$ python3 scripts/validate_catalog.py
WARN  catalog: source URL shared by superpowers-brainstorming, superpowers-systematic-debugging, superpowers-test-driven-development: https://github.com/obra/superpowers
WARN  catalog: source URL shared by devhive-backender, devhive-frontender: https://pypi.org/project/devhive/
Checked 32 resources and 46 collections: 0 error(s), 2 warning(s).

$ python3 scripts/generate_indexes.py --check
Checked 67 generated file(s); 0 stale.

$ python3 scripts/generate_reports.py --check
Checked 5 report(s); 0 stale.

$ python3 scripts/check_links.py
Local links checked. Broken local: 0; broken external: 0.

$ python3 -m unittest discover -s tests -v
Ran 35 tests in 0.275s
OK

$ npx --yes markdownlint-cli2@0.13.0 "**/*.md" "#node_modules" "#**/.github/ISSUE_TEMPLATE/**"
Linting: 108 file(s)
Summary: 0 error(s)

$ python3 scripts/check_links.py --network --all-links --soft --timeout 8 --workers 12
Probed 79 external URL(s).
Local links checked. Broken local: 0; broken external: 0.
```

## Notes

- The two validation warnings are expected: one upstream repository provides three distinct skills, and one PyPI package provides two distinct agents. The validator reports shared sources without failing.
- npm blocks automated HEAD/GET requests with HTTP 403. This is recorded as a soft warning, not a broken link. Package existence was verified separately through the npm registry.
- No upstream resource was installed or executed. Functional testing of upstream resources is `NOT_TESTED`.
- Markdown lint excludes `.github/ISSUE_TEMPLATE/**` because those files are YAML issue forms, not Markdown documents.

## Honest limitations

- Catalog validation proves data consistency, not upstream correctness.
- External URL probing proves reachability at one point in time, not ongoing availability.
- Passing tests do not imply that any catalogued resource is safe or compatible with a specific OpenCode version.

## Reproduce

```bash
python3 scripts/validate_catalog.py
python3 scripts/generate_indexes.py --check
python3 scripts/generate_reports.py --check
python3 scripts/check_links.py
python3 -m unittest discover -s tests -v
npx --yes markdownlint-cli2@0.13.0 "**/*.md" "#node_modules" "#**/.github/ISSUE_TEMPLATE/**"
python3 scripts/check_links.py --network --all-links --soft
```

The same non-network checks are available as `make check`.
