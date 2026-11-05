PYTHON ?= python3
MDLINT ?= npx --yes markdownlint-cli2@0.13.0

.PHONY: help validate generate query test lint links network-links check all clean

help:
	@printf '%s\n' \
		'make validate       Validate schemas, IDs, categories and references' \
		'make generate       Regenerate index, category pages, collections and reports' \
		'make query          Print resources sorted by name' \
		'make test           Run the unit test suite' \
		'make lint           Lint Markdown (downloads markdownlint-cli2 via npx)' \
		'make links          Check local Markdown links' \
		'make network-links  Probe external catalog URLs (slow, informational)' \
		'make check          Validate, check drift, test and link-check' \
		'make all            Generate, then run the full check'

validate:
	$(PYTHON) scripts/validate_catalog.py

generate:
	$(PYTHON) scripts/generate_indexes.py
	$(PYTHON) scripts/generate_reports.py

query:
	$(PYTHON) scripts/query_catalog.py --sort name

test:
	$(PYTHON) -m unittest discover -s tests -v

lint:
	$(MDLINT) "**/*.md" "#node_modules" "#**/.github/ISSUE_TEMPLATE/**"

links:
	$(PYTHON) scripts/check_links.py

network-links:
	$(PYTHON) scripts/check_links.py --network --all-links --soft

check:
	$(PYTHON) scripts/validate_catalog.py
	$(PYTHON) scripts/generate_indexes.py --check
	$(PYTHON) scripts/generate_reports.py --check
	$(PYTHON) -m unittest discover -s tests -v
	$(PYTHON) scripts/check_links.py

all:
	$(MAKE) generate
	$(MAKE) check
	$(MAKE) lint

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
