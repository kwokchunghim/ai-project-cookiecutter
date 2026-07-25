"""Validate values before Cookiecutter writes a project."""

from __future__ import annotations

import re
import sys

REPOSITORY_NAME = "{{ cookiecutter.repository_name }}"
PACKAGE_NAME = "{{ cookiecutter.package_name }}"
GITHUB_OWNER = "{{ cookiecutter.github_owner }}"
PROFILE = "{{ cookiecutter.profile }}"


def fail(message: str) -> None:
    print(f"Cookiecutter input error: {message}", file=sys.stderr)
    raise SystemExit(1)


if not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", REPOSITORY_NAME):
    fail("repository_name must be a lowercase kebab-case slug beginning with a letter")

if not re.fullmatch(r"[a-z][a-z0-9_]*", PACKAGE_NAME):
    fail("package_name must be a lowercase Python identifier")

if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", GITHUB_OWNER):
    fail("github_owner is not a valid GitHub user or organization name")

if PROFILE not in {"python-core", "python-api", "full-stack"}:
    fail(f"unsupported profile: {PROFILE}")
