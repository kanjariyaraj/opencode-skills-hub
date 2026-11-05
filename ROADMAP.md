# Roadmap

This roadmap is a direction, not a promise. Priorities favor trust and usefulness over entry count.

## Phase 1 — Foundation (complete, v0.1.0)

- [x] Repository architecture and governance documents
- [x] JSON schemas for resources and collections
- [x] Verified catalog split by resource type
- [x] Raw inventory with unresolved entries preserved
- [x] Category and collection pages generated from data
- [x] Validation, link-check and report generators
- [x] Unit tests
- [x] CI workflows
- [x] Security review labels and restricted archive policy

## Phase 2 — Coverage and verification depth

- [ ] Add verified standalone entries for DevOps & Cloud
- [ ] Add verified standalone entries for AI/ML and data science
- [ ] Add verified standalone entries for game development
- [ ] Add verified standalone entries for audio and business workflows
- [ ] Resolve the highest-value `SOURCE_UNRESOLVED` entries
- [ ] Add license review notes for every `LICENSE_REVIEW_REQUIRED` entry
- [ ] Add a maintainer-reviewed subset labelled `REVIEWED`

## Phase 3 — Isolated testing

- [ ] Define a container-based test harness for low-risk resources
- [ ] Record installation evidence for a small, reviewed subset
- [ ] Add `INSTALLATION_TESTED` only where evidence exists
- [ ] Add a rollback and uninstall verification step

## Phase 4 — Discovery experience

- [ ] Add a generated "Find by task" data file for tooling
- [ ] Add tag and platform indexes
- [ ] Add a contribution helper that scaffolds a valid entry
- [ ] Add cross-reference aliases for duplicate resources

## Phase 5 — Website

- [ ] Freeze and version the catalog API
- [ ] Build a static site with search and filters
- [ ] Add resource detail pages
- [ ] Add responsive layout and dark/light themes
- [ ] Verify accessibility

## Phase 6 — Maintenance automation

- [ ] Scheduled source re-verification
- [ ] Automatic stale-entry reports
- [ ] Automatic license drift detection
- [ ] Security advisory watch for catalogued dependencies

## Non-goals

- Maximizing the number of links.
- Hosting or mirroring upstream code.
- Providing unrestricted or guardrail-removal tooling.
- Guaranteeing upstream safety or compatibility.
- Automated installation of arbitrary third-party scripts.
