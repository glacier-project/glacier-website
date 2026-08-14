# Maintenance commands for the GLACIER website. Run `make help` for the list.
# Uses .venv/bin if it exists, so it works with or without the venv activated.

PYTHON := $(shell [ -x .venv/bin/python ] && echo .venv/bin/python || echo python3)
MKDOCS := $(PYTHON) -m mkdocs
SITE_TREE := $(PYTHON) scripts/site_tree.py

.DEFAULT_GOAL := help
.PHONY: help serve build site-tree site-map check clean

help:  ## Show this list of commands
	@grep -E '^[a-z-]+:.*##' $(MAKEFILE_LIST) | sed 's/:.*##/\t/' | expand -t 12

serve:  ## Preview the website locally at http://127.0.0.1:8000
	$(MKDOCS) serve

build:  ## Build the site into site/, failing on any warning
	$(MKDOCS) build --strict

site-tree:  ## Print the complete public navigation as a tree
	@$(SITE_TREE)

site-map:  ## Regenerate docs/reference/site-map.md from the navigation
	@$(SITE_TREE) --site-map

check: build  ## Strict build, plus navigation and site-map consistency
	@$(SITE_TREE) --check

clean:  ## Remove the generated site/ directory
	rm -rf site
