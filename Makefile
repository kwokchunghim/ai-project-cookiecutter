.DEFAULT_GOAL := help
PRE_COMMIT := uvx --from pre-commit==4.3.0 pre-commit
.PHONY: help sync lock hooks format format-check lint test quality-all check render-test

help: ## Show available commands
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z_-]+:.*## / {printf "  %-16s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

sync: ## Install the locked template development environment
	uv sync --frozen

lock: ## Refresh the template development lockfile
	uv lock

hooks: ## Install pre-commit and pre-push hooks
	@test -d .git || (echo "Run git init -b main first" >&2; exit 1)
	$(PRE_COMMIT) install --hook-type pre-commit --hook-type pre-push

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

quality-all: format-check lint test ## Run template formatting, lint, and render tests

check: ## Run every pre-commit hook over the repository
	$(PRE_COMMIT) run --all-files --hook-stage manual
