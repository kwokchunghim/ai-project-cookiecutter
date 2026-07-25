from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest
from cookiecutter.exceptions import FailedHookException
from cookiecutter.main import cookiecutter

TEMPLATE_ROOT = Path(__file__).parents[1]
PROFILES = ("python-core", "python-api", "full-stack")
COMMON_FILES = {
    "README.md",
    "Makefile",
    "AGENTS.md",
    "CLAUDE.md",
    ".pre-commit-config.yaml",
    ".github/workflows/ci.yml",
    "scripts/github_protect.py",
}


def test_root_release_guidance_is_linked() -> None:
    guidance = (TEMPLATE_ROOT / "RELEASING.md").read_text()
    readme = (TEMPLATE_ROOT / "README.md").read_text()
    contributing = (TEMPLATE_ROOT / "CONTRIBUTING.md").read_text()
    agent_guidance = (TEMPLATE_ROOT / "AGENTS.md").read_text()

    assert "Keep `main` releasable" in guidance
    assert "explicit maintainer" in guidance
    assert "never move" in guidance.lower()
    assert "--checkout vX.Y.Z" in guidance
    assert "[`RELEASING.md`](RELEASING.md)" in readme
    assert "[RELEASING.md](RELEASING.md)" in contributing
    assert "explicitly authorizes" in agent_guidance


def render(tmp_path: Path, profile: str) -> Path:
    name = f"rendered-{profile}"
    result = cookiecutter(
        str(TEMPLATE_ROOT),
        no_input=True,
        output_dir=str(tmp_path),
        extra_context={
            "project_name": f"Rendered {profile}",
            "repository_name": name,
            "package_name": name.replace("-", "_"),
            "description": f"Render test for {profile}.",
            "profile": profile,
            "author_name": "Template Test",
            "github_owner": "kwokchunghim",
            "license": "MIT",
        },
    )
    return Path(result)


@pytest.mark.parametrize("profile", PROFILES)
def test_profile_renders_without_generator_artifacts(tmp_path: Path, profile: str) -> None:
    project = render(tmp_path, profile)

    assert COMMON_FILES <= {str(path.relative_to(project)) for path in project.rglob("*")}
    assert not (project / ".profiles").exists()
    assert (project / "CLAUDE.md").is_symlink()
    assert os.readlink(project / "CLAUDE.md") == "AGENTS.md"

    for path in project.rglob("*"):
        if path.is_file() and path.stat().st_size < 1_000_000:
            assert "{{ cookiecutter." not in path.read_text(errors="ignore")


def test_python_core_contains_only_core_architecture(tmp_path: Path) -> None:
    project = render(tmp_path, "python-core")
    package = project / "src/rendered_python_core"

    assert (project / "uv.lock").is_file()
    assert (package / "models.py").is_file()
    assert (package / "cli.py").is_file()
    assert not (package / "api.py").exists()
    assert not (package / "settings.py").exists()
    assert not (project / "package.json").exists()
    assert not (project / "supabase").exists()


def test_python_api_adds_only_api_architecture(tmp_path: Path) -> None:
    project = render(tmp_path, "python-api")
    package = project / "src/rendered_python_api"

    assert (project / "uv.lock").is_file()
    assert (package / "api.py").is_file()
    assert (package / "settings.py").is_file()
    assert (project / "tests/test_api.py").is_file()
    assert not (project / "package.json").exists()


def test_full_stack_contains_no_python_service(tmp_path: Path) -> None:
    project = render(tmp_path, "full-stack")

    assert (project / "package-lock.json").is_file()
    assert (project / "src/App.tsx").is_file()
    assert (project / "supabase/migrations/20260725000000_profiles.sql").is_file()
    assert (project / "vercel.json").is_file()
    assert not (project / "pyproject.toml").exists()
    assert not (project / "uv.lock").exists()
    assert not list(project.rglob("*.py")) or list(project.rglob("*.py")) == [
        project / "scripts/github_protect.py"
    ]


def test_generated_agent_guidance_requires_modular_verified_commits(
    tmp_path: Path,
) -> None:
    project = render(tmp_path, "python-core")
    guidance = (project / "AGENTS.md").read_text()

    assert "commit must represent one logical change" in guidance
    assert "git commit --no-verify" in guidance
    assert "git push --no-verify" in guidance
    assert "`SKIP`" in guidance
    assert "Run `make check-all` before pushing" in guidance


@pytest.mark.parametrize("profile", PROFILES)
def test_generated_release_guidance_requires_authorized_immutable_releases(
    tmp_path: Path,
    profile: str,
) -> None:
    project = render(tmp_path, profile)
    agent_guidance = " ".join((project / "AGENTS.md").read_text().split())
    contributor_guidance = " ".join((project / "CONTRIBUTING.md").read_text().split())

    assert not (project / "RELEASING.md").exists()
    assert "explicitly authorizes" in agent_guidance
    assert "tested commit" in agent_guidance
    assert "never move or reuse a published tag" in agent_guidance
    assert "Keep `main` releasable" in contributor_guidance
    assert "Tagged releases are optional" in contributor_guidance
    assert "semantic versions" in contributor_guidance


def test_full_stack_retries_transient_type_generation_failure(tmp_path: Path) -> None:
    project = render(tmp_path, "full-stack")
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    counter = tmp_path / "npm-invocations"
    fake_npm = fake_bin / "npm"
    fake_npm.write_text(
        """#!/bin/sh
count="$(cat "$FAKE_NPM_COUNTER" 2>/dev/null || printf 0)"
count=$((count + 1))
printf '%s' "$count" > "$FAKE_NPM_COUNTER"
case "$*" in
  *"supabase gen types"*)
    test "$count" -ge 3 || exit 1
    cat "$EXPECTED_TYPES"
    ;;
  *"prettier --write"*) ;;
  *) exit 1 ;;
esac
"""
    )
    fake_npm.chmod(0o755)
    fake_sleep = fake_bin / "sleep"
    fake_sleep.write_text("#!/bin/sh\nexit 0\n")
    fake_sleep.chmod(0o755)
    env = {
        **os.environ,
        "EXPECTED_TYPES": str(project / "src/types/database.ts"),
        "FAKE_NPM_COUNTER": str(counter),
        "PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}",
    }

    subprocess.run(
        ["./scripts/check_database_types.sh"],
        cwd=project,
        env=env,
        check=True,
    )

    assert counter.read_text() == "4"


def test_invalid_repository_name_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(FailedHookException):
        cookiecutter(
            str(TEMPLATE_ROOT),
            no_input=True,
            output_dir=str(tmp_path),
            extra_context={
                "repository_name": "../unsafe",
                "package_name": "unsafe",
            },
        )
