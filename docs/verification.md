# Verification Methodology

The catalog separates **discovery**, **source verification**, **license verification**, **compatibility verification**, **installation testing** and **functional testing**. These are different levels of evidence and are never collapsed into a single "verified" badge.

## Verification date

Every catalog entry records a `verification.date`. Source and license facts are a snapshot. An entry may be accurate on that date and stale later. Re-verify before relying on it.

## Status definitions

| Status | Evidence required |
| --- | --- |
| `DISCOVERED` | The entry was found in a brief, list or search. No source check. |
| `SOURCE_VERIFIED` | The GitHub, npm or PyPI source was confirmed by metadata. |
| `LICENSE_VERIFIED` | A license was confirmed from repository or registry metadata. |
| `COMPATIBILITY_VERIFIED` | OpenCode compatibility was independently checked, not just claimed upstream. |
| `INSTALLATION_TESTED` | The resource was installed in an isolated environment and the result was recorded. |
| `FUNCTIONAL_TESTED` | The resource was executed and behaved as described. |
| `MAINTAINED` | The upstream project showed activity within roughly 180 days of the verification date. |
| `UNAVAILABLE` | The source could not be reached. |
| `DUPLICATE` | Another entry represents the same resource. |
| `UNMAINTAINED` | The upstream project has older activity. Not proof that it is broken. |
| `INCOMPATIBLE` | Known not to work with OpenCode. |
| `LICENSE_REVIEW_REQUIRED` | No recognized license was found; redistribution is not safe. |
| `SECURITY_REVIEW_REQUIRED` | Capability warrants review before use. |

## How source verification is performed

For GitHub repositories, metadata is read from the GitHub API:

- full name
- stars observed
- license SPDX identifier
- last push timestamp
- archived flag

For npm packages, metadata is read from the npm registry:

- package name
- latest version
- declared license
- repository URL

For PyPI packages, metadata is read from the PyPI JSON API:

- name and version
- declared license
- project summary and home page

A source is **not** considered verified because a README says so, because a search result exists, or because a package name "looks right".

## How license verification is performed

A license is marked `LICENSE_VERIFIED` only when a recognized SPDX identifier is returned by the registry or repository metadata. Otherwise:

- `NOASSERTION` — a repository exists but no recognized license was detected.
- `UNKNOWN` — the package metadata does not declare a license.
- `LICENSE_REVIEW_REQUIRED` — the catalog records it but does not treat redistribution as safe.

A missing license is not proof that a project is unlicensed. It means the catalog could not confirm one.

## Maintenance signals

`MAINTAINED` and `UNMAINTAINED` are based on the last observed upstream push relative to the verification date. They are activity signals, not quality or safety judgments. A low-activity project can be stable; a very active project can be risky.

## Installation and functional testing

No third-party resource was installed on the maintainer's host during the initial cataloging pass. Entries therefore record `install.tested: "NOT_TESTED"`.

If you perform an isolated installation test, record:

- the environment (container image, OS, versions)
- the exact command
- the observed output or error
- whether uninstall worked
- the date and your identity

Do not mark `INSTALLATION_TESTED` or `FUNCTIONAL_TESTED` without reproducible evidence.

## Star counts

`signals.github_stars_observed` is an observed snapshot with a date. It is not a recommendation, a quality score or a live badge. The README does not display star counts as a ranking.

## What "compatible" means

- `native`: built specifically for OpenCode.
- `compatible`: the upstream project states compatibility or uses a portable skill/plugin format.
- `unknown`: no compatibility evidence was collected.
- `incompatible`: known not to work with OpenCode.

`compatible` does not mean `tested`.

## Corrections

If an entry is wrong, open an issue or pull request with evidence. Corrections are welcome and are a normal part of maintenance.
