from __future__ import annotations

from fastapi.testclient import TestClient

from {{ cookiecutter.package_name }}.api import create_app
from {{ cookiecutter.package_name }}.settings import Settings


def test_health_endpoint_uses_typed_settings() -> None:
    app = create_app(Settings(service_name="test-service", environment="test"))

    response = TestClient(app).get("/healthz")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "test-service",
        "environment": "test",
    }
