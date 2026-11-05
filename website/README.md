# Website

No website exists yet. This directory reserves the place for the future static site described in [`docs/website.md`](../docs/website.md).

## Why nothing is built yet

The data model and verification process come first. A website built on unstable data would amplify bad entries. GitHub Markdown, generated category pages and JSON are enough for the current catalog.

## Planned stack

- Next.js + TypeScript, or a static generator for a smaller footprint
- Tailwind CSS
- Accessible components
- Catalog loaded at build time from `catalog/index.json`
- Light and dark themes
- Search and filters

## Data contract

The site must consume generated catalog data and must not invent counts, stars or badges. Verification dates, license status and security labels must remain visible.

## Contributing to the website

Website work starts after the schemas are frozen. Until then, improvements to the catalog, generators and documentation are more valuable.
