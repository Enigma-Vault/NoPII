"""
Anthropic Streaming with NoPII PII Protection

Streaming with Anthropic works seamlessly through NoPII.
Detokenization happens in real time as chunks arrive.

This example shows credential detection - NoPII catches API keys,
Slack tokens, and other secrets alongside traditional PII.
"""

import os

import anthropic
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

nopii_base = os.environ.get("NOPII_BASE_URL", "https://api.nopii.co")
client = anthropic.Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"],
    base_url=nopii_base,
)

with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": (
                "Review this config snippet for security issues: "
                "AWS key AKIAIOSFODNN7EXAMPLE, Stripe key sk_live_1234567890abcdefgh, "
                "Slack bot token xoxb-1234567890-abcdefghij. "
                "Deployed by Mike Torres (mike.t@startup.io, phone 415-555-0142) "
                "on 2024-03-15."
            ),
        }
    ],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

print()
