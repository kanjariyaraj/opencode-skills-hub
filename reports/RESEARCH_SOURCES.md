# Research Sources

Observed on 2026-11-05.

## Primary sources

| Source | Use |
| --- | --- |
| [OpenCode documentation](https://opencode.ai/docs) | Plugin, skill, MCP, agent and configuration semantics |
| [OpenCode plugins](https://opencode.ai/docs/plugins) | Plugin loading and configuration keys |
| [OpenCode skills](https://opencode.ai/docs/skills) | Skill discovery and `SKILL.md` conventions |
| [OpenCode MCP servers](https://opencode.ai/docs/mcp-servers) | MCP configuration |
| [OpenCode agents](https://opencode.ai/docs/agents) | Agent definitions |
| GitHub REST API (`gh api`) | Repository, README, license and release metadata |
| npm registry | Package names, versions and install commands |
| PyPI JSON API | Package metadata for Python resources |

## Repository evidence

For every addition the catalog stores:

- the canonical GitHub URL and `owner/repo` identifier;
- the license SPDX identifier reported by GitHub;
- the last push timestamp and observed star count;
- the latest release tag when one exists;
- a verification date and a note describing what was **not** checked.

## Verification boundaries

- Registry metadata confirms existence and declared license, not safety.
- README inspection confirms documented install steps, not that they work.
- Docker smoke tests cover four cases; see [installation results](installation-results.md).
- No resource received a source-code security audit.
