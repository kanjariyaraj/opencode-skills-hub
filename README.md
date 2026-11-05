# OpenCode Skills Hub

> Discover. Build. Create. Automate.

A structured, searchable and evidence-based catalog of skills, agents, plugins, MCP servers, commands, rules, hooks, providers and workflow collections for [OpenCode](https://opencode.ai).

This project is not a link dump. Every catalogued resource has a stable ID, a category, a source, a license status, a security label and a verification record. Entries that could not be verified are preserved in a separate raw inventory instead of being presented as working software.

---

## Table of contents

- [What this is](#what-this-is)
- [What this is not](#what-this-is-not)
- [Quick start](#quick-start)
- [Catalog at a glance](#catalog-at-a-glance)
- [Resource types](#resource-types)
- [Find by task](#find-by-task)
- [Browse categories](#browse-categories)
- [Role collections](#role-collections)
- [Verification methodology](#verification-methodology)
- [Security and trust](#security-and-trust)
- [Installation guidance](#installation-guidance)
- [Repository structure](#repository-structure)
- [Local development](#local-development)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [Acknowledgements](#acknowledgements)
- [License](#license)

---

## What this is

- A **catalog** of OpenCode ecosystem resources across technical and non-technical domains.
- A **discovery system** organized by category, resource type, task and user role.
- A **verification record** that separates upstream claims from independently observed facts.
- A **maintainable data set** in JSON with schemas, validation scripts, tests and CI.
- A **contribution-ready** open-source project with governance, security and support docs.

## What this is not

- It is not an endorsement or a safety guarantee.
- It is not a mirror of upstream code. Resources stay at their original sources.
- It is not a promise that an upstream project still works today.
- It is not a home for permission-bypass, guardrail-removal or jailbreak tooling. Those are documented only in the [restricted archive](restricted/README.md).

---

## Quick start

```bash
git clone https://github.com/kanjariyaraj/opencode-skills-hub.git
cd opencode-skills-hub

# Browse the catalog
ls categories/
ls collections/

# Validate the data
python3 scripts/validate_catalog.py

# Regenerate indexes and reports from data
python3 scripts/generate_indexes.py
python3 scripts/generate_reports.py
```

There is no build step and no third-party Python dependency required for validation, generation or tests.

---

## Catalog at a glance

Counts below are produced from [`catalog/*.json`](catalog/). They describe catalog entries, not downloads, stars or upstream quality. The live breakdown is in [`reports/stats.md`](reports/stats.md).

| Metric | Value |
| --- | ---: |
| Catalogued resources | 32 |
| Collections (role, skill packs, toolkits) | 46 |
| Primary categories | 18 |
| Raw inventory entries preserved | 111 |
| Resources with a verified source | 32 |
| Resources with an installation test | 0 |

> `0` installation tests is deliberate and honest. Third-party resources were **not** installed on the maintainer's host during cataloging. Upstream README claims are not treated as test results.

### Categories

| Category | Resources | Collections |
| --- | ---: | ---: |
| [Software Development](categories/software-development.md) | 8 | 19 |
| [Mobile Development](categories/mobile-development.md) | 1 | 6 |
| [Android System & Custom ROM](categories/android-system-custom-rom.md) | 2 | 4 |
| [Linux & Low-Level Systems](categories/linux-low-level.md) | 1 | 3 |
| [Database & Backend Infrastructure](categories/database-backend.md) | 2 | 4 |
| [DevOps & Cloud](categories/devops-cloud.md) | 0 | 2 |
| [Cybersecurity](categories/cybersecurity.md) | 4 | 3 |
| [AI & Machine Learning](categories/ai-machine-learning.md) | 0 | 4 |
| [Data Science & Analytics](categories/data-science.md) | 0 | 4 |
| [Game Development](categories/game-development.md) | 0 | 4 |
| [Design & UI/UX](categories/design-ui-ux.md) | 5 | 6 |
| [Image Generation & Editing](categories/image-generation.md) | 5 | 8 |
| [Video Generation & Editing](categories/video-generation.md) | 2 | 5 |
| [Audio, Voice & Music](categories/audio-music.md) | 0 | 3 |
| [Content & Marketing](categories/content-marketing.md) | 0 | 6 |
| [Documents & Productivity](categories/documents-productivity.md) | 2 | 8 |
| [Education & Research](categories/education-research.md) | 0 | 3 |
| [Business & Finance](categories/business-finance.md) | 0 | 4 |

A category can serve users through bundled skill packs even when it has no standalone resource entries yet. Zero means "no standalone verified entry", not "nothing useful".

---

## Resource types

| Type | Meaning |
| --- | --- |
| **Skill** | Instructions and scripts an agent loads for a specific task. |
| **Agent** | A specialist persona or workflow role. |
| **Plugin** | Code that extends OpenCode itself. |
| **MCP server** | A Model Context Protocol server exposing tools or data. |
| **Command** | A named workflow triggered from the agent. |
| **Rule** | Persistent behavioural guidance. |
| **Hook** | An event-driven automation. |
| **Provider** | A model or inference provider. |

Collections describe either a **user role** (a curated mapping) or an **upstream skill pack/toolkit** (a bundle catalogued as one entry).

---

## Find by task

Start from the task, then open the category page or role collection.

| I want to... | Start here |
| --- | --- |
| Build a web app | [Software Development](categories/software-development.md) · [Full-Stack Developer](collections/role-fullstack-developer.md) |
| Build a Flutter app | [Flutter Developer](collections/role-flutter-developer.md) · [Mobile Development](categories/mobile-development.md) |
| Build an Android app | [Android Developer](collections/role-android-developer.md) |
| Build a custom Android ROM | [Custom ROM Developer](collections/role-custom-rom-developer.md) · [Android System & Custom ROM](categories/android-system-custom-rom.md) |
| Write an Android kernel module | [Kernel Engineer](collections/role-kernel-engineer.md) · [Linux & Low-Level Systems](categories/linux-low-level.md) |
| Work with a database | [Database & Backend](categories/database-backend.md) · [Backend Developer](collections/role-backend-developer.md) |
| Set up Docker, Kubernetes or CI | [DevOps & Cloud](categories/devops-cloud.md) |
| Audit my application security | [Cybersecurity](categories/cybersecurity.md) · [Cybersecurity Researcher](collections/role-cybersecurity-researcher.md) |
| Build an AI/ML or RAG workflow | [AI & Machine Learning](categories/ai-machine-learning.md) · [AI Engineer](collections/role-ai-engineer.md) |
| Analyze data | [Data Science & Analytics](categories/data-science.md) |
| Make a game | [Game Development](categories/game-development.md) · [Game Developer](collections/role-game-developer.md) |
| Design a UI or design system | [Design & UI/UX](categories/design-ui-ux.md) · [UI/UX Designer](collections/role-ui-ux-designer.md) |
| Generate or edit images | [Image Generation & Editing](categories/image-generation.md) |
| Generate or edit video | [Video Generation & Editing](categories/video-generation.md) · [Video Editor & Creator](collections/role-video-editor.md) |
| Create audio, voice or music | [Audio, Voice & Music](categories/audio-music.md) |
| Write content or run marketing | [Content & Marketing](categories/content-marketing.md) · [Content Creator](collections/role-content-creator.md) |
| Process documents and notes | [Documents & Productivity](categories/documents-productivity.md) · [Productivity User](collections/role-productivity-user.md) |
| Read papers or study | [Education & Research](categories/education-research.md) · [Researcher & Student](collections/role-researcher.md) |
| Run a business workflow | [Business & Finance](categories/business-finance.md) |

> Never use an offensive-security resource against a system without explicit written authorization. See [Security](SECURITY.md).

---

## Browse categories

The full category index is generated at [`categories/README.md`](categories/README.md). Each page includes:

- an introduction and subcategory list
- standalone resources with source, license, security and verification status
- skill packs and toolkits
- related role collections and related categories
- a verification legend

## Role collections

Role collections are curated starting points, not endorsements. Browse them at [`collections/README.md`](collections/README.md). Available roles include full-stack, frontend, backend, Flutter, Android, custom ROM, kernel, cybersecurity, AI, data science, UI/UX, video, content, research, productivity and game development.

---

## Verification methodology

A resource is promoted to `catalog/*.json` only when a source is confirmed. The catalog records these statuses:

| Status | Meaning |
| --- | --- |
| `SOURCE_VERIFIED` | The GitHub, npm or PyPI source was confirmed by metadata. |
| `LICENSE_VERIFIED` | A license was confirmed from registry metadata. |
| `LICENSE_REVIEW_REQUIRED` | No recognized license was found. Do not redistribute until resolved. |
| `COMPATIBILITY_VERIFIED` | OpenCode compatibility was independently checked. |
| `INSTALLATION_TESTED` | The resource was installed in an isolated environment. |
| `FUNCTIONAL_TESTED` | The resource was executed and behaved as described. |
| `MAINTAINED` | Recent upstream activity was observed (last push within roughly 180 days of the verification date). |
| `UNMAINTAINED` | Older upstream activity was observed. Low activity, not necessarily broken. |
| `SECURITY_REVIEW_REQUIRED` | Capability requires a security review before use. |

Important distinctions:

- **Source verified** does not mean **installed**.
- **Installed** does not mean **functionally tested**.
- **Maintained** does not mean **safe**.
- **Popular** does not mean **trustworthy**.

Full details: [`docs/verification.md`](docs/verification.md).

---

## Security and trust

- Security labels are project review labels, not guarantees.
- Offensive-security resources are labelled `HIGH RISK` and require explicit authorization and a defined in-scope target.
- Permission-bypass, guardrail-removal and jailbreak tools are excluded from the catalog and documented only in the [restricted archive](restricted/README.md).
- No secrets are stored in the repository. API keys must be supplied through environment variables.
- Review any resource that executes shell commands, accesses a database, controls a browser or handles credentials.

Read [SECURITY.md](SECURITY.md) and the generated [security review report](reports/security-review.md).

---

## Installation guidance

This hub does **not** auto-install third-party resources. The safe workflow is:

1. Open the resource's upstream source.
2. Read its README and inspect its files.
3. Check the license and security notes in this catalog.
4. Prefer an isolated environment (container, VM, disposable project).
5. Install using the upstream-documented method.
6. Verify the result yourself.
7. Uninstall by reversing the documented install steps.

Some entries include an npm or pip command because the package was confirmed in a registry. Those commands are marked `NOT_TESTED`. Copying arbitrary files into `~/.config/opencode/` without review is discouraged.

See [`docs/installation.md`](docs/installation.md).

---

## Repository structure

```text
.
├── README.md                 # this file
├── LICENSE                   # MIT
├── CONTRIBUTING.md           # contribution workflow
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── SUPPORT.md
├── CHANGELOG.md
├── ROADMAP.md
├── AUTHORS.md
├── CITATION.cff
├── catalog/                  # source-of-truth JSON catalog
│   ├── skills.json
│   ├── agents.json
│   ├── plugins.json
│   ├── mcp.json
│   ├── commands.json
│   ├── rules.json
│   ├── hooks.json
│   ├── providers.json
│   ├── collections.json
│   └── index.json            # generated unified index
├── schemas/                  # JSON Schema definitions
├── data/
│   ├── taxonomy.json         # categories and subcategories
│   └── raw-inventory.json    # every discovered entry, including unresolved
├── categories/               # generated category pages
├── collections/              # generated role and pack pages
├── docs/                     # methodology and guides
├── scripts/                  # validation and generation tools
├── tests/                    # unittest suite
├── reports/                  # generated evidence reports
├── restricted/               # excluded tools and policy
├── website/                  # future website plan (no app yet)
└── .github/                  # CI, issue and PR templates
```

## Local development

Requirements: Python 3.10+ and Git. No third-party packages are required.

```bash
python3 scripts/validate_catalog.py          # validate schemas, IDs, references
python3 scripts/validate_catalog.py --json   # machine-readable result
python3 scripts/check_links.py               # local Markdown links
python3 scripts/check_links.py --network     # probe catalog URLs (slow)
python3 scripts/generate_indexes.py          # regenerate category/collection pages
python3 scripts/generate_indexes.py --check  # fail if generated files are stale
python3 scripts/generate_reports.py          # regenerate reports
python3 scripts/generate_reports.py --check  # fail if reports are stale
python3 -m unittest discover -s tests -v     # run the test suite
```

CI runs validation, generation drift checks, tests, Markdown linting and link checking. See [`.github/workflows/`](.github/workflows/).

---

## Contributing

Contributions are welcome. The most useful contribution is a **verified** resource with a confirmed source, license and honest verification status.

1. Read [CONTRIBUTING.md](CONTRIBUTING.md).
2. Add the entry to the correct `catalog/<type>.json` file.
3. Add the upstream source to `data/raw-inventory.json` if it is not already there.
4. Run the validation and generation commands.
5. Open a pull request using the template.

Do not submit invented repositories, guessed package names or unverified install commands.

---

## Roadmap

See [ROADMAP.md](ROADMAP.md). Near-term priorities:

- Increase coverage in DevOps, AI/ML, data science, game development, audio and business categories with verified standalone entries.
- Add a schema-driven static website with search and filters.
- Add isolated installation tests for a subset of low-risk resources.
- Add automated source re-verification on a schedule.

---

## Acknowledgements

This catalog builds on the work of the OpenCode community and the upstream maintainers of every listed project. Resources remain the property of their authors and are governed by their own licenses. See [AUTHORS.md](AUTHORS.md) and the per-resource source links.

The category structure and verification model were shaped by the requirements of this project and by lessons from public awesome-list and agent-skill collections.

---

## License

This repository's own content is licensed under the [MIT License](LICENSE). Upstream resources are **not** covered by this license; consult each upstream project.

---

**OpenCode Skills Hub — Discover. Build. Create. Automate.**
