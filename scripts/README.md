# Scripts

Stdlib-only Python tooling.

| Script | Purpose |
| --- | --- |
| `validate_catalog.py` | Validate schemas, enums, IDs, categories, duplicates and references |
| `check_links.py` | Check local Markdown links; optionally probe external catalog URLs |
| `generate_indexes.py` | Generate `catalog/index.json`, category pages and collection pages |
| `generate_reports.py` | Generate statistics, missing-source, license, compatibility and security reports |
| `generate_assets.py` | Generate theme-aware README banner and coverage SVGs |
| `query_catalog.py` | Filter, sort and print catalog resources as a table, JSON or IDs |

## Common commands

```bash
python3 scripts/validate_catalog.py
python3 scripts/validate_catalog.py --json
python3 scripts/validate_catalog.py --strict
python3 scripts/check_links.py
python3 scripts/check_links.py --network --soft
python3 scripts/generate_indexes.py
python3 scripts/generate_indexes.py --check
python3 scripts/generate_reports.py
python3 scripts/generate_reports.py --check
python3 scripts/generate_assets.py
python3 scripts/generate_assets.py --check
python3 scripts/query_catalog.py --category image-generation --sort name
python3 scripts/query_catalog.py --license LICENSE_REVIEW_REQUIRED --format ids
```

## Exit codes

- `0` success (warnings may be present)
- `1` validation failure or generated-file drift
- `2` usage or IO error

## Safety

- The scripts never execute third-party install commands.
- Network probing only sends HEAD/GET requests to URLs already in the catalog.
- Generated files are deterministic; `--check` is safe for CI.
- Do not add dependencies without a strong reason.
