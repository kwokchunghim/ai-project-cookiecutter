#!/usr/bin/env python3
"""Apply an idempotent main-branch protection policy through GitHub CLI."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from typing import Any

DEFAULT_REPOSITORY = "{{ cookiecutter.github_owner }}/{{ cookiecutter.repository_name }}"
REQUIRED_CHECKS = ["check"]


def protection_payload() -> dict[str, Any]:
    return {
        "required_status_checks": {
            "strict": True,
            "contexts": REQUIRED_CHECKS,
        },
        "enforce_admins": False,
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": False,
            "require_code_owner_reviews": False,
            "required_approving_review_count": 0,
        },
        "restrictions": None,
        "required_conversation_resolution": True,
        "allow_force_pushes": False,
        "allow_deletions": False,
    }


def validate_repository(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", value):
        raise ValueError("repository must have owner/name form")
    return value


def resolve_repository(explicit: str | None) -> str:
    if explicit:
        return validate_repository(explicit)
    result = subprocess.run(
        ["gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"],
        check=True,
        capture_output=True,
        text=True,
    )
    return validate_repository(result.stdout.strip())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--repo", help="GitHub repository in owner/name form")
    args = parser.parse_args()

    payload = protection_payload()
    repository = validate_repository(args.repo or DEFAULT_REPOSITORY)

    if args.dry_run:
        print(f"Dry run for {repository} main:")
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    repository = resolve_repository(args.repo)
    subprocess.run(
        [
            "gh",
            "api",
            "--method",
            "PUT",
            f"repos/{repository}/branches/main/protection",
            "--input",
            "-",
        ],
        check=True,
        input=json.dumps(payload),
        text=True,
    )
    print(f"Protected {repository}:main")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, subprocess.CalledProcessError, ValueError) as error:
        print(f"github-protect failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
