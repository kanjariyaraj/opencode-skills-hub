# Compatibility Report

Compatibility is recorded from the catalog entry, not from an installation test unless explicitly marked `INSTALLATION_TESTED`.

| Resource | OpenCode | Platforms | Dependencies | API key | Install test |
| --- | --- | --- | --- | --- | --- |
| [3D Web Skill](https://www.npmjs.com/package/3d-web-skill) | compatible | linux, macos, windows | Node.js | no | NOT_TESTED |
| [AI Artist](https://github.com/Stonelukas/Mouse-on-Numpad) | compatible | linux, macos, windows | none declared | no | NOT_TESTED |
| [Android Kernel LKM](https://github.com/Yunnijian/android-kernel-lkm) | compatible | linux, android | matching Android kernel headers, adb, insmod | no | NOT_TESTED |
| [Designing Canvas Art](https://github.com/osmontero/opencode-skills) | compatible | linux, macos, windows | none declared | no | NOT_TESTED |
| [DevHive Backender](https://pypi.org/project/devhive/) | compatible | linux, macos, windows | Python 3.10+ | no | NOT_TESTED |
| [DevHive Frontender](https://pypi.org/project/devhive/) | compatible | linux, macos, windows | Python 3.10+ | no | NOT_TESTED |
| [DuckBrain](https://pypi.org/project/duckbrain/) | compatible | linux, macos, windows | Python 3, Obsidian vault | no | NOT_TESTED |
| [HyperDroid Skill](https://github.com/hyperb1iss/hyperdroid-skill) | compatible | linux | repo, git, Android build host | no | NOT_TESTED |
| [Impeccable](https://github.com/pbakaus/impeccable) | compatible | linux, macos, windows | none declared | no | NOT_TESTED |
| [Legnext AI Skills (Midjourney API)](https://github.com/legnext-ai/skills) | compatible | linux, macos, windows | Legnext API key | yes | NOT_TESTED |
| [MrZero](https://www.npmjs.com/package/@bengabay94/mrzero) | compatible | linux, macos | Node.js, Ghidra, Metasploit | no | NOT_TESTED |
| [OpenCode Browser Control](https://www.npmjs.com/package/opencode-browser-control) | compatible | linux, macos, windows | Node.js, Playwright, Chromium/Chrome | no | NOT_TESTED |
| [OpenCode Flutter Architect](https://www.npmjs.com/package/@alghanem/opencode-flutter) | compatible | linux, macos, windows | Node.js, Flutter SDK | no | NOT_TESTED |
| [OpenCode Nano Banana](https://www.npmjs.com/package/opencode-nanobanana) | compatible | linux, macos, windows | Node.js, image/video provider API key | yes | NOT_TESTED |
| [OpenCode Postgres Plugin](https://www.npmjs.com/package/opencode-postgres) | compatible | linux, macos, windows | Node.js, PostgreSQL | no | NOT_TESTED |
| [OpenCode Productivity Agent](https://www.npmjs.com/package/opencode-productivity-agent) | compatible | linux, macos, windows | Node.js | no | NOT_TESTED |
| [OpenSploit Core](https://www.npmjs.com/package/@opensploit/core) | compatible | linux | Node.js, Docker | no | NOT_TESTED |
| [Pentester MCP](https://pypi.org/project/pentester-mcp/) | compatible | linux, macos | Python 3 | no | NOT_TESTED |
| [QA Test CLI](https://www.npmjs.com/package/qa-test-cli) | compatible | linux, macos, windows | Node.js | no | NOT_TESTED |
| [Sprezzature](https://pypi.org/project/sprezzature/) | compatible | linux, macos, windows | Python 3 | no | NOT_TESTED |
| [Superpowers: Brainstorming](https://github.com/obra/superpowers) | compatible | linux, macos, windows | none declared | no | NOT_TESTED |
| [Superpowers: Systematic Debugging](https://github.com/obra/superpowers) | compatible | linux, macos, windows | none declared | no | NOT_TESTED |
| [Superpowers: Test-Driven Development](https://github.com/obra/superpowers) | compatible | linux, macos, windows | none declared | no | NOT_TESTED |
| [Termux Skill](https://www.npmjs.com/package/termux-skill) | compatible | android, linux | Termux, Termux:API | no | NOT_TESTED |
| [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | compatible | linux, macos, windows | none declared | no | NOT_TESTED |
| [Videocut Clip](https://github.com/zrt-ai-lab/opencode-skills) | compatible | linux, macos, windows | ffmpeg | no | NOT_TESTED |
| [WaveSpeed CLI](https://www.npmjs.com/package/@wavespeed/cli) | compatible | linux, macos, windows | Node.js, WaveSpeed API key | yes | NOT_TESTED |
| [database-admin](https://www.npmjs.com/package/database-admin) | compatible | linux, macos, windows | Node.js, database driver, database credentials | no | NOT_TESTED |
| [gstack](https://www.npmjs.com/package/opencode-plugin-gstack) | compatible | linux, macos, windows | Node.js | no | NOT_TESTED |
| [img2threejs](https://github.com/img2threejs/img2threejs) | compatible | linux, macos, windows | Node.js | no | NOT_TESTED |
| [oh-my-design-cli](https://www.npmjs.com/package/oh-my-design-cli) | compatible | linux, macos, windows | Node.js | no | NOT_TESTED |
| [open-sploit](https://www.npmjs.com/package/open-sploit) | compatible | linux | Node.js, Kali Linux or WSL2 for full tooling | no | NOT_TESTED |

## Interpretation

- `native`: built specifically for OpenCode.
- `compatible`: the upstream project states compatibility or uses a portable skill/plugin format.
- `unknown`: no compatibility evidence was collected.
- `incompatible`: known not to work with OpenCode.

No entry in this catalog has been end-to-end tested in a disposable OpenCode environment. Treat `NOT_TESTED` as a call to verify in your own environment.
