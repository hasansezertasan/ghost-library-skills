.PHONY: sync check test build check-all

PYTHON ?= python3
.DEFAULT_GOAL := check-all
INSTALL_STAMP := node_modules/.install-stamp

$(INSTALL_STAMP): package.json package-lock.json
	npm ci --include=dev --ignore-scripts
	@touch $@

sync: $(INSTALL_STAMP)
	$(PYTHON) tools/sync_packaging.py

check: $(INSTALL_STAMP)
	$(PYTHON) tools/sync_packaging.py --check
	$(PYTHON) tools/build_skills.py --check
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest discover -s tests -v

test: $(INSTALL_STAMP)
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest discover -s tests -v

# Choose an absent or empty destination with: make build OUTPUT=dist/my-bundle
OUTPUT ?= dist/plugins
build: $(INSTALL_STAMP)
	$(PYTHON) tools/build_plugins.py --output "$(OUTPUT)"

# CI parity: validate without repair, then build into a disposable destination.
check-all: check
	@set -eu; temporary=$$(mktemp -d); trap 'rm -rf "$$temporary"' EXIT; \
	$(PYTHON) tools/build_plugins.py --output "$$temporary/plugins"
