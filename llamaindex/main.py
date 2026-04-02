"""
LlamaIndex with NoPII PII Protection

LlamaIndex's OpenAI LLM accepts api_base, making NoPII a drop-in proxy.
All LlamaIndex abstractions (query engines, agents, etc.) work unchanged.
"""

import os

from dotenv import load_dotenv
from llama_index.core.llms import ChatMessage
from llama_index.llms.openai import OpenAI

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# Point LlamaIndex at NoPII
llm = OpenAI(
    model="gpt-4o",
    api_key=os.environ["OPENAI_API_KEY"],
    api_base=os.environ.get("NOPII_BASE_URL", "https://api.nopii.co/v1"),
)

# Chat with PII - automatically protected
response = llm.chat(
    [
        ChatMessage(
            role="user",
            content=(
                "Analyze this employee record: "
                "Name: David Park, Email: d.park@megacorp.io, "
                "SSN: 345-67-8901, Phone: 628-555-0173. "
                "He's in the engineering department, started January 2024. "
                "Summarize the key details."
            ),
        )
    ]
)

print(response.message.content)
