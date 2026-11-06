# Quality Scorecard

Date: 2026-11-05. This is a self-assessment with evidence, not an external audit.

## Overall: 8.1/10

| Dimension | Score | Evidence and gaps |
| --- | --- | --- |
| Source verification | 10/10 | Every entry has a canonical GitHub URL confirmed by API metadata. |
| License transparency | 9/10 | 87% have a recognized license; 16 are explicitly flagged for review. |
| Security labeling | 8/10 | Conservative labels and notes, but no source-code audits. 4 high-risk entries are clearly marked. |
| Installation evidence | 6/10 | 3/123 (2.4%) have isolated Docker smoke tests; zero functional tests. |
| Documentation | 9/10 | Verification, installation, discovery, data model, FAQ and maintainer guides are complete. |
| Automation | 9/10 | Validation, drift checks, tests, link checks and CI workflows run from a single Makefile. |
| UX and discoverability | 8/10 | Categories-first README, task index, query CLI, generated pages and theme-aware artwork. |
| Coverage | 8/10 | 123 resources across all 18 categories, but audio, business and game development remain thin. |
| Maintenance model | 8/10 | Dates, last-push signals and pinning make staleness visible; no automated upstream refresh yet. |
| Community readiness | 6/10 | Contribution templates and governance exist; no external contributors or independent audits yet. |

## What a 10/10 would require

1. Independent security review for every code-executing resource.
2. Functional tests with recorded model/session evidence, not only install smoke tests.
3. Automated upstream freshness checks with review reminders.
4. Coverage of the thin categories with the same verification depth.
5. External contributors and a second maintainer.
6. A published website with search and per-resource pages generated from the same JSON.

## Non-negotiable honesty rules

- No unverified URL, install command, star count or license claim is presented as confirmed.
- `NOT_TESTED` is the default.
- Popularity is never used as a proxy for quality or safety.
