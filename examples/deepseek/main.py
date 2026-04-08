"""
DeepSeek with NoPII PII Protection

DeepSeek uses an OpenAI-compatible API, so NoPII works as a drop-in proxy.
Just change the base_url - NoPII detects the provider from your API key
and routes to DeepSeek automatically.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url=os.environ.get("NOPII_BASE_URL", "https://api.nopii.co"),
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {
            "role": "user",
            "content": (
                "Translate this customer note to formal English: "
                "Hey, so Mike Thompson called again about his account. "
                "His number is 408-555-0234 and email mike.t@startup.io. "
                "He says the payment from card 5105-1051-0510-5100 didn't go through."
            ),
        }
    ],
)

print(response.choices[0].message.content)
