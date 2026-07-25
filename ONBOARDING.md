# Onboarding

This guide is for people generating a new project and contributors changing the
Cookiecutter itself. You do not need to know Cookiecutter internals to create a project.

## Choose a profile

| Start with | Choose it when | Main local tools |
|---|---|---|
| `python-core` | You need a Python AI library, batch job, worker, or CLI without an HTTP service | Python 3.12, uv |
| `python-api` | You also need a typed FastAPI service and health endpoint | Python 3.12, uv |
| `full-stack` | You need a browser app, authentication, owned Postgres data, and Vercel deployment | Node 24, npm 11, Docker |

Choose the smallest profile that supports the first real user flow. The Python profiles
do not select an AI provider. The full-stack profile intentionally uses Supabase and
Vercel and does not include a Python service.

## Prerequisites

All profiles require:

- macOS or Linux, because generated projects use a real symlink;
- Git;
- [uv](https://docs.astral.sh/uv/);
- a GitHub account and GitHub CLI if you will publish the generated repository.

The full-stack profile additionally requires Node 24, npm 11, and a running Docker
engine for local Supabase checks. It uses ports `55320`–`55322` so it can coexist with a
Supabase project using the default `5432x` ports.

Confirm the relevant tools:

```bash
git --version
uv --version
gh auth status

# Full-stack only
node --version
npm --version
docker info
```

## Generate a project

From the directory that should contain the new repository:

```bash
uvx --from cookiecutter==2.7.1 \
  cookiecutter gh:kwokchunghim/ai-project-cookiecutter
```

The prompts collect:

- the display name and one-sentence description;
- derived repository and Python package names;
- one of the three profiles;
- author and future GitHub owner;
- MIT, Apache-2.0, or proprietary licensing.

Review the derived names before accepting them. Repository names must be lowercase
kebab-case; Python package names must be lowercase identifiers with underscores.

## First 15 minutes in the generated repository

```bash
cd <generated-project-slug>
git init -b main
make sync
make hooks
make check-all
```

You should see:

- locked dependencies installed without changing the lockfile;
- formatting, linting, typechecking, and unit tests pass;
- a build complete;
- CLI/API integration tests for Python profiles; or
- a Supabase reset, RLS isolation tests, generated-type comparison, and Vite production
  build for the full-stack profile.

Run `make help` for profile-specific commands. Useful starting points are:

```bash
# Python core and API
make diagnostics

# Python API
make serve

# Full-stack
make db-start
make db-reset
make dev
```

Run `make db-stop` when you finish full-stack development.

## Make the first change

Read `AGENTS.md` and `CONTRIBUTING.md` in the generated repository before editing. They
define the working method, verification expectations, security boundaries, and branch
policy.

Start work from current `main`:

```bash
git switch main
git pull --ff-only origin main
git switch -c feat/short-description
```

Keep the change focused, add concrete tests with behavior changes, and run
`make check-all` before pushing. Open a draft pull request; do not push directly to
`main`, force-push, or rewrite published history. The only exception is the one-time
initial scaffold push that creates `main` in a brand-new, empty remote.

## Publish a generated repository

The generated README contains the complete first-push and protection workflow. Decide
whether the new repository should be public or private, run all checks, create it with
GitHub CLI, and wait for its first successful CI run before applying branch protection.
That initial scaffold push may go directly to `main`; all subsequent changes use
branches and pull requests.

Preview protection without changing GitHub:

```bash
make github-protect DRY_RUN=1
```

## Security and environment setup

- Copy `.env.example` to an ignored environment file; never put real credentials in the
  example.
- Keep provider secrets, service-role keys, database passwords, and production prompts
  out of browser bundles, tests, logs, and Git history.
- The full-stack browser uses only the Supabase URL, publishable key, and user JWT.
- Replace deterministic local seed accounts before using a hosted environment.
- Complete `docs/project-checklist.md` before a production release.

## Contribute to this template

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) for the issue-first workflow, fork setup,
branch policy, review expectations, and change-specific verification. After cloning the
template and creating a branch, run:

```bash
make sync
make check
```

`make check` renders and inspects all three profiles in temporary directories. When a
change affects generated behavior, also generate the affected profile and run its
`make check-all`. For full-stack database changes, verify migrations, seeds, positive
and negative RLS behavior, and generated types together.

Do not edit generated lockfiles or database types by hand. Change the owning manifest or
migration, run its generator, and review the resulting diff.

## Troubleshooting

- **`CLAUDE.md` is not a symlink:** generate on macOS/Linux and ensure the checkout
  preserves symlinks.
- **Docker or Supabase cannot start:** confirm Docker is running and ports
  `55320`–`55322` are free.
- **A locked install reports drift:** do not bypass it; refresh the lock with
  `make lock`, review the dependency changes, and rerun the complete gate.
- **Branch protection rejects a status check:** wait for the repository's first
  successful `CI / check` run, then retry `make github-protect`.
- **You expected template updates to appear:** generated repositories are independent
  snapshots. Adopt later template changes deliberately through a reviewed pull request.
