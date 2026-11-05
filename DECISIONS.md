# Decisions

## ADR-001: Single catalog with type-specific files

**Decision:** Store resources in `catalog/<type>.json` with a `type` field enforced by the validator, plus a generated unified `catalog/index.json`.

**Reason:** Keeps the source readable by humans and consumers while preserving type-specific validation and a stable API for a future website.

## ADR-002: Separate raw inventory from verified catalog

**Decision:** Preserve every discovered entry in `data/raw-inventory.json`; promote only verified entries to the catalog.

**Reason:** Avoids silently discarding discoveries while preventing unverified links from being presented as working resources.

## ADR-003: Conservative security labels

**Decision:** Default to `REVIEW REQUIRED`; use `HIGH RISK` for offensive or broad-access capability; exclude permission-bypass tooling.

**Reason:** Popularity is not safety. A catalog must not imply a guarantee it cannot provide.

## ADR-004: No third-party installation during cataloging

**Decision:** Do not install resources on the maintainer's host. Mark `NOT_TESTED` honestly.

**Reason:** Supply-chain safety and honesty. Isolation and evidence are required before claiming installation testing.

## ADR-005: Stdlib-only tooling

**Decision:** Use Python's standard library for validation, generation, tests and link checking.

**Reason:** Low maintenance, fast CI, no dependency supply chain and broad contributor compatibility.

## ADR-006: Generated Markdown before a website

**Decision:** Generate category, collection and report pages from JSON; defer the website.

**Reason:** GitHub Markdown is immediately useful and the data model must stabilize before building a UI.

## ADR-007: Deterministic generation

**Decision:** Generators must not embed timestamps or non-deterministic ordering.

**Reason:** `--check` can then detect drift reliably in CI.

## ADR-008: Restricted archive

**Decision:** Document permission-bypass and guardrail-removal tools only in `restricted/README.md` without install instructions.

**Reason:** Awareness without promotion.
