# Evaluations

Evaluation cases should contain representative, redacted inputs and concrete expected
behavior. Keep deterministic fixtures in the default suite. Live-provider evaluation is
opt-in and must define quality thresholds, latency/token/cost budgets, failure handling,
and a safe retention policy before it is automated.

At minimum, cover normal inputs, malformed inputs, prompt-injection attempts, sensitive
data handling, provider errors, and output validation. Store aggregate results and
version metadata; do not commit raw production prompts or personal data.
