"""
Google Gemini with NoPII PII Protection

Gemini's OpenAI-compatible endpoint works with NoPII out of the box.
NoPII detects the provider from your API key and routes to Gemini automatically.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url=os.environ.get("NOPII_BASE_URL", "https://api.nopii.co/v1"),
)

response = client.chat.completions.create(
    model="gemini-2.0-flash",
    messages=[
        {
            "role": "user",
            "content": (
                "Summarize this insurance claim: "
                "Policyholder Lisa Wang (lisa.wang@email.com, SSN 456-78-9012) "
                "filed a claim on 2024-02-20. She can be reached at 503-555-0187. "
                "The claim is for water damage at "
                "742 Evergreen Terrace, Portland, OR 97201."
            ),
        }
    ],
)

print(response.choices[0].message.content)
