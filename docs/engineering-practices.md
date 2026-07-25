# Engineering practices and provenance

This template distils practices from three first-party projects. It does not copy their
product-specific architecture and does not adopt MLflow-specific contribution, DCO,
dependency, or architecture rules.

| Practice | Source convention | Template application |
|---|---|---|
| uv-managed Python 3.12, a small Make interface, declarative configs, tests, eval guidance, and provider boundaries | SubCore Agent | Both Python profiles |
| Application factory, separated contracts, CLI-first diagnostics, and deterministic automated tests | SubCore Agent | Python API and Python core |
| npm lockfile, Vite/React, browser-safe Supabase configuration, local database migrations, deterministic seed users, and positive/negative RLS tests | PoliLab | Full-stack |
| Strict RLS ownership checks, including `USING` and `WITH CHECK`, and no secret key in browser bundles | PoliLab | Full-stack |
| Focused Vite SPA, TypeScript build gate, Tailwind through the Vite plugin, and simple local developer commands | SubCore Agent Demo | Full-stack |
| Small focused commits, test-with-change cadence, explicit success signals, and preservation of unrelated worktree changes | All three | Generated `AGENTS.md` and `CONTRIBUTING.md` |

The generated model interface is deliberately provider-neutral. The template does not
select an AI vendor, observability vendor, experiment tracker, hosting database, or
hosted deployment. Supabase and Vercel are selected only by the explicit full-stack
profile contract.
