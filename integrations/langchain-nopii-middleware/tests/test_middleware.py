"""Tests for NoPIIMiddleware - verify model rebinding without making real LLM calls."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from langchain_nopii_middleware import (
    DEFAULT_NOPII_BASE_URL,
    NoPIIMiddleware,
    UnsupportedModelError,
)
from langchain_nopii_middleware.middleware import SESSION_HEADER


def test_default_base_url_constant() -> None:
    assert DEFAULT_NOPII_BASE_URL == "https://api.nopii.co"


def test_trailing_slash_stripped() -> None:
    mw = NoPIIMiddleware(base_url="https://proxy.example.com/")
    assert mw.base_url == "https://proxy.example.com"


def test_unsupported_model_raises() -> None:
    mw = NoPIIMiddleware()

    class WeirdModel:
        pass

    with pytest.raises(UnsupportedModelError, match="WeirdModel"):
        mw._reroute(WeirdModel())


# ------ ChatOpenAI ------


@pytest.fixture
def chat_openai():
    pytest.importorskip("langchain_openai")
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(model="gpt-4o-mini", api_key="sk-test-not-real")


def test_openai_reroute_changes_base_url(chat_openai) -> None:
    mw = NoPIIMiddleware(base_url="https://proxy.example.com")
    new_model = mw._reroute(chat_openai)

    assert new_model.openai_api_base == "https://proxy.example.com/v1"
    assert chat_openai.openai_api_base != new_model.openai_api_base, (
        "original model must not be mutated"
    )


def test_openai_reroute_rebuilds_client(chat_openai) -> None:
    """The underlying openai SDK client must actually point at the new base URL."""
    mw = NoPIIMiddleware(base_url="https://proxy.example.com")
    new_model = mw._reroute(chat_openai)

    assert new_model.root_client is not None
    assert str(new_model.root_client.base_url).startswith("https://proxy.example.com/v1")
    assert new_model.root_async_client is not None
    assert str(new_model.root_async_client.base_url).startswith("https://proxy.example.com/v1")


def test_openai_session_header_attached(chat_openai) -> None:
    mw = NoPIIMiddleware(session_id="sess-abc")
    new_model = mw._reroute(chat_openai)

    headers = new_model.default_headers or {}
    assert headers.get(SESSION_HEADER) == "sess-abc"


def test_openai_no_session_header_when_unset(chat_openai) -> None:
    mw = NoPIIMiddleware()
    new_model = mw._reroute(chat_openai)

    headers = new_model.default_headers or {}
    assert SESSION_HEADER not in headers


# ------ ChatAnthropic ------


@pytest.fixture
def chat_anthropic():
    pytest.importorskip("langchain_anthropic")
    from langchain_anthropic import ChatAnthropic

    return ChatAnthropic(
        model="claude-3-5-sonnet-latest",
        anthropic_api_key="sk-ant-test-not-real",
    )


def test_anthropic_reroute_changes_base_url(chat_anthropic) -> None:
    mw = NoPIIMiddleware(base_url="https://proxy.example.com")
    new_model = mw._reroute(chat_anthropic)

    assert new_model.anthropic_api_url == "https://proxy.example.com"
    assert chat_anthropic.anthropic_api_url != new_model.anthropic_api_url


def test_anthropic_reroute_clears_cached_client(chat_anthropic) -> None:
    """Triggering the cached_property to rebuild against the new base URL."""
    # Force the original cached_property to populate
    _ = chat_anthropic._client
    assert "_client" in chat_anthropic.__dict__

    mw = NoPIIMiddleware(base_url="https://proxy.example.com")
    new_model = mw._reroute(chat_anthropic)

    # New model must NOT have the cached client carried over
    assert "_client" not in new_model.__dict__
    # And accessing it now should build against the new base URL
    assert str(new_model._client.base_url).startswith("https://proxy.example.com")


def test_anthropic_session_header_attached(chat_anthropic) -> None:
    mw = NoPIIMiddleware(session_id="sess-xyz")
    new_model = mw._reroute(chat_anthropic)

    headers = new_model.default_headers or {}
    assert headers.get(SESSION_HEADER) == "sess-xyz"


# ------ wrap_model_call wiring ------


def test_wrap_model_call_swaps_model_and_invokes_handler(chat_openai) -> None:
    mw = NoPIIMiddleware(base_url="https://proxy.example.com")

    captured = {}

    def handler(req):
        captured["model"] = req.model
        return "OK"

    request = SimpleNamespace(model=chat_openai)
    result = mw.wrap_model_call(request, handler)

    assert result == "OK"
    assert captured["model"] is request.model  # in-place swap
    assert captured["model"].openai_api_base == "https://proxy.example.com/v1"


@pytest.mark.asyncio
async def test_awrap_model_call_swaps_model_and_invokes_handler(chat_openai) -> None:
    mw = NoPIIMiddleware(base_url="https://proxy.example.com")

    captured = {}

    async def handler(req):
        captured["model"] = req.model
        return "OK-ASYNC"

    request = SimpleNamespace(model=chat_openai)
    result = await mw.awrap_model_call(request, handler)

    assert result == "OK-ASYNC"
    assert captured["model"].openai_api_base == "https://proxy.example.com/v1"
