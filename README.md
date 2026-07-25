# AI Project Cookiecutter

One Cookiecutter generator for three production-minded project shapes:

| Profile | Generated architecture |
|---|---|
| `python-core` | Python 3.12/uv package, provider-neutral model protocol, deterministic fake, CLI diagnostics, configs, tests, and eval guidance |
| `python-api` | Python core plus a FastAPI application factory, typed settings, `/healthz`, and API tests |
| `full-stack` | Vite, React, TypeScript, Tailwind, Supabase email/password Auth and Postgres, owned profiles protected by RLS, and Vercel SPA configuration |

Generated repositories are independent snapshots. They do not automatically receive
later changes from this template.

New here? Follow the audience-specific setup and first-change workflow in
[`ONBOARDING.md`](ONBOARDING.md).

Want to improve the template? Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening
an issue or pull request.

## Generate locally

```bash
cd /Users/tony/workspaces
uvx --from cookiecutter==2.7.1 cookiecutter ./ai-project-cookiecutter
cd <generated-project-slug>

git init -b main
make sync
make hooks
make check-all
```

Cookiecutter asks for:

1. `project_name`: the human-readable name.
2. `repository_name`: the derived lowercase kebab-case directory and repository slug.
3. `package_name`: the derived underscore-form Python package name. It is retained as
   metadata for every profile and used as an import name by Python profiles.
4. `description`: a one-sentence project summary.
5. `profile`: `python-core`, `python-api`, or `full-stack`.
6. `author_name`: the initial package/documentation author.
7. `github_owner`: the GitHub user or organization that will own a future repository.
8. `license`: `MIT`, `Apache-2.0`, or `Proprietary`.

Names are validated before generation. The post-generation hook selects the appropriate
committed lockfile, removes every unused profile file, and creates the real
`CLAUDE.md → AGENTS.md` symlink. Generation targets macOS and Linux because the symlink
is intentional.

After this template has been published, generate it directly from GitHub:

```bash
cd /Users/tony/workspaces
uvx --from cookiecutter==2.7.1 \
  cookiecutter gh:kwokchunghim/ai-project-cookiecutter
```

## Create the new GitHub repository

Run `make check-all` before the first push. The command below is the one permitted
direct push to `main`: it bootstraps a brand-new, empty remote with the initial
scaffold.

```bash
git add .
git commit -m "Create initial project scaffold"

gh repo create kwokchunghim/<project-slug> \
  --private \
  --source=. \
  --remote=origin

git push -u origin main
gh run watch
make github-protect
```

Replace `--private` with `--public` for a public repository. To connect a repository that
already exists on GitHub, skip `gh repo create`, run
`git remote add origin git@github.com:<owner>/<repository>.git`, and then push.

Wait for the initial CI workflow to succeed before running `make github-protect`;
GitHub cannot require a status check that has not appeared yet. The target is
idempotent. Preview its validated API payload without changing GitHub using
`make github-protect DRY_RUN=1`.

## Subsequent work

Preserve or resolve existing worktree changes before switching branches:

```bash
git switch main
git pull --ff-only origin main
git switch -c feat/short-description
gh pr create --draft
```

Use `feat/`, `fix/`, `docs/`, or `chore/` branches and focused commits. Never push
directly to `main` after the one-time empty-repository bootstrap, force-push, or rewrite
published history. Bring a published feature branch up to date by merging the current
`origin/main`, not by rebasing it.

## Template development

Contributor setup, issue policy, branch rules, and profile-specific verification are
documented in [`CONTRIBUTING.md`](CONTRIBUTING.md).

```bash
make sync
make check
```

`make check` renders and inspects all profiles in isolated temporary directories.
Generated repositories expose the same quality commands through Make and use pre-commit
as the shared local gate. See
[`docs/engineering-practices.md`](docs/engineering-practices.md) for the first-party
conventions applied here.
