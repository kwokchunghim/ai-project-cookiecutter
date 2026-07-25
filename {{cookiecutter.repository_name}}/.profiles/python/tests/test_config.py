from __future__ import annotations

from pathlib import Path

from {{ cookiecutter.package_name }}.config import ProjectConfig, load_config


def test_load_config_reads_typed_defaults() -> None:
    config = load_config(Path("configs/default.toml"))

    assert config == ProjectConfig(
        environment="local",
        model_timeout_seconds=30.0,
        model_max_output_tokens=256,
    )
