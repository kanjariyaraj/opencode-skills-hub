# Data

| File | Purpose |
| --- | --- |
| `taxonomy.json` | Category and subcategory definitions used by validation and generation |
| `raw-inventory.json` | Every discovered entry, including unresolved, not-found and restricted items |

`raw-inventory.json` is intentionally broader than the catalog. It preserves the discovery history and prevents entries from being silently discarded. Its `resolution` values are:

- `VERIFIED` — promoted to the catalog
- `SOURCE_UNRESOLVED` — no canonical source supplied or confirmed
- `NOT_FOUND` — a claimed source was checked and did not exist
- `RESTRICTED` — excluded by security policy
- `DUPLICATE` — represented by another entry

## Taxonomy changes

Adding a category affects schemas, validation, generation and docs. Propose it in an issue first, then update:

1. `data/taxonomy.json`
2. the category enum in `schemas/resource.schema.json`
3. `scripts/validate_catalog.py` if it hard-codes categories
4. tests and documentation
5. regenerate indexes and reports

Do not invent resources to fill a category.
