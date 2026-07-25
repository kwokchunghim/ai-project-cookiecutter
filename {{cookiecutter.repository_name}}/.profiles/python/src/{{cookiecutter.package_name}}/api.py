"""FastAPI application factory."""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from {{ cookiecutter.package_name }}.settings import Settings


class HealthResponse(BaseModel):
    status: str
    service: str
    environment: str


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved = settings or Settings()
    app = FastAPI(title=resolved.service_name)

    @app.get("/healthz", response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse(
            status="ok",
            service=resolved.service_name,
            environment=resolved.environment,
        )

    return app
