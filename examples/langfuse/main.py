"""
Langfuse + NoPII Distributed Tracing

NoPII has built-in Langfuse support. Enable it in the admin console
(app.nopii.co) and NoPII will send its own traces to Langfuse for every
proxied request — showing the sanitize, llm-call, and desanitize steps
between NoPII and the LLM provider. PII never appears in those traces;
only tokenized content is logged.

This example shows the client side: your application creates its own
Langfuse traces and connects them to NoPII's server-side traces using
the W3C traceparent header. The result is end-to-end visibility — from
your app through NoPII to the LLM — in a single Langfuse trace view.

Prerequisites:
  1. Enable Langfuse in the NoPII admin console (app.nopii.co)
  2. Set LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY in your .env
"""

import os
import uuid

from dotenv import load_dotenv
from langfuse import Langfuse, observe
from openai import OpenAI

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ.get("NOPII_BASE_URL", "https://api.nopii.co"),
)

langfuse = Langfuse(
    public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
    secret_key=os.environ["LANGFUSE_SECRET_KEY"],
    host=os.environ.get(
        "LANGFUSE_HOST", "https://us.cloud.langfuse.com"
    ),
)

PROMPT = (
    "Summarize the customer record for John Smith. "
    "His SSN is 234-56-7891 and his email is john.smith@acme.com. "
    "He called from 555-867-5309 about his credit card "
    "4242-4242-4242-4242."
)


@observe(as_type="generation")
def call_llm(prompt: str, traceparent: str) -> str:
    """Call OpenAI via NoPII with a traceparent header."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        extra_headers={"traceparent": traceparent},
    )
    langfuse.update_current_generation(
        model="gpt-4o",
        usage_details={
            "input": response.usage.prompt_tokens,
            "output": response.usage.completion_tokens,
        },
    )
    return response.choices[0].message.content


@observe()
def customer_lookup(prompt: str) -> str:
    """Application trace that links to NoPII's server-side trace."""
    # Build a W3C traceparent header to link NoPII's trace to yours
    trace_id = uuid.uuid4().hex
    span_id = uuid.uuid4().hex[:16]
    traceparent = f"00-{trace_id}-{span_id}-01"

    return call_llm(prompt, traceparent)


result = customer_lookup(PROMPT)
print(result)

langfuse.flush()
print("\nTrace sent to Langfuse — check your dashboard.")
