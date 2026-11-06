# Security Report

Date: 2026-11-05. Full per-resource notes are in [security-review.md](security-review.md).

## Label distribution

| Project label | Resources |
| --- | --- |
| REVIEW REQUIRED | 111 |
| LOW RISK | 8 |
| HIGH RISK | 4 |

- No resource received a source-code security audit.
- `REVIEW REQUIRED` is the default for anything that executes code, reads workspace data or handles credentials.
- `LOW RISK` is limited to theme JSON files.
- `HIGH RISK` is limited to offensive-security tooling.

## High-risk entries

| ID | Resource | Why |
| --- | --- | --- |
| `mrzero` | [MrZero](https://www.npmjs.com/package/@bengabay94/mrzero) | Exploit-development tooling. Authorization required. Pre-release; expect instability. |
| `opensploit-core` | [OpenSploit Core](https://www.npmjs.com/package/@opensploit/core) | Bundles offensive security tooling. Never run against systems without explicit written authorization. Keep isolated. |
| `pentester-mcp` | [Pentester MCP](https://pypi.org/project/pentester-mcp/) | Offensive security tooling. Use only with explicit authorization and a defined in-scope target. Never scan third-party systems. |
| `open-sploit` | [open-sploit](https://www.npmjs.com/package/open-sploit) | Offensive tooling. Authorization required. No source-level review was possible without a repository URL. |

## Threat themes in this expansion

- **Credential handling:** auth plugins read OAuth tokens and refresh them.
- **Data egress:** memory, telemetry, vision and chat bridges can send workspace data to third parties.
- **Code execution:** plugins and subagents run inside the OpenCode process.
- **Local indexing:** RAG, code-search and session-search tools persist source or conversation data.
- **OSINT/privacy:** investigation tooling can collect personal data.

## Use guidance

1. Read the plugin or skill before enabling it.
2. Use a dedicated browser profile for browser automation.
3. Keep provider keys scoped and rotate them.
4. Prefer local embeddings/memory when the data is sensitive.
5. Use offensive tooling only with explicit written authorization.
