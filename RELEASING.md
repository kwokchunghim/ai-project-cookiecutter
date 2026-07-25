# Releasing

This guide covers releases of AI Project Cookiecutter itself. Repositories generated
from the template are independent projects with their own versions and release
decisions.

## Policy

- Keep `main` releasable. Merge focused pull requests after their required checks pass;
  do not hold completed work for a release branch or release day.
- Publish a release when a meaningful user-facing set of template changes is ready.
  Routine documentation or dependency maintenance does not require a release unless it
  changes what users receive or a reproducible checkpoint is useful.
- Create releases only from tested commits already merged into `main`.
- Never move, delete, or reuse a published tag.
- Do not create a tag, GitHub release, or deployment without explicit maintainer
  authorization.

GitHub-generated release notes are sufficient for this project's current size. There is
no separate release branch or manually maintained changelog.

## Choose a version

Use semantic versions:

- Patch (`v0.1.1`) for compatible fixes, security updates, and maintenance checkpoints.
- Minor (`v0.2.0`) for new prompts, profiles, or other meaningful template capabilities.
  Before `v1.0.0`, also use a minor release for breaking changes and call them out
  prominently in the release notes.
- Major (`v2.0.0`) after `v1.0.0` for changes that break established generation or
  upgrade expectations.

The template's version does not set the version of a generated project. A project
created from template release `v0.2.0` can still begin its own lifecycle at `0.1.0`.

## Publish a release

Start with a clean checkout of current `main`, then run the repository's complete
quality gate:

```bash
git switch main
git pull --ff-only origin main
git status --short
make sync
make check
```

Confirm GitHub Actions passed for the same commit:

```bash
git rev-parse HEAD
gh run list --branch main --commit "$(git rev-parse HEAD)"
```

Choose an unused `vX.Y.Z` version and create the release at that exact commit:

```bash
gh release create vX.Y.Z \
  --target "$(git rev-parse HEAD)" \
  --title "vX.Y.Z — <short release name>" \
  --generate-notes
```

Verify both the published release and its remote tag:

```bash
gh release view vX.Y.Z
git ls-remote --tags origin refs/tags/vX.Y.Z
```

If preparation fails, fix the problem through the normal pull-request workflow and
restart from updated `main`. Do not retag a different commit.

## Generate from a release

The default GitHub command uses the repository's current default branch. Select a tag
when a reproducible template snapshot is more important than receiving the latest
merged changes:

```bash
uvx --from cookiecutter==2.7.1 \
  cookiecutter --checkout vX.Y.Z \
  gh:kwokchunghim/ai-project-cookiecutter
```
