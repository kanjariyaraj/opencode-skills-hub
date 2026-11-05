# Testing Progress

Last updated: 2026-11-05

## Suite

`python3 -m unittest discover -s tests -v`

## Areas covered

- catalog validation
- duplicate and reference detection
- category validation
- local Markdown link checking
- index generation and `--check`
- report generation and `--check`

## Current results

See `reports/test-results.md` for the recorded run. Re-run before claiming success; results are a snapshot.

## Not tested

- upstream resource installation
- upstream resource functionality
- OpenCode version compatibility
- network link availability (separate scheduled job)
- website (not built)

## Rules

- A failure is never converted into a pass by weakening an assertion.
- Claims of completion require command output.
