"""
Multi-Provider PII Protection with NoPII

One NoPII instance protects traffic to all LLM providers.
Same PII, same protection, regardless of which model you use.
NoPII detects the provider from your API key automatically.
"""

import os

import anthropic
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

NOPII_BASE_URL = os.environ.get("NOPII_BASE_URL", "https://api.nopii.co")

# The same PII-laden prompt, sent to multiple providers
PROMPT = (
    "Summarize this patient intake form: "
    "Patient Emma Wilson, DOB 07/22/1990, SSN 567-89-0123. "
    "Contact: emma.w@hospital.org, phone 206-555-0156. "
    "Emergency contact: James Wilson at 206-555-0199."
)

# --- OpenAI ---
print("=== OpenAI (GPT-4o) ===\n")
openai_client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=NOPII_BASE_URL,
)

response = openai_client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": PROMPT}],
)
print(response.choices[0].message.content)

# --- Anthropic ---
print("\n=== Anthropic (Claude) ===\n")
# Point the Anthropic client at NoPII
anthropic_client = anthropic.Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"],
    base_url=NOPII_BASE_URL,
)

message = anthropic_client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": PROMPT}],
)
print(message.content[0].text)

# --- DeepSeek (optional) ---
if os.environ.get("DEEPSEEK_API_KEY"):
    print("\n=== DeepSeek ===\n")
    deepseek_client = OpenAI(
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url=NOPII_BASE_URL,
    )

    response = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": PROMPT}],
    )
    print(response.choices[0].message.content)

print("\n--- Same PII, same protection, every provider. ---")
