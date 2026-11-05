# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses semantic versioning for its own data and tooling.

## [Unreleased]

### Planned

- Expand verified standalone coverage in DevOps, AI/ML, data science, game development, audio and business categories.
- Add isolated installation testing for selected low-risk resources.
- Add a schema-driven static website with search and filters.
- Add scheduled source re-verification.

## [0.1.0] - 2026-11-05

### Added

- Initial repository structure, MIT license, governance and security documentation.
- JSON schemas for resources, catalog files and collections.
- Structured catalog split by resource type: skills, agents, plugins, MCP servers, commands, rules, hooks and providers.
- Role collections and upstream skill-pack/toolkit collections.
- Raw discovery inventory preserving every entry from the initial brief, including unresolved and restricted items.
- Validation script for schemas, IDs, categories, duplicates and references.
- Link checker for local Markdown links and optional external URL probing.
- Deterministic index and report generators.
- Eighteen category pages generated from catalog data.
- Evidence reports for statistics, missing sources, licenses, compatibility and security.
- Unit tests for validation, generation and link checking.
- GitHub Actions workflows for validation, generation drift, tests, Markdown linting and link checks.
- Restricted archive policy for permission-bypass and guardrail-removal tooling.

### Notes

- No third-party resource was installed on the host during cataloging. Installation tests are reported as `NOT_TESTED`.
- Source and license verification was performed against GitHub, npm and PyPI metadata on 2026-11-05.
- Upstream claims are kept separate from independently observed facts.
