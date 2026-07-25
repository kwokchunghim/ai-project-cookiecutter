# Contributing

Thanks for helping improve AI Project Cookiecutter. This is a small project, so the
contribution process is intentionally lightweight: agree on code changes first, keep
the implementation focused, and show that the generated projects still work.

## Before you start

Open an issue before every non-documentation code change:

- use the bug form for incorrect or broken behavior;
- use the feature form for new behavior, refactors, dependencies, or architecture
  changes.

Small documentation corrections may go directly to a pull request. For a suspected
vulnerability, follow [SECURITY.md](SECURITY.md) instead of opening a public issue.

Discuss the smallest useful outcome before investing in substantial work. New profiles,
frameworks, deployment targets, dependencies, migrations, and security-sensitive
changes need explicit maintainer agreement.

## Set up a fork

Fork the repository on GitHub, then clone your fork and add this repository as
`upstream`:

```bash
git clone https://github.com/<your-user>/ai-project-cookiecutter.git
cd ai-project-cookiecutter
git remote add upstream \
  https://github.com/kwokchunghim/ai-project-cookiecutter.git

make sync
make check
```

The template targets macOS and Linux because generated repositories contain a real
`CLAUDE.md → AGENTS.md` symlink. Full-stack changes also require Node 24, npm 11, Docker,
and the pinned Supabase CLI installed through the generated project.

## Create a focused branch

Start from current `main`:

```bash
git fetch upstream
git switch main
git merge --ff-only upstream/main
git switch -c feat/short-description
```

Use a `feat/`, `fix/`, `docs/`, or `chore/` prefix. Preserve unrelated worktree changes,
keep commits limited to one concern, and do not push directly to `main`, force-push, or
rewrite published history. If a published branch needs updating, merge current
`upstream/main` into it rather than rebasing it.

## Make and verify the change

Follow [AGENTS.md](AGENTS.md): make the smallest change that solves the agreed problem,
add concrete tests for behavior changes, and avoid unrelated cleanup.

Run the checks appropriate to the change:

| Change | Required verification |
|---|---|
| Documentation or repository metadata | `make check` |
| Generator hooks or Python-profile output | `make check`, then the affected generated profile's `make check-all` |
| Full-stack output, migrations, RLS, or generated database types | `make check`, then the generated full-stack profile's `make check-all` with Docker running |

Use the local-generation workflow in [README.md](README.md) to exercise an affected
profile. Do not hand-edit generated lockfiles or database types; update their owning
manifest or migration and run the documented generator.

Never include credentials, private keys, personal data, production prompts, generated
local databases, or Supabase volumes in a commit.

## Open a pull request

Push your branch to your fork and open a draft pull request against this repository's
`main` branch:

```bash
git push -u origin <branch-name>
gh pr create \
  --repo kwokchunghim/ai-project-cookiecutter \
  --base main \
  --head <your-user>:<branch-name> \
  --draft
```

Link the issue for every code change. Describe the problem, the chosen minimal approach,
test evidence, and any security, privacy, migration, compatibility, or rollback impact.
Mark checks as not applicable only when the pull request explains why.

External pull requests require review from `@kwokchunghim` and passing CI.
Maintainer-authored pull requests rely on passing CI because GitHub does not allow
authors to approve their own pull requests. DCO sign-off, signed commits, and a human
approval on maintainer-authored pull requests are not required.
