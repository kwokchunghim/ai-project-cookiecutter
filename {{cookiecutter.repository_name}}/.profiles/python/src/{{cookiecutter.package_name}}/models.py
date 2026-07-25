"""Provider-neutral model contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass(frozen=True, slots=True)
class ModelRequest:
    """Input shared by model-provider adapters."""

    prompt: str
    max_output_tokens: int = 256


@dataclass(frozen=True, slots=True)
class ModelResponse:
    """Normalized provider response and usage."""

    text: str
    model: str
    input_tokens: int
    output_tokens: int


@runtime_checkable
class ModelClient(Protocol):
    """Small boundary implemented by a concrete model provider."""

    def complete(self, request: ModelRequest) -> ModelResponse:
        """Return one normalized completion."""
        ...
