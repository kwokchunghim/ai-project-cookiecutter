# Configuration

Keep non-secret, reviewable defaults in TOML. Put credentials and environment-specific
overrides in ignored environment files or a secret manager. Provider adapters should
translate this provider-neutral configuration at the outer boundary.
