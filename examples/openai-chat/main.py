"""
OpenAI Chat Completion with NoPII PII Protection

Demonstrates the simplest possible NoPII integration: change base_url, done.
PII in your prompts is automatically tokenized before reaching OpenAI,
and responses are detokenized before reaching your app.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

# The only change: point base_url at NoPII
client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ.get("NOPII_BASE_URL", "https://api.nopii.co"),
)

# Send a message containing PII - NoPII intercepts and tokenizes it
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": (
                "Summarize the customer record for John Smith. "
                "His SSN is 234-56-7891 and his email is john.smith@acme.com. "
                "He called from 555-867-5309 about his credit card 4242-4242-4242-4242."
            ),
        }
    ],
)

# The response contains real PII - NoPII detokenized it on the way back
print(response.choices[0].message.content)
