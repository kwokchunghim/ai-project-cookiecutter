"""Deterministic local diagnostics."""

from __future__ import annotations

import platform
from dataclasses import asdict, dataclass
from typing import Any

from {{ cookiecutter.package_name }}.models import ModelClient, ModelRequest


@dataclass(frozen=True, slots=True)
class DiagnosticReport:
    status: str
    profile: str
    python_version: str
    model: str
    model_probe: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def run_diagnostics(client: ModelClient) -> DiagnosticReport:
    response = client.complete(ModelRequest(prompt="diagnostic probe", max_output_tokens=16))
    return DiagnosticReport(
        status="ok",
        profile="{{ cookiecutter.profile }}",
        python_version=platform.python_version(),
        model=response.model,
        model_probe=response.text,
    )
