# Contributing

Start from updated `main` on a focused branch:

```bash
git switch main
git pull --ff-only origin main
git switch -c feat/short-description
make sync
make hooks
```

Use `feat/`, `fix/`, `docs/`, or `chore/` prefixes. Keep each commit limited to one
logical concern, add concrete tests with behavior changes, and run `make check-all`
before pushing. Open a draft pull request early.

Preserve unrelated worktree changes. The initial scaffold may be pushed directly to
`main` once to bootstrap a brand-new, empty remote. After that, never push directly to
`main`, force-push, or rewrite published history. Merge `origin/main` into a published
branch instead of rebasing it.

Pull requests should explain the problem, the chosen minimal approach, test evidence,
manual or operational verification, and any security, privacy, migration, or rollback
impact. DCO and signed commits are not mandatory.

## Releases

Keep `main` releasable by merging focused pull requests only after their required checks
pass. Tagged releases are optional until the project is distributed or deployed. When
the project needs releases, use semantic versions unless it documents another scheme,
tag only tested commits already merged into `main`, record user-visible changes, and
never move or reuse a published tag.
