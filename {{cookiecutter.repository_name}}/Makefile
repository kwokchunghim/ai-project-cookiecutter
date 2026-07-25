.DEFAULT_GOAL := help
PROFILE := {{ cookiecutter.profile }}
PRE_COMMIT := uvx --from pre-commit==4.3.0 pre-commit
.PHONY: help sync lock hooks format format-check lint typecheck test build quality-all check check-all test-integration github-protect{% if cookiecutter.profile != "full-stack" %} diagnostics{% if cookiecutter.profile == "python-api" %} serve{% endif %}{% else %} dev db-start db-stop db-reset db-types db-types-check test-rls db-verify{% endif %}

help: ## Show available commands
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z_-]+:.*## / {printf "  %-18s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

{% if cookiecutter.profile != "full-stack" -%}
sync: ## Install exact dependencies from uv.lock
	uv sync --frozen

lock: ## Refresh uv.lock
	uv lock

hooks: ## Install pre-commit and pre-push hooks
	@test -d .git || (echo "Run git init -b main first" >&2; exit 1)
	$(PRE_COMMIT) install --hook-type pre-commit --hook-type pre-push

format: ## Format Python and apply safe lint fixes
	uv run ruff format .
	uv run ruff check --fix .

format-check: ## Check Python formatting without changing files
	uv run ruff format --check .

lint: ## Lint Python
	uv run ruff check .

typecheck: ## Run strict static type checking
	uv run mypy src tests

test: ## Run unit tests
	uv run pytest tests --ignore=tests/integration

build: ## Build wheel and source distribution
	uv build

diagnostics: ## Run deterministic CLI diagnostics
	uv run {{ cookiecutter.repository_name }} diagnostics

{% if cookiecutter.profile == "python-api" -%}
serve: ## Start the local FastAPI service
	uv run uvicorn {{ cookiecutter.package_name }}.api:create_app --factory --reload

{% endif -%}
test-integration: ## Run CLI{% if cookiecutter.profile == "python-api" %} and API{% endif %} integration tests
	uv run pytest tests/integration
{% else -%}
sync: ## Install exact dependencies from package-lock.json
	npm ci

lock: ## Refresh package-lock.json without running package scripts
	npm install --package-lock-only --ignore-scripts

hooks: ## Install pre-commit and pre-push hooks
	@test -d .git || (echo "Run git init -b main first" >&2; exit 1)
	$(PRE_COMMIT) install --hook-type pre-commit --hook-type pre-push

format: ## Format frontend and configuration files
	npm run format

format-check: ## Check formatting without changing files
	npm run format:check

lint: ## Lint TypeScript and React
	npm run lint

typecheck: ## Run strict TypeScript checks
	npm run typecheck

test: ## Run frontend unit tests
	npm run test

build: ## Build the production Vite SPA
	npm run build

dev: ## Start the local Vite server
	npm run dev

db-start: ## Start the profile-owned local Supabase stack
	npm exec -- supabase start

db-stop: ## Stop the profile-owned local Supabase stack
	npm exec -- supabase stop --no-backup

db-reset: ## Replay migrations and deterministic seed data
	npm exec -- supabase db reset

db-types: ## Regenerate committed database types
	npm exec -- supabase gen types typescript --local > src/types/database.ts
	npm exec -- prettier --write src/types/database.ts

db-types-check: ## Reject generated database type drift
	./scripts/check_database_types.sh

test-rls: ## Exercise owner access and outsider denial through PostgREST
	npm run test:rls

db-verify: ## Start, reset, test RLS, and check generated type drift
	./scripts/verify_supabase.sh

test-integration: db-verify ## Run local Supabase integration checks
{% endif %}
quality-all: format-check lint typecheck test ## Always-run pre-commit quality gate

check: ## Run every pre-commit hook over the repository
	$(PRE_COMMIT) run --all-files --hook-stage manual

check-all: check build test-integration ## Add builds and integration tests

github-protect: ## Apply main protection; set DRY_RUN=1 to print only
	python3 scripts/github_protect.py $(if $(filter 1 true yes,$(DRY_RUN)),--dry-run,)
