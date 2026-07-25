"""Typed local configuration loaded from TOML."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class ProjectConfig:
    environment: str
    model_timeout_seconds: float
    model_max_output_tokens: int


def load_config(path: Path) -> ProjectConfig:
    raw: dict[str, Any]
    with path.open("rb") as stream:
        raw = tomllib.load(stream)
    project = raw["project"]
    model = raw["model"]
    return ProjectConfig(
        environment=str(project["environment"]),
        model_timeout_seconds=float(model["timeout_seconds"]),
        model_max_output_tokens=int(model["max_output_tokens"]),
    )
