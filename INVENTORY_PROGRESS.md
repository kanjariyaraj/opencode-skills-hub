# Inventory Progress

Last updated: 2026-11-05

## Raw inventory

`data/raw-inventory.json` preserves every identifiable entry from the brief, including unresolved, not-found and restricted items.

Resolution counts are generated in `reports/stats.md` under "Raw inventory resolution".

## Promotions

Only entries with a confirmed GitHub, npm or PyPI source were promoted to `catalog/*.json`.

## Deliberate exclusions

- Permission-bypass, guardrail-removal and jailbreak tooling: documented only in `restricted/README.md`.
- Entries with no resolvable source: kept in the raw inventory, not in the catalog.
- Search-result-only claims: not treated as verified.

## Duplicate handling

Shared source URLs are allowed for multiple skills from the same upstream repository (for example, several Superpowers skills). The validator reports them as warnings, not errors.

## Open work

See `reports/missing-sources.md` for the current unresolved list.
