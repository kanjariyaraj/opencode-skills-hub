# Next Steps

## For the next session

1. Read `PROJECT_STATE.md`, `TODO.md` and this file.
2. Run `git status` and `git log -5 --oneline`.
3. Run the verification commands:

   ```bash
   python3 scripts/validate_catalog.py
   python3 scripts/generate_indexes.py --check
   python3 scripts/generate_reports.py --check
   python3 -m unittest discover -s tests -v
   ```

4. Pick the highest-priority open item from `TODO.md`.
5. Add verified entries or resolve raw-inventory gaps.
6. Regenerate, test and commit one logical change.

## Recommended next contribution

Resolve the unresolved entries in `reports/missing-sources.md` that have a plausible canonical source. Promote only when the source, license and compatibility are confirmed.

## Do not

- Install arbitrary third-party resources on the host.
- Fabricate stars, downloads, test results or verification claims.
- Add permission-bypass or guardrail-removal tooling to the main catalog.
- Hand-edit generated files.
- Force-push or rewrite history.
