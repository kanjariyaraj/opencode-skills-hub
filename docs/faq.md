# Frequently asked questions

Short answers to the questions new readers ask most often. For methodology, see
[verification.md](verification.md); for contribution rules, see
[../CONTRIBUTING.md](../CONTRIBUTING.md).

## Is every resource installed and tested?

No. Source verification and license verification are recorded separately from
installation and functional testing. Most entries are `NOT_TESTED` because
third-party code was not installed on the maintainer's host during cataloging.

A status of `INSTALLATION_TESTED` should point to a reproducible evidence note.
If it does not, treat the status as unverified and report it.

## What does "verified" mean here?

It means the source URL was confirmed against a registry (GitHub, npm or PyPI)
and the recorded metadata matched. It does **not** mean the resource is safe,
useful, maintained or compatible with your setup.

## Why are some categories empty?

A zero count means no **standalone verified entry** yet. The category may still
list upstream skill packs that cover the topic. Packs are catalogued as one
entry rather than decomposed into unverified sub-items.

## Why are there more raw inventory entries than catalog entries?

Discovery records every candidate, including ones that cannot be confirmed. The
raw inventory preserves them so useful leads are not lost. Only confirmed
entries are promoted to `catalog/*.json`.

## Can I add my own project?

Yes, if it is real, reachable and honestly described. Use
[resource-template.md](resource-template.md), run `make check`, and open a pull
request. Self-promotion is acceptable when the entry is accurate; inventing
stars, downloads or test results is not.

## Why is installation testing not automated?

Installing arbitrary ecosystem resources on shared infrastructure is unsafe.
Most need API keys, model access, desktop components or platform-specific
dependencies. A future phase will test a small set of low-risk resources in
disposable containers.

## How often is the catalog re-verified?

Each entry stores a verification date and observed maintenance signal. There is
no scheduled re-verification yet; Phase 6 of the [roadmap](../ROADMAP.md) covers
it. Treat older dates as a reason to re-check upstream.

## Why are some license statuses "review required"?

No recognized license was found in registry metadata. The resource is not
automatically rejected, but it must not be redistributed until the license is
resolved. See [licenses.md](../reports/licenses.md).

## Why are permission-bypass or jailbreak tools excluded?

They remove the user's ability to consent to actions. They are documented only
in the [restricted archive](../restricted/README.md) so the exclusion is
explicit, and they are never recommended.

## Does inclusion mean endorsement?

No. Inclusion is a discovery aid. Authorship, licensing and support stay with
the upstream project. See [../AUTHORS.md](../AUTHORS.md).

## Can I use the catalog offline?

Yes. Clone the repository and read the Markdown and JSON locally. No build step
or network access is required for browsing. Network access is only needed for
`make network-links` and for installing upstream resources.

## How do I report a broken or unsafe entry?

Open an issue using the bug report template and include the catalog ID, the
observed problem and any evidence. For security-sensitive reports, follow
[../SECURITY.md](../SECURITY.md) instead of a public issue.

## What Python version is required?

Python 3.10 or newer. The tooling uses only the standard library. There are no
`pip install` requirements for validation, generation or tests.
