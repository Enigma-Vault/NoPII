"""
Multi-Turn Conversation with NoPII

Demonstrates deterministic tokenization across conversation turns.
The same PII value always maps to the same token, so the LLM maintains
context about entities across turns without ever seeing real data.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ.get("NOPII_BASE_URL", "https://api.nopii.co"),
)

conversation = []


def chat(user_message: str) -> str:
    """Send a message and get a response, maintaining conversation history."""
    conversation.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=conversation,
    )

    assistant_message = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": assistant_message})
    return assistant_message


# Turn 1: Introduce PII
print("--- Turn 1 ---")
print("User: Schedule a meeting with John Smith at john.smith@acme.com")
reply = chat(
    "Schedule a meeting with John Smith at john.smith@acme.com for next Tuesday."
)
print(f"Assistant: {reply}\n")

# Turn 2: Reference the same person without repeating PII
print("--- Turn 2 ---")
print("User: What email did I give you for John?")
reply = chat("What email did I give you for John?")
print(f"Assistant: {reply}\n")

# Turn 3: Add more people
print("--- Turn 3 ---")
print("User: Also invite Sarah Lee (sarah@acme.com)")
reply = chat("Also invite Sarah Lee at sarah@acme.com to the same meeting.")
print(f"Assistant: {reply}\n")

# Turn 4: Reference both people
print("--- Turn 4 ---")
print("User: Send both of them a reminder")
reply = chat("Send both John and Sarah a reminder about the meeting.")
print(f"Assistant: {reply}")
