"""Integration test against a live NoPII proxy.

Run manually against your own NoPII deployment:
    OPENAI_API_KEY=sk-... \
    NOPII_BASE_URL=https://api.nopii.co \
        python examples/test_against_remote.py

This is NOT a pytest test - it makes real network calls and costs real OpenAI
tokens. Kept outside tests/ so it does not run in CI by default.
"""

from __future__ import annotations

import os
import sys
import uuid
from urllib.parse import urlparse

from langchain_openai import ChatOpenAI

from langchain_nopii_middleware import NoPIIMiddleware


def assert_routed_through_proxy(model: object, expected_host: str) -> None:
    base_url = str(model.root_client.base_url)  # type: ignore[attr-defined]
    if expected_host not in base_url:
        raise AssertionError(
            f"Model base_url is {base_url!r}, expected to contain {expected_host!r}"
        )
    print(f"  base_url confirmed: {base_url}")


def run_direct_reroute(base_url: str, api_key: str, session_id: str) -> None:
    print("\n[1] Direct _reroute - bypassing the agent loop")
    model = ChatOpenAI(model="gpt-4o-mini", api_key=api_key, temperature=0)
    mw = NoPIIMiddleware(base_url=base_url, session_id=session_id)
    rerouted = mw._reroute(model)

    expected_host = urlparse(base_url).hostname or ""
    assert_routed_through_proxy(rerouted, expected_host)

    prompt = (
        "Reply with a one-sentence confirmation that you received this message. "
        "The user's name is Jane Smith, her email is jane.smith@example.com, "
        "and her phone is 415-555-0142."
    )
    response = rerouted.invoke(prompt)
    print(f"  response: {response.content[:200]}")
    if not response.content:
        raise AssertionError("Empty response from proxied model")


def run_through_agent(base_url: str, api_key: str, session_id: str) -> None:
    print("\n[2] Full agent path - wrap_model_call invoked by create_agent")

    try:
        from langchain.agents import create_agent
    except ImportError as exc:
        print(f"  SKIPPED - {exc}")
        return

    model = ChatOpenAI(model="gpt-4o-mini", api_key=api_key, temperature=0)
    agent = create_agent(
        model=model,
        tools=[],
        middleware=[NoPIIMiddleware(base_url=base_url, session_id=session_id)],
    )

    prompt = (
        "Acknowledge the contact details for Bob Johnson "
        "(bob.j@acme.co, 212-555-9988) in one sentence."
    )
    result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
    last = result["messages"][-1]
    text = getattr(last, "content", None) or str(last)
    print(f"  response: {text[:200]}")
    if not text:
        raise AssertionError("Empty response from agent")


def main() -> int:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: set OPENAI_API_KEY", file=sys.stderr)
        return 2

    base_url = os.environ.get("NOPII_BASE_URL", "https://api.nopii.co")
    session_id = os.environ.get("NOPII_SESSION_ID", f"langchain-mw-test-{uuid.uuid4()}")

    print(f"NoPII base_url: {base_url}")
    print(f"session_id:     {session_id}")

    run_direct_reroute(base_url, api_key, session_id)
    run_through_agent(base_url, api_key, session_id)

    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
