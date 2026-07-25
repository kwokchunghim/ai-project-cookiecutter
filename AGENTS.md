# AI Project Cookiecutter Instructions

## Working method

1. State assumptions and measurable success criteria before editing.
2. Inspect the rendered profiles and tests that cover the affected behavior.
3. Make the smallest change that meets the requirement.
4. Add or update a concrete test with each behavior change.
5. Run `make check` and the affected generated profile's `make check-all`.
6. Review the diff for unrelated changes, generated noise, secrets, and unresolved Jinja.

Do not silently choose between ambiguous requirements. Explain the alternatives and ask
when the choice materially changes the generated architecture.

## Scope and simplicity

- Keep one conditional skeleton and three supported profiles: `python-core`,
  `python-api`, and `full-stack`.
- Do not add optional frameworks, providers, deployment targets, or abstractions without
  a demonstrated requirement.
- Touch only files that trace directly to the active task. Preserve unrelated worktree
  changes and mention unrelated dead code instead of removing it.
- Remove imports, variables, and files only when the active change makes them unused.

## Verification and safety

- Reproduce bugs with a test before fixing them.
- Use concrete inputs and expected outputs; builds and import checks are not behavioral
  verification.
- Never commit credentials, generated local databases, Supabase volumes, or test data
  containing real personal information.
- Never delete generated smoke repositories unless every independent allowlist and
  content check in the smoke-test procedure passes.

## Git workflow

Preserve existing changes, update `main` with a fast-forward-only pull, then work on a
`feat/`, `fix/`, `docs/`, or `chore/` branch. Keep commits focused and open a draft pull
request. A one-time direct push of the initial scaffold may create `main` in a new,
empty remote. After that bootstrap push, never push directly to `main`, force-push, or
rewrite published history. Merge the current `origin/main` into a published feature
branch instead of rebasing it.

Before creating any commit that will be pushed to a remote, run `make hooks` once in the
checkout and leave both the pre-commit and pre-push hooks enabled. Never use
`git commit --no-verify`, `git push --no-verify`, or `SKIP` to bypass required hooks.
Fix hook failures and rerun the original command. Run `make check` before pushing even
when the installed hooks have already passed.
