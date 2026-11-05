# Reports

All files in this directory are generated from `catalog/*.json` and `data/raw-inventory.json`. Do not edit them by hand.

| Report | Contents |
| --- | --- |
| `stats.md` | Counts by type, category, verification, security and license |
| `missing-sources.md` | Raw inventory entries that are not verified |
| `licenses.md` | License status for every catalogued resource |
| `compatibility.md` | OpenCode compatibility, platforms and dependencies |
| `security-review.md` | Security labels and capability notes |
| `documentation-checklist.md` | Maintainer checklist for documentation |

Regenerate with:

```bash
python3 scripts/generate_reports.py
```

Check for drift with:

```bash
python3 scripts/generate_reports.py --check
```
