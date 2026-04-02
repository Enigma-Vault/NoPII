"""
LangChain with NoPII PII Protection

LangChain's ChatOpenAI accepts a base_url parameter, making NoPII integration
a single-line change. All chains, agents, and tools work exactly as before.
"""

import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# Point LangChain at NoPII - everything else stays the same
llm = ChatOpenAI(
    model="gpt-4o",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ.get("NOPII_BASE_URL", "https://api.nopii.co/v1"),
)

# Simple invocation with PII
response = llm.invoke(
    [
        HumanMessage(
            content=(
                "Extract the key details from this support ticket: "
                "Customer Alice Johnson (alice.j@techcorp.com, SSN 234-56-7890) "
                "is reporting unauthorized charges on card 4111-1111-1111-1111. "
                "Please respond with a structured summary."
            )
        )
    ]
)

print(response.content)
print("\n--- With a chain ---\n")

from langchain_core.prompts import ChatPromptTemplate  # noqa: E402

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful customer service agent. Be concise."),
        ("human", "{input}"),
    ]
)

chain = prompt | llm

response = chain.invoke(
    {
        "input": (
            "Look up the account for Bob Williams at bob.w@example.com. "
            "His SSN is 876-54-3210 and phone is 312-555-0199."
        )
    }
)

print(response.content)
