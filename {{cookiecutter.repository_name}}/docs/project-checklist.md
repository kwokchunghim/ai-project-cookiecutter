# Production-readiness checklist

- [ ] Document data retention, deletion, and legal requirements.
- [ ] Inventory PII and redact PII, prompts, credentials, and sensitive features from
      logs, traces, fixtures, and support output.
- [ ] Define representative evaluations, expected outputs, thresholds, and regression
      ownership.
- [ ] Set provider request, token, latency, and monetary budgets with failure behavior.
- [ ] Add service, model, data-quality, cost, and security observability.
- [ ] Separate local, test, staging, and production credentials and data.
- [ ] Test database/configuration backups and a rollback procedure.
- [ ] Define release/versioning policy and compatibility guarantees.
- [ ] Document private security reporting, triage ownership, and incident response.
- [ ] Verify least privilege, dependency updates, and `make check-all` before release.
