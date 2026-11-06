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

## Review required (111)

These entries were not security-audited. Review them before use, especially anything that executes shell commands, accesses databases, controls a browser or handles credentials.

| Resource | Notes |
| --- | --- |
| [3D Web Skill](https://www.npmjs.com/package/3d-web-skill) | Instruction-only skill; no source-level audit was possible without a repository URL. |
| [AI Artist](https://github.com/Stonelukas/Mouse-on-Numpad) | Instruction-only skill; not security-audited. |
| [AI Sessions MCP](https://github.com/yoavf/ai-sessions-mcp) | Reads local AI session transcripts that may contain sensitive code and prompts. Limit indexed directories. |
| [AUR Skills](https://github.com/enihcam/aur-skills) | Skills generate and can run packaging commands. Inspect PKGBUILDs before building or submitting. |
| [Android Kernel LKM](https://github.com/Yunnijian/android-kernel-lkm) | Kernel-level operations can destabilize or brick a device. License file not detected by GitHub API. |
| [Antigravity Auth](https://github.com/NoeFabris/opencode-antigravity-auth) | Handles OAuth credentials for a Google account. Review token storage and Google's terms; the plugin is unofficial. |
| [Architecture Diagram Skill](https://github.com/konraddzbik/architecture-diagram-skill) | Instruction-only skill. SKILL.md can direct the agent to run commands; review it before enabling. |
| [ArtCraft Skills](https://github.com/midasmatterhorn/artcraft-skills) | Instruction-only skill. SKILL.md can direct the agent to run commands; review it before enabling. |
| [CTF Skills](https://github.com/ljagiello/ctf-skills) | Offensive security techniques for CTF training. Use only in authorized labs and competitions. |
| [Cache Stats](https://github.com/nmdra/opencode-cache-stats) | Plugin code runs inside OpenCode. Review the source and pin a version before enabling it. |
| [Claude Auth](https://github.com/griffinmartin/opencode-claude-auth) | Reads and refreshes Claude Code OAuth credentials. Review credential storage, account terms and access. |
| [Claude Code Plugin](https://github.com/khalilgharbaoui/opencode-claude-code-plugin) | Launches the Claude CLI as a subprocess. Review CLI permissions and the account terms. |
| [Claude Memory](https://github.com/kuitos/opencode-claude-memory) | Writes persistent project memory files. Review what is stored and exclude secrets. |
| [CodeSearch](https://github.com/flupkede/codesearch) | Indexes repository contents locally. Verify where indexes are stored and exclude secrets before indexing. |
| [DaisyWriter](https://github.com/ricky-theseus/DaisyWriter) | Some skills install Node and Playwright packages and automate publishing sites. Review the scripts before running them. |
| [Deep Research Skills](https://github.com/Weizhena/Deep-Research-skills) | Research workflows browse external sources and may process untrusted content. Verify citations before publishing. |
| [Design MD Generator](https://github.com/Vann4799/design-md-generator) | Installer copies files into agent configuration directories. Preview with --list and review the diff. |
| [Designing Canvas Art](https://github.com/osmontero/opencode-skills) | May instruct the agent to run local graphics tooling; review before use. |
| [DevHive Backender](https://pypi.org/project/devhive/) | Python package install; review dependencies and scripts before installing globally. |
| [DevHive Frontender](https://pypi.org/project/devhive/) | Python package install; review dependencies and scripts before installing globally. |
| [Dir Tree TUI](https://github.com/aihaipeng/opencode-dir-tree-tui) | Plugin code runs inside OpenCode. Review the source and pin a version before enabling it. |
| [DuckBrain](https://pypi.org/project/duckbrain/) | Reads and writes local notes. Back up the vault and restrict write access until reviewed. |
| [Dynamic Context Pruning](https://github.com/Tarquinen/opencode-dynamic-context-pruning) | Modifies conversation context before model calls. Verify that important instructions are not pruned. |
| [Figma MCP](https://github.com/gberaudo/opencode-mcp-figma) | Connects to a Figma account and exposes design data. Review OAuth scope and workspace permissions. |
| [Gemini Auth](https://github.com/jenslys/opencode-gemini-auth) | Handles Google OAuth credentials. Review token storage, account terms and quota usage. |
| [History Search](https://github.com/joeyism/opencode-history-search) | Reads local conversation history that may contain secrets. Limit scope and protect the index. |
| [HyperDroid Skill](https://github.com/hyperb1iss/hyperdroid-skill) | Build instructions can consume large disk space and run long build jobs; review before executing. |
| [Impeccable](https://github.com/pbakaus/impeccable) | Instruction-only skill; not security-audited. |
| [Langfuse Observability](https://github.com/langfuse/opencode-observability-plugin) | Sends prompts, generations and tool traces to Langfuse. Review data residency, secrets and retention. |
| [Laya Drift](https://github.com/pythongiant/laya-drift) | Scores and stores agent behavior locally. Review the data collected and model dependencies. |
| [Legnext AI Skills (Midjourney API)](https://github.com/legnext-ai/skills) | Third-party API integration; review credential handling and billing implications. |
| [Marimo OpenCode Skill](https://github.com/adrunkhuman/marimo-opencode-skill) | Instruction-only skill. SKILL.md can direct the agent to run commands; review it before enabling. |
| [Mermaid Renderer](https://github.com/anis-dr/opencode-mermaid-renderer) | Plugin code runs inside OpenCode. Review the source and pin a version before enabling it. |
| [Message Bridge](https://github.com/YuanG1944/message-bridge-opencode-plugin) | Connects a chat bot to a coding agent. Restrict bot access and review message logging and workspace permissions. |
| [MiniMax H3 OpenCode Skills](https://github.com/unknowlei/minimax-h3-opencode-skills) | Instruction-only skill. SKILL.md can direct the agent to run commands; review it before enabling. |
| [Morph Fast Apply](https://github.com/JRedeker/opencode-morph-fast-apply) | Sends code snippets to Morph's API for edit application. Review data handling, billing and provider terms. |
| [OSINT MCP](https://github.com/n5za/osint-mcp) | OSINT tooling collects public and personal data. Use only for lawful, authorized research and review data retention. |
| [OSINT Skill](https://github.com/smixs/osint-skill) | OSINT workflows can collect personal data. Use only for lawful, authorized research and respect privacy rules. |
| [Obsidian Knowledge Workflow](https://github.com/r007b34r/opencode-obsidian-knowledge-workflow) | Skills can read and modify an Obsidian vault. Back up the vault and review write operations. |
| [Ogham MCP](https://github.com/ogham-mcp/ogham-mcp) | Stores and shares conversation memory across clients. Review storage location, access control and deletion. |
| [Open Document Skills](https://github.com/leiverkus/open-document-skills) | Instruction-only skill. SKILL.md can direct the agent to run commands; review it before enabling. |
| [OpenAI Codex Auth](https://github.com/numman-ali/opencode-openai-codex-auth) | Handles ChatGPT OAuth credentials. Review token storage, account terms and personal-use restrictions. |
| [OpenCode Academic Research](https://github.com/timpara/opencode-academic-research) | Research pipelines browse external sources and may process untrusted content. Verify sources and citations. |
| [OpenCode Auto Resume](https://github.com/Mte90/opencode-auto-resume) | Automatically retries failed model calls. Review retry limits to avoid unexpected provider charges. |
| [OpenCode Browser](https://github.com/michaljach/opencode-browser) | Automates a live browser session and can act on logged-in accounts. Use a dedicated profile and restrict site access. |
| [OpenCode Browser Control](https://www.npmjs.com/package/opencode-browser-control) | Browser control can access authenticated sessions. Isolate profiles and avoid exposing credentials to untrusted sites. |
| [OpenCode Charts](https://github.com/joe-broadhead/opencode-charts) | Plugin code runs inside OpenCode. Review the source and pin a version before enabling it. |
| [OpenCode Command Provider](https://github.com/rashidrazak/opencode-cmd-provider) | Adds a third-party model provider. Review account credentials, data handling and billing. |
| [OpenCode Execsa](https://github.com/lkonga/opencode-execsa) | Delegates terminal execution to a subagent. Review command permissions and sandboxing. |
| [OpenCode Failover](https://github.com/bulutmuf/opencode-failover) | Handles multiple provider API keys and switches between them. Review secret storage and billing impact. |
| [OpenCode Flutter Architect](https://www.npmjs.com/package/@alghanem/opencode-flutter) | Global npm install executes package install scripts. Review provenance and the package contents first. |
| [OpenCode LLM Proxy](https://github.com/KochC/opencode-llm-proxy) | Runs a local model gateway that may hold provider credentials. Bind it to localhost and review access controls. |
| [OpenCode LiteLLM](https://github.com/yuseferi/opencode-litellm) | Connects to a LiteLLM proxy that may hold provider keys. Review proxy access control and data handling. |
| [OpenCode MCP](https://github.com/AlaeddineMessadi/opencode-mcp) | Exposes broad OpenCode tooling to MCP clients. Review tool scope and workspace access. |
| [OpenCode Mem](https://github.com/tickernelz/opencode-mem) | Stores conversation memory in a local vector database. Review the storage path, retention and credential redaction. |
| [OpenCode Mercato](https://github.com/ThomasSanna/opencode-mercato) | Marketplace plugin can install or enable other plugins. Review the source of anything it installs. |
| [OpenCode Model Router](https://github.com/marco-jardim/opencode-model-router) | Routes requests across configured models. Review cost limits, provider terms and fallback behavior. |
| [OpenCode Models Discovery](https://github.com/yuhp/opencode-models-discovery) | Queries provider endpoints with configured credentials. Review network access, caching and provider terms. |
| [OpenCode Multiplexer](https://github.com/joeyism/opencode-multiplexer) | Plugin code runs inside OpenCode. Review the source and pin a version before enabling it. |
| [OpenCode Nano Banana](https://www.npmjs.com/package/opencode-nanobanana) | Sends prompts and media to third-party generation APIs. Review data handling and billing. |
| [OpenCode OpenTelemetry](https://github.com/DEVtheOPS/opencode-plugin-otel) | Sends session telemetry to a configured collector. Review the payload, endpoint and retention policy. |
| [OpenCode Parser](https://github.com/TejasS1233/opencode-parser) | Parses untrusted documents inside the agent runtime. Keep parser dependencies patched and sandbox risky files. |
| [OpenCode Postgres Plugin](https://www.npmjs.com/package/opencode-postgres) | Database access plugin. Use least-privilege credentials and verify the read-only safeguards in the source. |
| [OpenCode Productivity Agent](https://www.npmjs.com/package/opencode-productivity-agent) | Integrations may request access to external work tools. Review OAuth scopes and data handling. |
| [OpenCode Rules](https://github.com/frap129/opencode-rules) | Injects local rule files into model context. Review rules for secrets or unintended instructions. |
| [OpenCode See Image](https://github.com/alfaoz/opencode-see-image) | Sends images to a configured vision model. Review provider data handling and image privacy. |
| [OpenCode Senses](https://github.com/itsmeadarsh2008/opencode-senses) | Sends images to a local or remote vision model. Review provider configuration and image privacy. |
| [OpenCode Sessions](https://github.com/malhashemi/opencode-sessions) | Manages multiple agent sessions and their context. Review session isolation and data retention. |
| [OpenCode Simple Memory](https://github.com/ApplauseLab/opencode-plugin-simple-memory) | Plugin code runs inside OpenCode. Review the source and pin a version before enabling it. |
| [OpenCode Skill Creator](https://github.com/antongulin/opencode-skill-creator) | Instruction-only skill. SKILL.md can direct the agent to run commands; review it before enabling. |
| [OpenCode Supermemory](https://github.com/supermemoryai/opencode-supermemory) | Sends project memory to the Supermemory cloud service. Review data residency, scoping and deletion. |
| [OpenCode Synced](https://github.com/iHildy/opencode-synced) | Syncs configuration that may contain MCP secrets or tokens. Review encryption and repository permissions before enabling. |
| [OpenCode Telegram](https://github.com/gkhantyln/opencode-telegram) | Exposes a coding agent through Telegram. Restrict chat access, review command permissions and avoid sending secrets. |
| [OpenCode Vim](https://github.com/leohenon/opencode-vim-plugin) | Plugin code runs inside OpenCode. Review the source and pin a version before enabling it. |
| [OpenCode Voice](https://github.com/renjfk/opencode-voice) | Captures microphone audio and may store transcripts. Review recording, storage and transcription privacy. |
| [OpenCode WakaTime](https://github.com/angristan/opencode-wakatime) | Sends coding activity metadata to WakaTime. Review the account, project-name leakage and telemetry settings. |
| [OpenCode Websearch](https://github.com/emilsvennesson/opencode-websearch) | Sends search queries through the configured model provider. Review provider terms and query privacy. |
| [OpenCode Working Memory](https://github.com/sdwolf4103/opencode-working-memory) | Persists workspace context and may inject it into prompts. Review storage and secret handling. |
| [OpenCode++](https://github.com/whut09/opencode-plusplus) | Distributed as a Windows installer executable. Verify the release signature/hash and review the source before running. |
| [OpenCodeRAG](https://github.com/MrDoe/OpenCodeRAG) | Indexes source code and may send embeddings to a remote provider. Review storage, provider and secret-exclusion settings. |
| [OpenSpec Plugin](https://github.com/Octane0411/opencode-plugin-openspec) | Plugin code runs inside OpenCode. Review the source and pin a version before enabling it. |
| [OpenToken](https://github.com/MrGray17/opentoken) | Rewrites and compresses shell output before it reaches the model. Check that security-relevant output is not hidden. |
| [PPT Image First](https://github.com/NyxTides/ppt-image-first) | Sends presentation content and style prompts to an image-generation provider. Review data handling and billing. |
| [Papercut Explainer](https://github.com/0xS4N4TG/papercut-explainer) | Skills drive a Remotion video pipeline and may install Node packages. Review scripts and generated media. |
| [Python Expert Agent](https://github.com/amrahman90/python-expert-agent) | Global npm install runs package scripts. Review the package and generated agent config before use. |
| [QA Test CLI](https://www.npmjs.com/package/qa-test-cli) | Scaffolding tool writes into the user's skills directory. Review generated files. |
| [Quarkus Skill](https://github.com/b6k-dev/quarkus-skill) | Instruction-only skill. SKILL.md can direct the agent to run commands; review it before enabling. |
| [Ralph Loop](https://github.com/charfeng1/opencode-ralph-loop) | Auto-continues agent work. Set stop conditions and monitor token usage. |
| [Rust Agentic Skills](https://github.com/udapy/rust-agentic-skills) | Instruction-only skill. SKILL.md can direct the agent to run commands; review it before enabling. |
| [Sense](https://github.com/luuuc/sense) | Indexes source code and exposes it to the agent. Exclude secrets and third-party code you cannot process. |
| [Spec Forge](https://github.com/tercel/spec-forge) | Instruction-only skill. SKILL.md can direct the agent to run commands; review it before enabling. |
| [Sprezzature](https://pypi.org/project/sprezzature/) | Instruction-only skill collection; license unreviewed. |
| [SubAgent Magazine](https://github.com/Hotakus/opencode-subagent-magazine) | Plugin code runs inside OpenCode. Review the source and pin a version before enabling it. |
| [Superpowers: Brainstorming](https://github.com/obra/superpowers) | Instruction-only process skill; not security-audited here. |
| [Superpowers: Systematic Debugging](https://github.com/obra/superpowers) | Instruction-only process skill; not security-audited here. |
| [Superpowers: Test-Driven Development](https://github.com/obra/superpowers) | Instruction-only process skill; not security-audited here. |
| [SwiftUI Design Skill](https://github.com/Wholiver/swiftui-design-skill) | Instruction-only skill. SKILL.md can direct the agent to run commands; review it before enabling. |
| [Termux Skill](https://www.npmjs.com/package/termux-skill) | Grants device-control capabilities through Termux. Review the exact API calls before enabling. |
| [Theme Studio](https://github.com/kkugot/opencode-theme-studio) | Edits local theme files. Back up custom themes before experimenting. |
| [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Instruction-only skill; no installation audit was performed. Content may instruct the agent to run commands. |
| [Unity Skills](https://github.com/Besty0728/Unity-Skills) | Skills can modify Unity projects and invoke editor scripts. Work on a copy or version-controlled project. |
| [Videocut Clip](https://github.com/zrt-ai-lab/opencode-skills) | Runs FFmpeg file operations; confirm input/output paths to avoid overwriting source media. |
| [WaveSpeed CLI](https://www.npmjs.com/package/@wavespeed/cli) | Paid third-party API. Review billing, data handling and credential storage. |
| [ast-grep MCP](https://github.com/ThinkDonk/ast-grep-mcp) | Can rewrite source code through AST replacements. Review tool permissions and use version control. |
| [database-admin](https://www.npmjs.com/package/database-admin) | Can execute SQL against configured databases. Use read-only accounts and never point it at production without authorization. |
| [gstack](https://www.npmjs.com/package/opencode-plugin-gstack) | Browser automation can reach external sites and handle session data. Review before use. |
| [heditor](https://github.com/pycodebr/heditor) | Skill may download and run media tooling and upload footage to generation providers. Review its install script first. |
| [iSpan Data Science Cookbooks](https://github.com/Zenobia000/iSpan_python-FE_DM-cookbooks) | Instruction-only skill. SKILL.md can direct the agent to run commands; review it before enabling. |
| [img2threejs](https://github.com/img2threejs/img2threejs) | Generates and executes project code; review generated output before deployment. |
| [oh-my-design-cli](https://www.npmjs.com/package/oh-my-design-cli) | Global npm install and CLI execution. Review before running. |
| [superPM](https://github.com/konglong87/superPM) | Instruction-only skill. SKILL.md can direct the agent to run commands; review it before enabling. |

## Restricted archive

Permission-bypass, guardrail-removal and jailbreak-style tools are documented only in [`restricted/README.md`](../restricted/README.md). They are excluded from the catalog and are not recommended.

## Authorization policy

Offensive-security resources may only be used against systems you own or for which you have explicit written authorization. Never scan, exploit or disrupt third-party systems.

## Credential policy

No secrets are stored in the catalog or reports. API keys must be supplied through environment variables and never committed.
