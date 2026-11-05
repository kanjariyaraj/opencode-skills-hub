# Security Review Report

These are project review labels, not guarantees. No resource was executed during cataloging.

## Method

1. Confirm the source against GitHub, npm or PyPI metadata.
2. Record the declared license and last observed push.
3. Assign a conservative security label based on capability (instruction-only, shell execution, database access, browser control, offensive tooling).
4. Keep permission-bypass and guardrail-removal tools out of the main catalog.

## High-risk and restricted-capability entries

| Resource | Level | Capability | Notes |
| --- | --- | --- | --- |
| [MrZero](https://www.npmjs.com/package/@bengabay94/mrzero) | HIGH RISK | plugin | Exploit-development tooling. Authorization required. Pre-release; expect instability. |
| [OpenSploit Core](https://www.npmjs.com/package/@opensploit/core) | HIGH RISK | plugin | Bundles offensive security tooling. Never run against systems without explicit written authorization. Keep isolated. |
| [Pentester MCP](https://pypi.org/project/pentester-mcp/) | HIGH RISK | mcp | Offensive security tooling. Use only with explicit authorization and a defined in-scope target. Never scan third-party systems. |
| [open-sploit](https://www.npmjs.com/package/open-sploit) | HIGH RISK | plugin | Offensive tooling. Authorization required. No source-level review was possible without a repository URL. |

## Review required (28)

These entries were not security-audited. Review them before use, especially anything that executes shell commands, accesses databases, controls a browser or handles credentials.

| Resource | Notes |
| --- | --- |
| [3D Web Skill](https://www.npmjs.com/package/3d-web-skill) | Instruction-only skill; no source-level audit was possible without a repository URL. |
| [AI Artist](https://github.com/Stonelukas/Mouse-on-Numpad) | Instruction-only skill; not security-audited. |
| [Android Kernel LKM](https://github.com/Yunnijian/android-kernel-lkm) | Kernel-level operations can destabilize or brick a device. License file not detected by GitHub API. |
| [Designing Canvas Art](https://github.com/osmontero/opencode-skills) | May instruct the agent to run local graphics tooling; review before use. |
| [DevHive Backender](https://pypi.org/project/devhive/) | Python package install; review dependencies and scripts before installing globally. |
| [DevHive Frontender](https://pypi.org/project/devhive/) | Python package install; review dependencies and scripts before installing globally. |
| [DuckBrain](https://pypi.org/project/duckbrain/) | Reads and writes local notes. Back up the vault and restrict write access until reviewed. |
| [HyperDroid Skill](https://github.com/hyperb1iss/hyperdroid-skill) | Build instructions can consume large disk space and run long build jobs; review before executing. |
| [Impeccable](https://github.com/pbakaus/impeccable) | Instruction-only skill; not security-audited. |
| [Legnext AI Skills (Midjourney API)](https://github.com/legnext-ai/skills) | Third-party API integration; review credential handling and billing implications. |
| [OpenCode Browser Control](https://www.npmjs.com/package/opencode-browser-control) | Browser control can access authenticated sessions. Isolate profiles and avoid exposing credentials to untrusted sites. |
| [OpenCode Flutter Architect](https://www.npmjs.com/package/@alghanem/opencode-flutter) | Global npm install executes package install scripts. Review provenance and the package contents first. |
| [OpenCode Nano Banana](https://www.npmjs.com/package/opencode-nanobanana) | Sends prompts and media to third-party generation APIs. Review data handling and billing. |
| [OpenCode Postgres Plugin](https://www.npmjs.com/package/opencode-postgres) | Database access plugin. Use least-privilege credentials and verify the read-only safeguards in the source. |
| [OpenCode Productivity Agent](https://www.npmjs.com/package/opencode-productivity-agent) | Integrations may request access to external work tools. Review OAuth scopes and data handling. |
| [QA Test CLI](https://www.npmjs.com/package/qa-test-cli) | Scaffolding tool writes into the user's skills directory. Review generated files. |
| [Sprezzature](https://pypi.org/project/sprezzature/) | Instruction-only skill collection; license unreviewed. |
| [Superpowers: Brainstorming](https://github.com/obra/superpowers) | Instruction-only process skill; not security-audited here. |
| [Superpowers: Systematic Debugging](https://github.com/obra/superpowers) | Instruction-only process skill; not security-audited here. |
| [Superpowers: Test-Driven Development](https://github.com/obra/superpowers) | Instruction-only process skill; not security-audited here. |
| [Termux Skill](https://www.npmjs.com/package/termux-skill) | Grants device-control capabilities through Termux. Review the exact API calls before enabling. |
| [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Instruction-only skill; no installation audit was performed. Content may instruct the agent to run commands. |
| [Videocut Clip](https://github.com/zrt-ai-lab/opencode-skills) | Runs FFmpeg file operations; confirm input/output paths to avoid overwriting source media. |
| [WaveSpeed CLI](https://www.npmjs.com/package/@wavespeed/cli) | Paid third-party API. Review billing, data handling and credential storage. |
| [database-admin](https://www.npmjs.com/package/database-admin) | Can execute SQL against configured databases. Use read-only accounts and never point it at production without authorization. |
| [gstack](https://www.npmjs.com/package/opencode-plugin-gstack) | Browser automation can reach external sites and handle session data. Review before use. |
| [img2threejs](https://github.com/img2threejs/img2threejs) | Generates and executes project code; review generated output before deployment. |
| [oh-my-design-cli](https://www.npmjs.com/package/oh-my-design-cli) | Global npm install and CLI execution. Review before running. |

## Restricted archive

Permission-bypass, guardrail-removal and jailbreak-style tools are documented only in [`restricted/README.md`](../restricted/README.md). They are excluded from the catalog and are not recommended.

## Authorization policy

Offensive-security resources may only be used against systems you own or for which you have explicit written authorization. Never scan, exploit or disrupt third-party systems.

## Credential policy

No secrets are stored in the catalog or reports. API keys must be supplied through environment variables and never committed.
