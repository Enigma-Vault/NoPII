"""
LangChain + Anthropic with NoPII PII Protection

ChatAnthropic accepts an anthropic_api_url parameter, so the same
pattern as the raw Anthropic SDK applies: point at NoPII. All chains,
agents, and tools work exactly as before.
"""

import os

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

nopii_base = os.environ.get("NOPII_BASE_URL", "https://api.nopii.co")

llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    api_key=os.environ["ANTHROPIC_API_KEY"],
    anthropic_api_url=nopii_base,
)

# Simple invocation — PII is intercepted and tokenized automatically
response = llm.invoke(
    [
        HumanMessage(
            content=(
                "Summarise this support ticket: "
                "Customer Sarah Chen (s.chen@finco.com, SSN 123-45-6789) "
                "reports a billing discrepancy on card 4111-1111-1111-1111. "
                "She called from 415-555-0182. Please extract the key fields."
            )
        )
    ]
)

print(response.content)
print("\n--- With a chain ---\n")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a concise customer service assistant."),
        ("human", "{input}"),
    ]
)

chain = prompt | llm

response = chain.invoke(
    {
        "input": (
            "Review the account for Marcus Webb at m.webb@enterprise.io. "
            "His employee ID is EMP-998821 and phone is 312-555-0144."
        )
    }
)

print(response.content)
