"""Promote the selected profile and remove generator-only files."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path.cwd()
PROFILE = "{{ cookiecutter.profile }}"
PROFILE_GROUP = "full-stack" if PROFILE == "full-stack" else "python"
PROFILE_ROOT = ROOT / ".profiles" / PROFILE_GROUP


def promote_profile() -> None:
    for source in sorted(PROFILE_ROOT.rglob("*")):
        relative = source.relative_to(PROFILE_ROOT)
        if source.name in {"uv-core.lock", "uv-api.lock"}:
            continue

        destination = ROOT / relative
        if source.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
            continue

        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            raise RuntimeError(f"profile file would overwrite {destination}")
        shutil.move(str(source), str(destination))


def select_python_lockfile() -> None:
    lock_name = "uv-api.lock" if PROFILE == "python-api" else "uv-core.lock"
    shutil.copyfile(PROFILE_ROOT / lock_name, ROOT / "uv.lock")


def remove_core_api_files() -> None:
    if PROFILE != "python-core":
        return
    for relative in (
        "src/{{ cookiecutter.package_name }}/api.py",
        "src/{{ cookiecutter.package_name }}/settings.py",
        "tests/test_api.py",
    ):
        (ROOT / relative).unlink()


if PROFILE_GROUP == "python":
    select_python_lockfile()

promote_profile()
remove_core_api_files()
shutil.rmtree(ROOT / ".profiles")

claude_link = ROOT / "CLAUDE.md"
if claude_link.exists() or claude_link.is_symlink():
    claude_link.unlink()
claude_link.symlink_to("AGENTS.md")
