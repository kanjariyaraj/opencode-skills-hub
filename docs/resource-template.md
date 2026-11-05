# Resource entry template

Copy the relevant object into `catalog/<type>.json` and replace the example
values. Keep the JSON valid and run `make check` before opening a pull request.

- Schema: [`schemas/resource.schema.json`](../schemas/resource.schema.json)
- Field reference: [`data-model.md`](data-model.md)
- Verification rules: [`verification.md`](verification.md)

## Minimal entry

```json
{
  "id": "example-skill",
  "name": "Example Skill",
  "type": "skill",
  "description": "A factual description of what the resource does and who it helps.",
  "primary_category": "software-development",
  "secondary_categories": [],
  "tags": ["example"],
  "source": {
    "url": "https://github.com/owner/repository",
    "kind": "github",
    "documentation": "https://github.com/owner/repository",
    "repository": "owner/repository"
  },
  "install": {
    "instructions": ["Follow the upstream README for the current installation method."],
    "requires_api_key": false,
    "tested": "NOT_TESTED",
    "notes": "Installation was not executed during cataloging."
  },
  "compatibility": {
    "opencode": "compatible",
    "platforms": ["linux", "macos", "windows"],
    "dependencies": []
  },
  "license": {
    "spdx": "MIT",
    "status": "LICENSE_VERIFIED"
  },
  "security": {
    "level": "REVIEW REQUIRED",
    "notes": "Describe what the resource can read, write or execute."
  },
  "verification": {
    "status": ["SOURCE_VERIFIED", "LICENSE_VERIFIED"],
    "date": "2026-11-05",
    "notes": "State exactly what was checked and how."
  },
  "signals": {
    "github_stars_observed": null,
    "observed_at": "2026-11-05",
    "latest_release": null,
    "last_push": null
  }
}
```

## Field checklist

| Field | Rule |
| --- | --- |
| `id` | Lowercase kebab-case, stable, unique across the whole catalog. |
| `name` | Display name, not a sentence. |
| `type` | Must match the resource file and a schema enum value. |
| `description` | Factual, 20–600 characters, no marketing superlatives. |
| `primary_category` | Exactly one ID from `data/taxonomy.json`. |
| `secondary_categories` | Zero or more taxonomy IDs, excluding the primary. |
| `tags` | Lowercase, descriptive, no duplicates. |
| `source.url` | Reachable `https://` URL owned by the project. |
| `source.kind` | `github`, `npm`, `pypi`, `website`, `docs` or `unknown`. |
| `install.tested` | `NOT_TESTED` unless you have reproducible evidence. |
| `install.instructions` | Safe steps or a pointer to upstream docs. No blind pipe-to-shell. |
| `compatibility.platforms` | Only platforms the upstream project claims to support. |
| `license.status` | Honest status; use `LICENSE_REVIEW_REQUIRED` when unsure. |
| `security.level` | Conservative label; explain the capability in `notes`. |
| `verification.status` | Only statuses you can defend with evidence. |
| `verification.date` | ISO date of the check. |
| `signals` | Observations only, with the date observed. `null` when unknown. |

## Do not submit

- Invented repositories, package names, download counts or star counts.
- Copied marketing text presented as an independent description.
- `INSTALLATION_TESTED` or `FUNCTIONAL_TESTED` without evidence.
- Install commands you have not read.
- Permission-bypass, guardrail-removal or jailbreak tooling.
- Credentials, API keys or private links.

## After editing

```bash
make validate    # schema, IDs, categories and references
make generate    # rebuild indexes, pages and reports
make test        # unit tests
make links       # local Markdown links
git add catalog/ categories/ collections/ reports/ data/
```

Generated files must be committed with the data change.
