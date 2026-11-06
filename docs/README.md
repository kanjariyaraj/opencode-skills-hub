# Documentation

This directory explains how the catalog is built, verified and maintained.

| Document | Purpose |
| --- | --- |
| [Verification](verification.md) | Source, license, compatibility and testing methodology |
| [Installation](installation.md) | Safe installation guidance and OpenCode configuration notes |
| [Data model](data-model.md) | Catalog schema, IDs, categories and collections |
| [Discovery](discovery.md) | How to search the catalog by task, tag, platform or status |
| [Resource template](resource-template.md) | Copy-ready JSON entry and submission checklist |
| [FAQ](faq.md) | Common questions about verification, counts and safety |
| [Maintainer guide](maintainer-guide.md) | Release, regeneration and review workflow |
| [Installation tests](../tests/installation/README.md) | Isolated Docker harness and evidence rules |
| [Test report](../reports/TEST_REPORT.md) | Current static and installation results |
| [Quality scorecard](../reports/QUALITY_SCORECARD.md) | Self-assessment, scores and remaining gaps |
| [Website plan](website.md) | Future static website architecture |
| [Security policy](../SECURITY.md) | Reporting and review policy |
| [Contributing](../CONTRIBUTING.md) | How to add or correct a resource |

## Design principles

1. **Evidence over claims.** Upstream marketing is not verification.
2. **Structure over volume.** A complete entry beats ten bare links.
3. **Safety over convenience.** No blind install scripts, no guardrail bypasses.
4. **Maintainability over cleverness.** Stdlib tooling, deterministic generation, clear schemas.
5. **Accessibility.** Plain Markdown works on GitHub, in editors and in generated sites.
