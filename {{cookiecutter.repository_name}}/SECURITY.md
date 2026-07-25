# Security policy

Do not report suspected vulnerabilities in public issues. Use GitHub's private
vulnerability reporting for `{{ cookiecutter.github_owner }}/{{ cookiecutter.repository_name }}`
when available, or contact the repository owner through a private channel listed on
their GitHub profile.

Include affected versions, impact, reproduction steps, and suggested mitigations. Do not
include real credentials, personal data, or production prompts in a report.

Before release, confirm:

- secrets and provider keys are stored outside the repository;
- logs and traces redact personal data, prompts, tokens, and credentials;
- data retention and deletion are documented;
- dependency and workflow updates have passed `make check-all`;
- backup, rollback, incident ownership, and security-reporting paths are tested.
{% if cookiecutter.profile == "full-stack" -%}
- every exposed Supabase table has ownership-aware RLS and allow/deny tests;
- browser bundles contain no service-role or secret keys.
{% endif %}

Report suspected vulnerabilities privately.
