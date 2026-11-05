# Maintainer Guide

## Routine workflow

```bash
python3 scripts/validate_catalog.py
python3 scripts/generate_indexes.py
python3 scripts/generate_reports.py
python3 scripts/generate_assets.py
python3 scripts/check_links.py
python3 -m unittest discover -s tests -v
python3 scripts/generate_indexes.py --check
python3 scripts/generate_reports.py --check
python3 scripts/generate_assets.py --check
```

If the generated files changed, commit them with the data change.

## Adding a resource

1. Verify the source and license.
2. Add the entry to `catalog/<type>.json`.
3. Update `data/raw-inventory.json`.
4. Run the workflow above.
5. Review the diff for secrets, invented claims and accidental code copying.
6. Commit with a scoped message.

## Re-verifying existing resources

1. Re-read GitHub, npm or PyPI metadata.
2. Update `signals` and `verification.date`.
3. Update `MAINTAINED` / `UNMAINTAINED` based on observed activity.
4. Update the license if it changed.
5. Regenerate reports and assets.
6. Note material changes in `CHANGELOG.md`.

## Reviewing a pull request

Check for:

- a real, reachable source
- an honest license status
- no invented install commands
- no secrets or personal data
- no copied code without a license
- correct type and category
- consistent IDs
- generated files regenerated
- tests passing

## Release process

1. Update `CHANGELOG.md`.
2. Bump the version in `CITATION.cff` and `CHANGELOG.md`.
3. Run the full local workflow.
4. Commit and tag.
5. Push the tag and create a release.
6. Announce only verified facts.

## Regenerating everything

```bash
python3 scripts/generate_indexes.py
python3 scripts/generate_reports.py
python3 scripts/generate_assets.py
```

Never hand-edit generated files.

## Schedule

Recommended cadence:

- Weekly: dependency and security review of project tooling
- Monthly: re-verify low-activity entries
- Quarterly: review the taxonomy and role collections
- On demand: respond to issues and security reports
