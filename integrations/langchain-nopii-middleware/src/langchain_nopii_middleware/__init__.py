"""LangChain middleware that routes model calls through the NoPII proxy."""

from langchain_nopii_middleware.middleware import (
    DEFAULT_NOPII_BASE_URL,
    NoPIIMiddleware,
    UnsupportedModelError,
)

__all__ = [
    "DEFAULT_NOPII_BASE_URL",
    "NoPIIMiddleware",
    "UnsupportedModelError",
]

__version__ = "0.1.0"
