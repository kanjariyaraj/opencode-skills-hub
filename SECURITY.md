# Security Policy

## Reporting a vulnerability

If you find a security issue **in this repository** (for example, a malicious catalog entry, a validation bypass, a harmful install instruction or a leaked secret), report it privately:

1. Use GitHub's private vulnerability reporting for `kanjariyaraj/opencode-skills-hub`, if available.
2. Otherwise contact the maintainer listed in [AUTHORS.md](AUTHORS.md) with a minimal reproduction and the affected path.

Do **not** open a public issue for an unresolved vulnerability. Do not include real credentials, personal data or exploit payloads in a report.

We will acknowledge the report, assess scope and coordinate a fix. Timelines depend on severity and maintainer availability.

## Scope

This repository is a **catalog and documentation project**. It does not host or execute upstream resources. A security issue in an upstream project must be reported to that project's maintainers.

In scope for this repository:

- malicious or misleading catalog entries
- broken or dangerous install instructions added by contributors
- validation or CI bypasses
- exposed secrets
- supply-chain risks introduced by project tooling
- license or attribution problems

Out of scope:

- vulnerabilities in third-party resources listed in the catalog
- requests to test third-party systems
- social engineering
- denial-of-service against this repository's hosting provider

## How resources are assessed

For each catalogued resource we try to confirm:

- source authenticity (GitHub, npm or PyPI metadata)
- declared license
- recent upstream activity
- install and runtime capabilities
- whether it handles credentials, executes shell commands, controls a browser or accesses a database
- whether it is offensive-security tooling

We assign a review label:

| Label | Meaning |
| --- | --- |
| `LOW RISK` | No meaningful execution surface observed. Still not a guarantee. |
| `REVIEWED` | A basic review was completed. |
| `REVIEW REQUIRED` | Not reviewed, or capability warrants review. |
| `HIGH RISK` | Offensive, destructive or broad-access capability. Authorization required. |
| `UNSAFE` | Known unsafe. Kept only for documentation or removed. |
| `DEPRECATED` | Superseded or unmaintained. |

## Restricted archive policy

Permission-bypass, guardrail-removal, jailbreak and unrestricted-execution tools are **excluded** from the main catalog. They are documented only in [`restricted/README.md`](restricted/README.md) for awareness, not as recommendations. This project will not accept contributions that encourage disabling permission systems or hiding actions from users.

## Offensive security policy

Offensive-security resources are catalogued only for:

- authorized penetration tests
- capture-the-flag competitions
- isolated labs and owned systems
- defensive research

Use requires explicit written authorization and a defined in-scope target. Never scan, exploit or disrupt third-party systems. Never use this catalog to target infrastructure you do not own.

## Secret handling

- Never commit `.env` files, tokens, private keys or credentials.
- API keys required by a resource must be supplied through environment variables or a secret manager.
- Reports and logs must not contain secrets.
- If you accidentally commit a secret, rotate it immediately and open a private report.

## Dependency and CI policy

- Project tooling is stdlib-only Python where possible.
- GitHub Actions are pinned to reviewed major versions or commit SHAs.
- CI does not execute third-party install scripts from the catalog.
- Network link checks run separately from pull-request validation to avoid flaky blocking.

## Supported versions

This is a documentation and data repository. Security fixes are applied to the default branch (`main`). There are no maintained release branches at this time.
