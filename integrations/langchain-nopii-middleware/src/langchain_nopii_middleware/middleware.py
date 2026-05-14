"""NoPIIMiddleware - route LangChain model calls through the NoPII proxy."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from langchain.agents.middleware import AgentMiddleware

if TYPE_CHECKING:
    from langchain.agents.middleware.types import ModelRequest, ModelResponse

DEFAULT_NOPII_BASE_URL = "https://api.nopii.co"

SESSION_HEADER = "X-NoPII-Session-Id"


class UnsupportedModelError(TypeError):
    """Raised when the middleware does not know how to rebind a model's API base URL."""


class NoPIIMiddleware(AgentMiddleware):
    """Route an agent's model calls through the NoPII tokenization proxy.

    NoPII detects PII in outbound prompts, replaces it with deterministic tokens
    before the request reaches the LLM, and restores the original values in the
    response. The middleware works by rebinding the model's API base URL to the
    NoPII proxy at the point of each model call; the underlying SDK still does
    the HTTP work and the caller's existing API key is forwarded to NoPII for
    tenant identification.

    Supported model classes (v0.1):
        - ``langchain_openai.ChatOpenAI``
        - ``langchain_anthropic.ChatAnthropic``

    Example:
        >>> from langchain.agents import create_agent
        >>> from langchain_openai import ChatOpenAI
        >>> from langchain_nopii_middleware import NoPIIMiddleware
        >>>
        >>> agent = create_agent(
        ...     model=ChatOpenAI(model="gpt-4.1"),
        ...     tools=[...],
        ...     middleware=[NoPIIMiddleware()],
        ... )
    """

    def __init__(
        self,
        base_url: str = DEFAULT_NOPII_BASE_URL,
        session_id: str | None = None,
    ) -> None:
        """Configure the middleware.

        Args:
            base_url: Root URL of the NoPII proxy. Defaults to the public
                production endpoint. Override for self-hosted or test environments.
            session_id: Optional NoPII session identifier. When set, all model
                calls made through this middleware instance share a single
                tokenization session, which is what enables consistent
                token-to-plaintext restoration across multi-turn conversations.
                When omitted, NoPII issues a new session per HTTP request.
        """
        super().__init__()
        self.base_url = base_url.rstrip("/")
        self.session_id = session_id

    def wrap_model_call(
        self,
        request: ModelRequest[Any],
        handler: Callable[[ModelRequest[Any]], ModelResponse[Any]],
    ) -> ModelResponse[Any]:
        request.model = self._reroute(request.model)
        return handler(request)

    async def awrap_model_call(
        self,
        request: ModelRequest[Any],
        handler: Callable[[ModelRequest[Any]], Any],
    ) -> Any:
        request.model = self._reroute(request.model)
        return await handler(request)

    def _reroute(self, model: Any) -> Any:
        class_name = type(model).__name__
        if class_name in {"ChatOpenAI", "AzureChatOpenAI"}:
            return self._reroute_openai(model)
        if class_name == "ChatAnthropic":
            return self._reroute_anthropic(model)
        raise UnsupportedModelError(
            f"NoPIIMiddleware does not yet support model class {class_name!r}. "
            "Supported: ChatOpenAI, ChatAnthropic."
        )

    def _reroute_openai(self, model: Any) -> Any:
        """Rebuild ChatOpenAI's SDK clients pointed at the NoPII proxy.

        Why: ChatOpenAI caches the openai SDK client inside validate_environment
        and does not re-validate on attribute assignment, so a plain model_copy
        with an updated openai_api_base would leave the cached client pointing
        at the original URL.
        """
        new_model = model.model_copy()
        new_model.openai_api_base = f"{self.base_url}/v1"
        new_model.root_client = None
        new_model.root_async_client = None
        new_model.client = None
        new_model.async_client = None
        if self.session_id:
            extra_headers = dict(getattr(new_model, "default_headers", None) or {})
            extra_headers[SESSION_HEADER] = self.session_id
            new_model.default_headers = extra_headers
        new_model.validate_environment()
        return new_model

    def _reroute_anthropic(self, model: Any) -> Any:
        """Update ChatAnthropic's base URL.

        ChatAnthropic builds its SDK client lazily via @cached_property, so
        clearing the cached attribute on a copy is sufficient to force a
        rebuild on next access.
        """
        new_model = model.model_copy()
        new_model.anthropic_api_url = self.base_url
        if self.session_id:
            extra_headers = dict(getattr(new_model, "default_headers", None) or {})
            extra_headers[SESSION_HEADER] = self.session_id
            new_model.default_headers = extra_headers
        for cached in ("_client", "_async_client", "_client_params"):
            new_model.__dict__.pop(cached, None)
        return new_model
