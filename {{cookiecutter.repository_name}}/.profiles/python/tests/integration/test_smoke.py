{% if cookiecutter.profile == "python-api" -%}
from __future__ import annotations

import json
import subprocess
import sys

from fastapi.testclient import TestClient

from {{ cookiecutter.package_name }}.api import create_app


def test_installed_cli_diagnostics() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "{{ cookiecutter.package_name }}.cli", "diagnostics"],
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["profile"] == "{{ cookiecutter.profile }}"
    assert payload["model_probe"] == "diagnostic-ok"


def test_application_factory_health_smoke() -> None:
    response = TestClient(create_app()).get("/healthz")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
{% else -%}
from __future__ import annotations

import json
import subprocess
import sys


def test_installed_cli_diagnostics() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "{{ cookiecutter.package_name }}.cli", "diagnostics"],
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["profile"] == "{{ cookiecutter.profile }}"
    assert payload["model_probe"] == "diagnostic-ok"
{% endif %}

# End of generated smoke tests.
