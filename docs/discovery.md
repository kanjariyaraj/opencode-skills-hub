# Discovery Guide

You can browse the generated Markdown, query the JSON directly, or use the scripts.

## Browse

- [Categories](../categories/README.md) — domain pages
- [Collections](../collections/README.md) — roles, skill packs and toolkits
- [Statistics](../reports/stats.md) — current counts
- [Compatibility](../reports/compatibility.md) — platforms and dependencies
- [Licenses](../reports/licenses.md) — license status
- [Security review](../reports/security-review.md) — risk labels
- [Missing sources](../reports/missing-sources.md) — unresolved entries

## Find by task

The README has a task table. Open the linked category or role collection.

## Filter and sort

`scripts/query_catalog.py` filters and sorts the catalog without third-party
packages. Filters combine with AND; repeated values within one filter combine
with OR.

```bash
# Every resource in a category, sorted by name
python3 scripts/query_catalog.py --category image-generation --sort name

# Plugins, riskiest first
python3 scripts/query_catalog.py --type plugin --sort security --reverse

# IDs only, for scripting
python3 scripts/query_catalog.py --license LICENSE_REVIEW_REQUIRED --format ids

# JSON output
python3 scripts/query_catalog.py --search design --format json

# Active resources on GitHub
python3 scripts/query_catalog.py --maintenance maintained --source-kind github
```

| Option | Values |
| --- | --- |
| `--sort` | `name`, `id`, `type`, `category`, `license`, `security`, `verification`, `source`, `last-push` |
| `--category` | Any ID from `data/taxonomy.json`; matches primary and secondary categories |
| `--type` | `skill`, `agent`, `plugin`, `mcp`, `command`, `rule`, `hook`, `provider` |
| `--status` | Any verification status in `schemas/resource.schema.json` |
| `--security` | `LOW RISK`, `REVIEWED`, `REVIEW REQUIRED`, `HIGH RISK`, `UNSAFE`, `DEPRECATED` |
| `--license` | `LICENSE_VERIFIED`, `LICENSE_REVIEW_REQUIRED`, `NOASSERTION`, `UNKNOWN` |
| `--source-kind` | `github`, `npm`, `pypi`, `website`, `docs`, `unknown` |
| `--maintenance` | `any`, `maintained`, `unmaintained` |
| `--search` | Case-insensitive match over id, name, description and tags |
| `--limit` | Maximum number of results |
| `--format` | `table`, `json`, `ids` |
| `--reverse` | Reverse the chosen sort order |

Generated pages and reports are sorted deterministically, so a diff only
appears when the data changes.

## Query with Python

```bash
python3 - <<'PY'
import json
index = json.load(open("catalog/index.json"))
for resource in index["resources"]:
    if "video" in resource["tags"] and resource["verification"]["status"]:
        print(resource["id"], "-", resource["description"])
PY
```

## Query by category

```bash
python3 - <<'PY'
import json
index = json.load(open("catalog/index.json"))
for category in index["categories"]:
    if category["id"] == "cybersecurity":
        print(category["resource_ids"])
PY
```

## Query by tag

```bash
python3 - <<'PY'
import json
index = json.load(open("catalog/index.json"))
for resource in index["resources"]:
    if "ffmpeg" in resource["tags"]:
        print(resource["name"], resource["source"]["url"])
PY
```

## Query by verification status

```bash
python3 - <<'PY'
import json
index = json.load(open("catalog/index.json"))
for resource in index["resources"]:
    if "LICENSE_REVIEW_REQUIRED" in resource["verification"]["status"]:
        print(resource["id"], resource["license"]["spdx"])
PY
```

## Search the Markdown

```bash
grep -ril "ffmpeg" categories collections
grep -ril "lineageos" categories collections
```

## Discovery rules

- Prefer entries with `SOURCE_VERIFIED` and `LICENSE_VERIFIED`.
- Treat `REVIEW REQUIRED` as "not yet reviewed", not "safe".
- Treat `HIGH RISK` as requiring authorization and isolation.
- Check `install.tested` before assuming an install command works.
- Follow the upstream source for current instructions.

## Future website

The generated `catalog/index.json` is the intended API for a static site. See [website.md](website.md).
