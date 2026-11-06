# Website Plan

No website is built yet. This is a scoped, implementation-ready plan, not a claim that a site exists. GitHub Markdown and the generated JSON remain the shipping interface.

## Readiness audit (2026-11-05)

| Prerequisite | Status |
| --- | --- |
| Stable IDs and schemas | Done — 123 resources, 0 duplicate IDs |
| Machine-readable aggregate | Done — `catalog/index.json` |
| Category and collection pages | Done — generated Markdown |
| Query/filter semantics | Done — `scripts/query_catalog.py` |
| Security and license fields | Done — every resource |
| Verification dates | Done — every resource |
| Theme-aware visual assets | Done — four SVGs |
| Search index | Not built |
| Static site generator | Not built |

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

## MVP scope

Build a static export from `catalog/index.json`:

- `/` — search, category grid, type counts, verification legend.
- `/categories/<id>/` — filtered list with license, security and verification badges.
- `/resources/<id>/` — description, install instructions, source links, signals, dates and warnings.
- `/collections/<id>/` — curated role or pack page.
- `/verification/`, `/security/`, `/licenses/` — methodology pages generated from the same data.
- `search-index.json` — small client-side index; no backend.

## Acceptance criteria

1. Every catalog resource has a page and every internal link resolves.
2. No count, star value or install command is hardcoded outside the JSON.
3. Security and license labels are visible without opening a details panel.
4. Keyboard navigation, visible focus and WCAG AA contrast are verified.
5. `prefers-reduced-motion` is respected; no autoplay media.
6. The build is reproducible from a clean checkout with one command.
7. The site refuses to build on catalog validation errors.

## Suggested implementation

| Layer | Choice | Reason |
| --- | --- | --- |
| Generator | Python stdlib + templates | Matches existing tooling; no new runtime |
| Output | Static HTML/CSS/JS | GitHub Pages compatible; no server |
| Styling | Hand-written CSS tokens | No framework lock-in |
| Search | Prebuilt JSON + client filter | 123 entries do not need a service |
| Tests | Link check, HTML validation, axe smoke test | Reuses current evidence culture |

## Sequencing

1. Add a `scripts/build_site.py` that renders from `catalog/index.json` and fails on validator errors.
2. Generate the MVP pages and `search-index.json`.
3. Add link checking and an accessibility smoke test.
4. Publish a preview build artifact in CI, not to production.
5. Add filters only after the static pages are correct.
6. Only then consider a backend.
