# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

Profile: `{{ cookiecutter.profile }}` · License: `{{ cookiecutter.license }}`

{% if cookiecutter.profile == "python-core" -%}
This is a Python 3.12/uv package with a provider-neutral `ModelClient` protocol,
deterministic test fake, declarative configuration, and CLI diagnostics.
{% elif cookiecutter.profile == "python-api" -%}
This is a Python 3.12/uv package with the core model boundary plus a FastAPI application
factory, typed environment settings, `/healthz`, and API tests.
{% else -%}
This is a Vite/React/TypeScript/Tailwind SPA backed by Supabase email/password Auth and
Postgres. The included profile slice uses browser-safe credentials and ownership-based
RLS. Vercel serves the static SPA; there is no Python service.
{% endif %}

## Start locally

```bash
git init -b main
make sync
make hooks
make check-all
```

{% if cookiecutter.profile == "python-core" -%}
Run diagnostics with `make diagnostics`.
{% elif cookiecutter.profile == "python-api" -%}
Run diagnostics with `make diagnostics` or start the API with `make serve`. The health
endpoint is `GET http://127.0.0.1:8000/healthz`.
{% else -%}
Copy `.env.example` to `.env.local`, start Supabase with `make db-start`, reset migrations
and deterministic seed users with `make db-reset`, then run `make dev`. Browser code must
contain only the Supabase URL and publishable key; never add a secret or service-role key.
Use `make db-verify` to replay migrations and seeds, exercise owner/outsider RLS, regenerate
database types into a temporary file, and reject drift.
{% endif %}

## Quality commands

`make sync`, `lock`, `hooks`, `format`, `format-check`, `lint`, `typecheck`, `test`,
`build`, `check`, and `check-all` are stable project interfaces. `make check` runs every
pre-commit hook over tracked files and always runs formatting checks, linting, typechecks,
and unit tests. The installed pre-push hook runs `make check-all`, adding builds and
integration checks.

## Create the GitHub repository

Run `make check-all` before the initial push. This is the one permitted direct push to
`main`, used only to bootstrap a brand-new, empty remote:

```bash
git add .
git commit -m "Create initial project scaffold"

gh repo create {{ cookiecutter.github_owner }}/{{ cookiecutter.repository_name }} \
  --private \
  --source=. \
  --remote=origin

git push -u origin main
gh run watch
make github-protect
```

Use `--public` instead of `--private` for a public repository. For an existing remote:

```bash
git remote add origin git@github.com:<owner>/<repository>.git
git push -u origin main
```

Wait for the first successful CI run before requiring its status check. Preview the
idempotent branch-protection payload without changing GitHub:

```bash
make github-protect DRY_RUN=1
```

## Branch workflow

Preserve or resolve worktree changes, then:

```bash
git switch main
git pull --ff-only origin main
git switch -c feat/short-description
gh pr create --draft
```

Use a `feat/`, `fix/`, `docs/`, or `chore/` branch and focused commits. After the
one-time empty-repository bootstrap, never push directly to `main`, force-push, or
rewrite published history. Merge current `origin/main` into a published feature branch
rather than rebasing it.

This repository is an independent snapshot. It will not automatically receive later
changes from the Cookiecutter template.
