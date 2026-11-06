# Catalog Data

This directory is the source of truth for the resource catalog.

| File | Contents |
| --- | --- |
| `skills.json` | Individual skills |
| `agents.json` | Agents and specialist roles |
| `plugins.json` | Plugins and CLIs |
| `mcp.json` | MCP servers |
| `themes.json` | OpenCode color themes |
| `commands.json` | Commands |
| `rules.json` | Rules |
| `hooks.json` | Hooks |
| `providers.json` | Providers |
| `collections.json` | Role collections, skill packs and toolkits |
| `index.json` | Generated unified index (do not edit) |

## Editing rules

- Add entries to the type-specific file, not to `index.json`.
- Keep IDs stable and globally unique.
- Use a category from `data/taxonomy.json`.
- Do not mark installation or functional testing without evidence.
- Run `python3 scripts/validate_catalog.py` after editing.
- Regenerate indexes and reports before committing.

See [`docs/data-model.md`](../docs/data-model.md) for field definitions and [`schemas/`](../schemas/) for machine-readable constraints.
