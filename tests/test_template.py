from __future__ import annotations

import os
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
