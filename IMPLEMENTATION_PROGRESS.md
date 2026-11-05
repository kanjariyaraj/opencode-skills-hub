# Implementation Progress

Last updated: 2026-11-05

## Implemented

- Repository structure and governance docs
- JSON schemas for resources, catalog files and collections
- Catalog split by resource type
- Collections for roles, skill packs and toolkits
- Raw inventory
- `scripts/validate_catalog.py`
- `scripts/check_links.py`
- `scripts/generate_indexes.py`
- `scripts/generate_reports.py`
- Generated category and collection pages
- Generated reports
- Unit tests
- GitHub Actions workflows
- Restricted archive

## Generated artifacts

- `catalog/index.json`
- `categories/README.md` and 18 category pages
- `collections/README.md` and per-collection pages
- `reports/*.md` (five generated reports)

## Not implemented

- Static website
- Automated isolated installation tests
- Scheduled source re-verification
- Automated secret scanning beyond CI configuration

## Constraints

- Stdlib-only Python tooling
- No third-party installs during cataloging
- No fabricated statistics
