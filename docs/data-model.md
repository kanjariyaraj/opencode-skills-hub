# Data Model

The catalog is plain JSON so that GitHub Markdown, scripts, CLIs and a future website can all consume the same source of truth.

## Files

| File | Contents |
| --- | --- |
| `catalog/skills.json` | Individual skills |
| `catalog/agents.json` | Agent definitions or specialist roles |
| `catalog/plugins.json` | OpenCode plugins and CLIs |
| `catalog/mcp.json` | MCP servers |
| `catalog/commands.json` | Commands |
| `catalog/rules.json` | Rules |
| `catalog/hooks.json` | Hooks |
| `catalog/providers.json` | Model or inference providers |
| `catalog/collections.json` | Role collections, skill packs and toolkits |
| `catalog/index.json` | Generated unified index (do not edit by hand) |
| `data/taxonomy.json` | Category and subcategory definitions |
| `data/raw-inventory.json` | Every discovered entry, including unresolved and restricted |

Each catalog file has the shape:

```json
{
  "schema_version": "1.0.0",
  "resource_type": "skill",
  "resources": []
}
```

## Resource fields

| Field | Required | Notes |
| --- | --- | --- |
| `id` | yes | Stable kebab-case ID, unique across all catalog files |
| `name` | yes | Human-readable name |
| `type` | yes | Must match the catalog file's `resource_type` |
| `description` | yes | 20–600 characters, factual |
| `primary_category` | yes | ID from `data/taxonomy.json` |
| `secondary_categories` | no | Additional category IDs |
| `tags` | yes | Lowercase discovery tags |
| `source` | yes | `url`, `kind`, optional `documentation` and `repository` |
| `install` | yes | `instructions`, `requires_api_key`, `tested`, `notes` |
| `compatibility` | yes | `opencode`, `platforms`, `dependencies` |
| `license` | yes | `spdx`, `status` |
| `security` | yes | `level`, `notes` |
| `verification` | yes | `status[]`, `date`, `notes` |
| `signals` | no | Observed stars, latest release, last push |
| `requires_alias_of` | no | Points to a canonical ID if this entry is an alias |

The authoritative constraints are in [`schemas/resource.schema.json`](../schemas/resource.schema.json).

## Collection fields

| Field | Required | Notes |
| --- | --- | --- |
| `id` | yes | Unique across resources and collections |
| `name` | yes | Human-readable name |
| `kind` | yes | `role`, `skill-pack` or `toolkit` |
| `description` | yes | 20–600 characters |
| `audience` | no | Intended user |
| `categories` | yes | At least one taxonomy category |
| `resources` | yes | Referenced resource or collection IDs |
| `source` | no | Upstream source for a pack or toolkit |
| `verification` | yes | `status[]`, `date`, `notes` |

## IDs

- Lowercase ASCII letters, digits and hyphens.
- Start with a letter or digit.
- 2–64 characters.
- Immutable once published. If a resource changes its canonical name, keep the ID and add an alias rather than silently reusing the old ID.

## Source kinds

`github`, `npm`, `pypi`, `docs`, `website`, `unknown`.

`SOURCE_URL_MISSING` is reserved for unresolved raw-inventory entries. Catalog entries must have a real URL.

## Categories

Categories and subcategories live in `data/taxonomy.json`. Each has:

- `id`, `label`, `description`
- `subcategories`
- `related` categories

A resource has exactly one `primary_category`. Secondary categories and tags support discovery without duplicating the entry.

## Collections and references

Role collections reference existing resource or collection IDs. Skill packs and toolkits are catalogued as one entry and usually have an empty `resources` array because their sub-items were not independently verified.

## Generated files

`catalog/index.json`, `categories/*.md`, `collections/*.md` and reports are generated. Do not edit them by hand; edit the source data and run the generators.

## Adding a new type

Adding a new resource type requires:

1. A new `resource_type` value in the schema and validator.
2. A new `catalog/<type>.json` file.
3. Generator labels.
4. Tests and documentation updates.

Prefer an existing type unless the new type is genuinely distinct.
