from __future__ import annotations

from {{ cookiecutter.package_name }}.diagnostics import run_diagnostics
from {{ cookiecutter.package_name }}.testing import FakeModelClient


def test_diagnostics_probes_model_boundary() -> None:
    client = FakeModelClient({"diagnostic probe": "ready"})

    report = run_diagnostics(client)

    assert report.status == "ok"
    assert report.profile == "{{ cookiecutter.profile }}"
    assert report.model == "deterministic-fake"
    assert report.model_probe == "ready"
    assert client.requests[0].max_output_tokens == 16
