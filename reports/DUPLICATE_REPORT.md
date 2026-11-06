# Duplicate Report

Generated from `catalog/*.json` on 2026-11-05.

## Result

- Duplicate stable IDs: **0**
- Duplicate source URLs: **2** (expected shared-source warnings below)
- Duplicate repository identifiers: **2**

## Shared source URLs

| Source URL | Entries |
| --- | --- |
| [https://github.com/obra/superpowers](https://github.com/obra/superpowers) | 3 |
| [https://pypi.org/project/devhive/](https://pypi.org/project/devhive/) | 2 |

These are intentional: three Superpowers skills share one upstream repository, and two DevHive agents share one PyPI package. They have distinct IDs because they are distinct installable capabilities.

## Cross-check against the 91 additions

- IDs checked against the pre-existing 32 catalog entries: 0 collisions.
- Canonical URLs checked: 0 collisions.
- Repository names checked: 0 collisions.
- Raw inventory deduplicated by `claimed_source`: 0 duplicate rows added.

## Collection references

Collections are validated against known resource IDs by `scripts/validate_catalog.py`; unresolved references fail validation.
