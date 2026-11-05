# Assets

Theme-aware SVG artwork used by the README. Every file here is generated from
the catalog; do not edit by hand.

| File | Purpose |
| --- | --- |
| `banner-light.svg` | Hero banner for light mode |
| `banner-dark.svg` | Hero banner for dark mode |
| `coverage-light.svg` | Category coverage chart for light mode |
| `coverage-dark.svg` | Category coverage chart for dark mode |

## Regenerate

```bash
python3 scripts/generate_assets.py
python3 scripts/generate_assets.py --check
```

The generator reads `catalog/*.json` and `data/taxonomy.json`. Counts, ordering
and the verification date in the chart are derived from the data, so the assets
change only when the catalog changes.

## Design notes

- Pure SVG, no scripts, no external fonts or images.
- System font stack for predictable rendering on GitHub.
- Light and dark variants so the artwork stays legible in both themes.
- Deterministic output keeps `--check` safe for CI.
- Category colors use a single indigo-to-cyan gradient for consistent branding.
