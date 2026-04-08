"""
OpenAI Streaming with NoPII PII Protection

Streaming works exactly like normal - NoPII handles detokenization
of streamed chunks in real time. No buffering, no delays.

This example shows credential detection - NoPII catches API keys,
database connection strings, and tokens that developers commonly
paste into LLM prompts.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ.get("NOPII_BASE_URL", "https://api.nopii.co"),
)

stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": (
                "Help me debug this deployment. Our app connects to "
                "postgresql://admin:s3cret@db.internal:5432/prod "
                "and calls OpenAI with key sk-proj-ABC123def456ghi789jkl012mno. "
                "Sarah Chen (sarah.chen@company.com) reported it failing "
                "after the deploy on 2024-03-20."
            ),
        }
    ],
    stream=True,
)

for chunk in stream:
    if chunk.choices and chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="", flush=True)

print()  # newline after stream completes
