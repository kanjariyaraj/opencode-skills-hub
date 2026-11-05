# Schemas

JSON Schema definitions for the catalog.

| Schema | Purpose |
| --- | --- |
| `resource.schema.json` | A single resource entry |
| `catalog.schema.json` | A type-specific catalog file |
| `collection.schema.json` | A role collection, skill pack or toolkit |
| `collections.schema.json` | The collections file |

The validator in `scripts/validate_catalog.py` implements the same constraints without requiring a third-party JSON Schema library. If you change a schema, update the validator and tests together.

## Validation

```bash
python3 scripts/validate_catalog.py
python3 -m unittest discover -s tests -v
```

The schemas use JSON Schema Draft 2020-12.
