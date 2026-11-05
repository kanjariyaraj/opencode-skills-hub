# Website Plan

No website is built yet. The catalog and data model must be stable first, and GitHub Markdown already provides a usable discovery experience.

## Intended architecture

- **Framework:** Next.js with TypeScript, or a static site generator if the feature set stays small.
- **Styling:** Tailwind CSS with an accessible component system.
- **Data:** generated from `catalog/index.json` at build time.
- **Search:** client-side index for small data sets; server-side search only if the catalog grows substantially.
- **Hosting:** static export where possible.
- **Themes:** light and dark, with system preference.
- **Accessibility:** keyboard navigation, visible focus, semantic landmarks, sufficient contrast, reduced-motion support.

## Pages

1. Home with search and category navigation.
2. Category page with filters.
3. Resource detail page.
4. Collection page.
5. Verification and security methodology pages.
6. Contribution guide.

## Filters

- resource type
- category and subcategory
- technology / tag
- platform
- license
- compatibility
- maintenance signal
- verification status
- security level
- API-key requirement

## Data contract

The website should consume `catalog/index.json` and treat `catalog/*.json` as the source of truth. Generated Markdown and reports remain available for GitHub users.

## Constraints

- Do not display fabricated counts, stars or badges.
- Do not rank by popularity alone.
- Show verification dates.
- Keep security labels visible.
- Do not provide one-click installs for unreviewed resources.
- Do not hide license or authorization warnings.

## Sequencing

1. Stabilize schemas and IDs.
2. Add tag, platform and task indexes.
3. Build the static site.
4. Add search and filters.
5. Add accessibility and performance testing.
6. Only then consider a backend.
