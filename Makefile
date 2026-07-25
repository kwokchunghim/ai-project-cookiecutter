.DEFAULT_GOAL := help
.PHONY: help sync lock format format-check lint test check render-test

help: ## Show available commands
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z_-]+:.*## / {printf "  %-16s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

sync: ## Install the locked template development environment
	uv sync --frozen

lock: ## Refresh the template development lockfile
	uv lock

format: ## Format template support code
	uv run ruff format hooks tests
	uv run ruff check --fix hooks tests

format-check: ## Check formatting without changing files
	uv run ruff format --check hooks tests

lint: ## Lint template support code
	uv run ruff check hooks tests

test: ## Render and inspect all profiles
	uv run pytest

render-test: test ## Alias for the isolated profile rendering suite

check: format-check lint test ## Run every template-level check
