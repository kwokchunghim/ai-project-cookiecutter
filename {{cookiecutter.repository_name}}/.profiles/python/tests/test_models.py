from __future__ import annotations

import pytest

from {{ cookiecutter.package_name }}.models import ModelClient, ModelRequest
from {{ cookiecutter.package_name }}.testing import FakeModelClient


def test_fake_model_client_returns_configured_response_and_usage() -> None:
    client = FakeModelClient({"summarize this": "short answer"})

    response = client.complete(ModelRequest("summarize this", max_output_tokens=12))

    assert isinstance(client, ModelClient)
    assert response.text == "short answer"
    assert response.model == "deterministic-fake"
    assert response.input_tokens == 2
    assert response.output_tokens == 2
    assert client.requests == [ModelRequest("summarize this", max_output_tokens=12)]


def test_fake_model_client_rejects_unconfigured_prompt() -> None:
    client = FakeModelClient({})

    with pytest.raises(ValueError, match="no fake response configured"):
        client.complete(ModelRequest("unknown"))
