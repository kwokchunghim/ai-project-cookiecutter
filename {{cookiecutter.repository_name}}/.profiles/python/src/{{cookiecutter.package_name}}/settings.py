"""Typed API settings."""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="{{ cookiecutter.package_name | upper }}_",
        env_file=".env",
        extra="ignore",
    )

    service_name: str = "{{ cookiecutter.repository_name }}"
    environment: str = "local"
    log_level: str = Field(default="INFO", pattern=r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
