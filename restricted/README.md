# Restricted Archive

This directory documents tools that are **excluded from the main catalog** because they remove or bypass safety and permission controls.

They are listed for awareness and defensive discussion only. They are **not** recommended, tested or supported by this project. No install commands are provided.

## Excluded category

| Category | Why it is excluded |
| --- | --- |
| Permission bypass | Removes or auto-approves the user's permission checks. |
| Guardrail removal | Strips safety instructions from agent prompts or model responses. |
| Jailbreak patches | Intercepts and rewrites refusals at runtime. |
| Unrestricted forks | Ships a modified agent binary with safety controls removed. |
| Credential harvesting | Reads tokens, keys or session data beyond the task's needs. |
| Covert execution | Hides commands, files or network activity from the user. |

## Entries seen in the wild

The initial discovery brief mentioned the following names. They are recorded here so contributors do not re-add them to the catalog. They were not installed, endorsed or verified.

- `@aegntic/bypass-agent` — claimed to bypass permission checks.
- `opencode-god-plugin` — claimed to auto-allow all permissions.
- `opencode-gpt-unlocked` — claimed to rewrite model refusals.
- `evil-opencode` — claimed to be a guardrail-stripped fork.

These projects may change, disappear or be malicious. Do not install them based on this mention.

## Project policy

- This project will not add install instructions for these tools.
- Pull requests that promote permission bypass or guardrail removal will be closed.
- Security concerns about such tools can be reported privately per [SECURITY.md](../SECURITY.md).
- If you need broad automation, use explicit, scoped permissions and review each action. Convenience is not a substitute for consent.

## Why list them at all?

Silence does not make risky tooling disappear. A short, clearly non-endorsing record helps users recognize the category, helps maintainers reject duplicates and keeps the main catalog trustworthy.
