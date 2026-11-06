# Installation Test Framework

This directory contains the **only** supported way to claim `INSTALLATION_TESTED` for a catalogued resource.

## Safety model

- Every case runs in a disposable Docker container.
- The host OpenCode config (`~/.config/opencode`) is never mounted.
- The container receives one temporary work directory, drops all Linux capabilities, and enables `no-new-privileges`.
- Cases are pinned to a commit SHA or an exact package version.
- No case runs without `--yes`.
- A `PASS` means the pinned installation command completed and the documented smoke check succeeded. It does **not** mean the resource is safe or fully functional.

## Run

```bash
python3 scripts/run_installation_tests.py --list
python3 scripts/run_installation_tests.py --case theme-catppuccin --yes
python3 scripts/run_installation_tests.py --all --yes
```

Results are written to [`reports/installation-results.json`](../../reports/installation-results.json) and [`reports/installation-results.md`](../../reports/installation-results.md).

## Add a case

1. Add an entry to `cases.json` with a unique `id`, the catalog `resource_id`, a pinned version or commit, a timeout, and a `bash` script.
2. Keep the script non-interactive and make the final command assert the expected outcome.
3. Run only that case with `--case`.
4. Update the resource's `install.tested` and `verification.status` only when the case passes.
5. Record the evidence path in the resource's verification notes.

## What is not covered

- Model calls, authentication flows, and OAuth consent screens.
- GUI/TUI behavior that requires a real terminal session.
- Resources whose install instructions cannot be executed non-interactively.
- Security review. Installation success is not a security audit.

Unlisted resources stay `NOT_TESTED`. This is deliberate and is not a quality claim either way.
