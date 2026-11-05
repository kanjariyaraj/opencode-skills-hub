# Missing and Unresolved Sources

Every entry from the original discovery brief is preserved in `data/raw-inventory.json`. This report lists entries that could not be promoted to the verified catalog because the source was missing, unresolved, not found, or restricted.

Unresolved raw entries: **54** of **111**.

## Source Unresolved (46)

| Entry | Claimed source | Category | Notes |
| --- | --- | --- | --- |
| AI Image Generator | unspecified | image-generation | No owner/repository supplied. |
| Generative Media Skills | unspecified | image-generation | No owner/repository supplied. |
| Godot3D-Harness | Awesome Skills | game-development | Listing referenced; no canonical repository supplied. |
| Hugging Face kernel-builder | kernel-builder skills add --opencode | linux-low-level | Hugging Face project referenced; exact OpenCode integration URL not supplied. |
| Linux Kernel OpenCode Config | AtomGit | linux-low-level | No exact AtomGit URL supplied. |
| MK-ORGANIZATION-1/AGENTS-COLLECTION | MK-ORGANIZATION-1/AGENTS-COLLECTION | software-development | Referenced in research; not verified by API in this pass. |
| MariaDB AI Plugins | MariaDB docs | database-backend | Official MariaDB documentation referenced but no exact URL supplied; not confirmed. |
| Midjourney MCP | Ace Data Cloud | image-generation | Vendor referenced; exact MCP endpoint not supplied. |
| MiniMax Skills | MiniMax | mobile-development | frontend-dev and android-native-dev skills exist in the local installed library; no upstream repository URL supplied or confirmed. |
| OpenCodeGameStudios (SkillsMP) | SkillsMP / striderZA | game-development | Listing referenced; no canonical repository supplied. |
| WebGL | JTech Forums | software-development | Technology, not a verified resource. |
| academic-researcher | create-opencode-workspace template | education-research | Template referenced; workspace package unverified. |
| algorithmic-art | JTech Forums | image-generation | Forum-listed skill; no canonical repository supplied. |
| anatomy | unspecified GitHub repo | image-generation | No exact repository supplied. |
| android-8-policy | JTech Forums | android-system-custom-rom | Forum-listed skill; no canonical repository supplied. |
| android-build | JTech Forums | android-system-custom-rom | Forum-listed skill; no canonical repository supplied. |
| android-reverse-engineering | JTech Forums | android-system-custom-rom | Forum-listed skill; no canonical repository supplied. |
| apktool | JTech Forums | android-system-custom-rom | Refers to the well-known APK tool, not necessarily an OpenCode skill. |
| audio-jingle | opencode-supreme-setup | audio-music | Referenced as part of an unverified setup collection. |
| canvas | JTech Forums | image-generation | Forum-listed skill; no canonical repository supplied. |
| codex-skills-alternative | unspecified GitHub repo | design-ui-ux | No exact repository supplied. |
| content-creator-core | SkillsMP | content-marketing | SkillsMP listing referenced; no canonical repository supplied. |
| create-opencode-workspace | npx create-opencode-workspace | content-marketing | npm package not checked in this pass; treat as unverified. |
| design-taste-frontend | JTech Forums | design-ui-ux | Forum-listed skill; no canonical repository supplied. |
| everything-backend | unspecified | database-backend | No owner/repository supplied. |
| finance-skills | alirezarezvani | business-finance | Owner name supplied without repository name. |
| interface-design | JTech Forums | design-ui-ux | Forum-listed skill; no canonical repository supplied. |
| lib-transformers | Skills.rest | ai-machine-learning | Skills.rest listing referenced; no canonical repository supplied. |
| linkedin-content-generator | unspecified | content-marketing | No owner/repository supplied. |
| material-design-3-ui | JTech Forums | design-ui-ux | Forum-listed skill; no canonical repository supplied. |
| mimo-audio-skill | unspecified GitHub repo | audio-music | No exact repository supplied. |
| mobile-developer | SkillsAuth | mobile-development | Listing referenced; no canonical repository supplied. |
| motion-design | JTech Forums | design-ui-ux | Forum-listed skill; no canonical repository supplied. |
| opencode QA | unspecified | software-development | No owner/repository supplied; cannot verify. |
| opencode-playwright-interactive | unspecified GitHub repo | software-development | No exact repository supplied. |
| opencode-supreme-setup | SkillsMP | software-development | Collection referenced; no canonical repository supplied. |
| opencodeskills.dev | <https://opencodeskills.dev> | software-development | Website referenced; not fetched or validated in this pass. |
| paper-reading | unspecified GitHub repo | education-research | No exact repository supplied. |
| render-visual | JTech Forums | design-ui-ux | Forum-listed skill; no canonical repository supplied. |
| reverse-engineer-anything | JTech Forums | cybersecurity | Forum-listed skill; no canonical repository supplied. |
| social-post-writer-seo | unspecified | content-marketing | No owner/repository supplied. |
| spotkit | JTech Forums | design-ui-ux | Forum-listed skill; no canonical repository supplied. |
| statistics-science | ffsshhttiikk/opencode-agents-skills | data-science | Repository referenced only inside a GitHub URL in the brief; not verified by API in this pass. |
| svg-creator | JTech Forums | image-generation | Forum-listed skill; no canonical repository supplied. |
| video-recap-skills | unspecified | video-generation | No owner/repository supplied. |
| video-subtitle-cutter | unspecified | video-generation | No owner/repository supplied. |

## Not Found (4)

| Entry | Claimed source | Category | Notes |
| --- | --- | --- | --- |
| GeniusHu-tgty/oc-tgtylab | GeniusHu-tgty/oc-tgtylab | cybersecurity | GitHub repo not found on 2026-11-05. |
| cmo-so/marketing | cmo-so/marketing | content-marketing | GitHub repo not found on 2026-11-05. |
| opencode-media-skills | unknown | image-generation | Not present on npm; no GitHub repo found under that exact name. |
| zrt-ai-lab/smart-query | zrt-ai-lab/smart-query | database-backend | GitHub repo does not exist at that path. The parent repo zrt-ai-lab/opencode-skills exists; smart-query may be a skill inside it. |

## Restricted (4)

| Entry | Claimed source | Category | Notes |
| --- | --- | --- | --- |
| @aegntic/bypass-agent | npm @aegntic/bypass-agent | cybersecurity | Permission-bypass tooling. Excluded from catalog; see restricted/README.md. |
| evil-opencode | unspecified GitHub repo | cybersecurity | Guardrail-stripped fork. Excluded from catalog; see restricted/README.md. |
| opencode-god-plugin | npm opencode-god-plugin | cybersecurity | Permission-bypass tooling. Excluded from catalog; see restricted/README.md. |
| opencode-gpt-unlocked | unspecified GitHub repo | cybersecurity | Refusal-rewrite tooling. Excluded from catalog; see restricted/README.md. |

## How to resolve an entry

1. Find the canonical upstream repository, package registry page or official documentation.
2. Confirm the license and compatibility.
3. Add a full entry to the correct `catalog/<type>.json` file.
4. Change the raw inventory resolution to `VERIFIED` and note the evidence.

Never guess a repository owner, package name or install command.
