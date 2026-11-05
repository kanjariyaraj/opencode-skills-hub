# Verification Progress

Last updated: 2026-11-05

## What was verified

For every promoted entry:

- source existence and metadata
- declared license where available
- last observed upstream push
- OpenCode compatibility claim (usually `compatible` for portable skill/plugin formats)
- security capability label

## What was not verified

- installation in an isolated environment
- functional behavior
- compatibility with a specific OpenCode version
- license compatibility for redistribution
- security audit of upstream code

## Figures

See `reports/stats.md` for current counts. Verification statuses are stored per entry in `verification.status`.

## Next verification targets

1. Resolve high-value `SOURCE_UNRESOLVED` entries.
2. Review `LICENSE_REVIEW_REQUIRED` entries.
3. Install a small set of low-risk skills in a container and record evidence.
4. Re-check low-activity entries.
