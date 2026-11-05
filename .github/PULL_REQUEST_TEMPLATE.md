# Pull Request

## Summary

Describe the change and why it improves the catalog.

## Type of change

- [ ] New verified resource
- [ ] Correction to an existing entry
- [ ] Resolve a raw-inventory entry
- [ ] Documentation
- [ ] Tooling or tests
- [ ] CI or security

## Verification

- [ ] `python3 scripts/validate_catalog.py` passes
- [ ] `python3 scripts/generate_indexes.py --check` passes
- [ ] `python3 scripts/generate_reports.py --check` passes
- [ ] `python3 -m unittest discover -s tests -v` passes
- [ ] `python3 scripts/check_links.py` passes

## Source evidence

- Source URL:
- Source kind (GitHub / npm / PyPI / docs):
- License observed:
- Date verified:
- Installation tested? (yes/no; if yes, describe the isolated environment)

## Checklist

- [ ] No invented repositories, package names or install commands
- [ ] No secrets, tokens or personal data
- [ ] No unlicensed third-party code copied
- [ ] Security label is conservative
- [ ] Generated files were regenerated and committed
- [ ] ID is unique and stable

## Notes for reviewers

<!-- Anything else reviewers should know. -->
