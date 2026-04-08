"""
LiteLLM with NoPII PII Protection

LiteLLM provides a unified interface for calling 100+ LLM providers.
Same litellm.completion() call, same NoPII protection - just change the
model string and API key. No separate SDKs or client setup needed.

Compare with multi-provider/, which requires separate SDK imports and
different client patterns for each provider.
"""

import os

import litellm
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

NOPII_BASE_URL = os.environ.get("NOPII_BASE_URL", "https://api.nopii.co")

# Same PII-laden prompt, sent to multiple providers via litellm.completion()
PROMPT = (
    "Summarize the customer record for Sarah Chen. "
    "Her SSN is 456-78-9012 and her email is sarah.chen@example.com. "
    "She called from 312-555-0198 about her credit card 4111-1111-1111-1111."
)

# --- OpenAI via LiteLLM ---
print("=== OpenAI (GPT-4o) via LiteLLM ===\n")
response = litellm.completion(
    model="openai/gpt-4o",
    api_key=os.environ["OPENAI_API_KEY"],
    api_base=NOPII_BASE_URL,
    messages=[{"role": "user", "content": PROMPT}],
)
print(response.choices[0].message.content)

# --- Anthropic via LiteLLM (optional) ---
# Same function, different model string. LiteLLM handles the SDK differences.
anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
if anthropic_key and not anthropic_key.endswith("..."):
    print("\n=== Anthropic (Claude) via LiteLLM ===\n")
    response = litellm.completion(
        model="anthropic/claude-sonnet-4-20250514",
        api_key=os.environ["ANTHROPIC_API_KEY"],
        api_base=NOPII_BASE_URL,
        max_tokens=1024,
        messages=[{"role": "user", "content": PROMPT}],
    )
    print(response.choices[0].message.content)

print("\n--- Same function, same PII protection, any provider. ---")
