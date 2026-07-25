"""Deterministic test doubles for model-dependent code."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from {{ cookiecutter.package_name }}.models import ModelRequest, ModelResponse


@dataclass(slots=True)
class FakeModelClient:
    """Return explicit fixture responses without network calls or randomness."""

    responses: Mapping[str, str]
    model: str = "deterministic-fake"
    requests: list[ModelRequest] = field(default_factory=list)

    def complete(self, request: ModelRequest) -> ModelResponse:
        self.requests.append(request)
        try:
            text = self.responses[request.prompt]
        except KeyError as error:
            raise ValueError(f"no fake response configured for {request.prompt!r}") from error
        return ModelResponse(
            text=text,
            model=self.model,
            input_tokens=len(request.prompt.split()),
            output_tokens=len(text.split()),
        )
