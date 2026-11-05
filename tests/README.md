# Tests

The suite uses Python's built-in `unittest` and requires no third-party packages.

```bash
python3 -m unittest discover -s tests -v
```

## Coverage

- catalog validation: valid data, duplicate IDs, unknown categories, bad references, type mismatch
- link checking: local Markdown links and escaping the repository
- index generation: deterministic output, category pages, collection pages, `--check`
- report generation: statistics and reports, `--check`

## Fixtures

`tests/fixtures/` holds small catalog and Markdown samples used by the tests. Keep them minimal and focused on one behavior each.

## Adding a test

1. Reproduce the bug or desired behavior with a fixture or temporary directory.
2. Write the failing test.
3. Fix the code.
4. Run the suite twice to confirm stability.
5. Do not weaken an assertion to make a failure disappear.
