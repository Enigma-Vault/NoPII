"""
LangGraph with NoPII PII Protection

LangGraph builds on LangChain's LLM layer, so the same base_url
approach carries over. PII is protected across every node in the graph —
including tool calls and inter-node messages — without any graph-level
changes.

This example: a two-node support triage graph that classifies then summarises.
"""

import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

# Single base_url change protects the entire graph
llm = ChatOpenAI(
    model="gpt-4o",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ.get("NOPII_BASE_URL", "https://api.nopii.co"),
)


class TicketState(TypedDict):
    ticket: str
    category: str
    summary: str


def classify(state: TicketState) -> TicketState:
    """Classify the ticket type. PII is tokenized before reaching the LLM."""
    response = llm.invoke(
        [
            SystemMessage(
                content=(
                    "Classify this support ticket in one word: "
                    "billing, technical, account, or other."
                )
            ),
            HumanMessage(content=state["ticket"]),
        ]
    )
    return {**state, "category": response.content.strip().lower()}


def summarise(state: TicketState) -> TicketState:
    """Summarise the ticket. Deterministic tokens keep entity refs consistent."""
    response = llm.invoke(
        [
            SystemMessage(
                content=(
                    f"You are a {state['category']} support specialist. "
                    "Provide a concise structured summary."
                )
            ),
            HumanMessage(content=state["ticket"]),
        ]
    )
    return {**state, "summary": response.content}


# Build the graph
graph = StateGraph(TicketState)
graph.add_node("classify", classify)
graph.add_node("summarise", summarise)
graph.set_entry_point("classify")
graph.add_edge("classify", "summarise")
graph.add_edge("summarise", END)
app = graph.compile()

# Run — the LLM never sees the real PII across either node
result = app.invoke(
    {
        "ticket": (
            "Customer Emily Rodriguez (e.rodriguez@acmecorp.com, SSN 567-89-0123) "
            "is disputing a charge of $2,400 on card 4242-4242-4242-4242. "
            "She called from 628-555-0199 and her account ID is ACC-44821."
        ),
        "category": "",
        "summary": "",
    }
)

print(f"Category: {result['category']}")
print(f"\nSummary:\n{result['summary']}")
