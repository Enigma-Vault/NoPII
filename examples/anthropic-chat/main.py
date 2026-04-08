"""
Anthropic Chat with NoPII PII Protection

NoPII supports Anthropic's Messages API natively. Same idea: swap the base_url,
and PII is automatically protected.
"""

import os

import anthropic
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

# Point the Anthropic client at NoPII
nopii_base = os.environ.get("NOPII_BASE_URL", "https://api.nopii.co")
client = anthropic.Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"],
    base_url=nopii_base,
)

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": (
                "Draft a follow-up note for patient Maria Garcia (DOB: 03/15/1985). "
                "Her SSN is 321-54-9876 and her email is maria.garcia@gmail.com. "
                "She visited on 2024-01-15 for a routine checkup."
            ),
        }
    ],
)

print(message.content[0].text)
