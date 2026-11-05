# Contributing to OpenCode Skills Hub

Thank you for helping make the OpenCode ecosystem easier to discover and safer to use.

This project optimizes for **trustworthy discovery**, not raw entry count. A small number of verified entries is more valuable than a large number of guessed links.

## Ways to contribute

- Add a verified resource.
- Resolve an entry in `data/raw-inventory.json`.
- Correct a category, description or compatibility note.
- Improve the validation scripts or tests.
- Report a security concern privately (see [SECURITY.md](SECURITY.md)).
- Improve documentation and accessibility.
- Review an existing entry's license or source.

## What we will not merge

- Invented repositories, package names or install commands.
- Entries with no resolvable source, unless they are added to `data/raw-inventory.json` as `SOURCE_UNRESOLVED` or `NOT_FOUND`.
- Permission-bypass, guardrail-removal or jailbreak tooling in the main catalog.
- Copied third-party code without its license and attribution.
- Secrets, tokens, API keys or personal data.
- Entries that claim installation or functional testing without evidence.
- Promotional content or fabricated statistics.

## Adding a resource

### 1. Verify the source

Confirm at least one of:

- a GitHub repository via the GitHub API or the repository page;
- an npm package via the registry;
- a PyPI package via the PyPI JSON API;
- official documentation from the upstream maintainer.

Record what you checked and when. Never guess an owner or package name.

### 2. Choose the type and category

Use one of the existing types:

`skill`, `agent`, `plugin`, `mcp`, `command`, `rule`, `hook`, `provider`.

Use a category ID from [`data/taxonomy.json`](data/taxonomy.json). If a new category is genuinely required, propose it in an issue first.

### 3. Add the entry

Add the resource to the matching `catalog/<type>.json` file. The file has the shape:

```json
{
  "schema_version": "1.0.0",
  "resource_type": "skill",
  "resources": []
}
```

A complete entry looks like this:

```json
{
  "id": "example-skill",
  "name": "Example Skill",
  "type": "skill",
  "description": "A concrete description of what the skill does and who it helps.",
  "primary_category": "software-development",
  "secondary_categories": ["design-ui-ux"],
  "tags": ["example", "skill"],
  "source": {
    "url": "https://github.com/example/example-skill",
    "kind": "github",
    "documentation": "https://github.com/example/example-skill",
    "repository": "example/example-skill"
  },
  "install": {
    "instructions": ["Follow the upstream README."],
    "requires_api_key": false,
    "tested": "NOT_TESTED",
    "notes": "Installation was not executed."
  },
  "compatibility": {
    "opencode": "compatible",
    "platforms": ["linux", "macos", "windows"],
    "dependencies": []
  },
  "license": { "spdx": "MIT", "status": "LICENSE_VERIFIED" },
  "security": {
    "level": "REVIEW REQUIRED",
    "notes": "Instruction-only; not security-audited."
  },
  "verification": {
    "status": ["SOURCE_VERIFIED", "LICENSE_VERIFIED"],
    "date": "2026-11-05",
    "notes": "Source and license confirmed; behaviour not executed."
  }
}
```

Rules:

- **ID**: stable, kebab-case, globally unique across all catalog files.
- **Description**: 20–600 characters, factual, no marketing superlatives.
- **Source**: must be an `https://` URL, or `SOURCE_URL_MISSING` only in the raw inventory.
- **Install**: `tested` must be `NOT_TESTED` unless you actually installed it in an isolated environment and can describe the result.
- **License**: use an SPDX identifier where possible. If unknown, use `UNKNOWN` with `LICENSE_REVIEW_REQUIRED`.
- **Security**: default to `REVIEW REQUIRED`. Use `HIGH RISK` for offensive tooling, destructive automation or broad credential access.
- **Verification**: list only statuses you can defend. Keep upstream claims out of verification notes.

### 4. Update the raw inventory

If the resource came from the original discovery brief, keep its entry in `data/raw-inventory.json` and set `resolution` to `VERIFIED` once it is in the catalog. If it is new, add a raw entry too, so the discovery history is preserved.

### 5. Regenerate and validate

```bash
python3 scripts/validate_catalog.py
python3 scripts/generate_indexes.py
python3 scripts/generate_reports.py
python3 scripts/check_links.py
python3 -m unittest discover -s tests -v
```

Commit the generated files along with the data change.

## Collections

- **Role collections** must reference existing resource or collection IDs.
- **Skill packs/toolkits** are catalogued as one entry; do not decompose them into unverified sub-items.
- Do not call a collection "officially recommended" unless it has been reviewed.

## Security-sensitive contributions

For defensive security resources, include the intended use and any privilege requirements. For offensive tooling:

- state explicitly that authorization is required;
- describe the intended isolated lab setup;
- do not include exploit payloads or target lists;
- expect a slower review.

## Pull request process

1. Fork the repository and create a branch.
2. Make one logical change per pull request.
3. Run the validation commands above.
4. Complete the pull request template.
5. Respond to review feedback with evidence, not assertions.

Maintainers may ask for a source URL, a license check or a compatibility note. That is normal and expected.

## Commit style

Use clear, scoped messages:

- `feat: add <resource>` for a new catalog entry
- `fix: correct <field> for <resource>`
- `docs: ...`
- `ci: ...`
- `test: ...`
- `chore: regenerate indexes`

## License of contributions

By contributing, you agree that your contribution is licensed under the repository's MIT License. You retain copyright to your original contribution. Do not contribute third-party content unless its license permits it and you include attribution.
