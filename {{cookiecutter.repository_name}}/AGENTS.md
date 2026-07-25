# {{ cookiecutter.project_name }} Project Instructions

## Working method

1. State assumptions and measurable success criteria before editing.
2. Inspect existing implementation and tests first.
3. Choose the simplest approach that meets the request; surface meaningful alternatives.
4. Make surgical changes. Do not refactor, reformat, or clean up unrelated code.
5. Add concrete tests with behavior changes and run the relevant checks.
6. Review the final diff for unrelated changes, generated noise, and leaked secrets.

If the request is ambiguous in a way that changes architecture or behavior, stop, name
the uncertainty, and ask. Remove only imports, variables, functions, or files made
obsolete by the current change. Mention pre-existing dead code without deleting it.

## Verification

Turn work into observable goals: reproduce a bug with a failing test, implement the
smallest fix, then make that test and the affected quality gates pass. Tests must use
concrete inputs and expected outputs; do not rely on trivial assertions or bare mock-call
checks. A successful build or import is not behavioral verification.

Run `make check-all` before handoff. Explain any check that could not run and do not claim
it passed.

## AI, data, and operations

- Keep model integrations behind typed provider-neutral interfaces. Default tests to
  deterministic fakes; live-provider tests are opt-in.
- Redact PII, prompts, credentials, and sensitive features from logs and traces.
- Define evaluation datasets, quality thresholds, provider budgets, and failure behavior
  before enabling production AI paths.
- Document observability, data retention/deletion, environment separation, backup and
  rollback, security reporting, and release/versioning decisions.
- Secrets belong only in ignored environment files or a secret manager. Never commit
  local databases, model artifacts, raw datasets, Supabase volumes, or credentials.
{% if cookiecutter.profile == "full-stack" %}
- Browser code may use only the Supabase URL, publishable key, and the user's JWT. Never
  expose a secret/service-role key.
- Enable RLS on every exposed table. Ownership or membership must be explicit; `TO
  authenticated` alone is not authorization. Updates require both `USING` and
  `WITH CHECK`.
- Create schema changes as migrations, reset them against local Supabase, regenerate
  database types, and run both allow and deny RLS tests.
{% endif %}

## Git workflow

Preserve or resolve existing worktree changes. Switch to `main`, fast-forward with
`git pull --ff-only origin main`, then create a `feat/`, `fix/`, `docs/`, or `chore/`
branch. Keep commits focused and open a draft pull request.

A one-time direct push of the initial scaffold may create `main` in a brand-new, empty
remote. After that bootstrap push, never push directly to `main`, force-push, or rewrite
published history. Merge current `origin/main` into a published feature branch instead
of rebasing it. Do not commit, push, or create pull requests unless the user asks.

For a larger change, use an ordered series of independently reviewable commits. Each
commit must represent one logical change, leave the repository in a valid state, and
pass the required hooks.

Before creating any commit that will be pushed to a remote, run `make hooks` once in the
checkout and leave both the pre-commit and pre-push hooks enabled. Never use
`git commit --no-verify`, `git push --no-verify`, or `SKIP` to bypass required hooks.
Fix hook failures and rerun the original command. Run `make check-all` before pushing
even when the installed hooks have already passed.
