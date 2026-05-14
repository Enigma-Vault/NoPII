# langchain-nopii-middleware

LangChain agent middleware that routes model calls through the [NoPII](https://www.nopii.co) tokenization proxy. Adds PII detection and tokenization to any LangChain agent in a single line, without changing how the model is constructed and without an SDK.

## What it does

NoPII detects PII in outbound prompts, replaces it with deterministic tokens before the request reaches the LLM, and restores the original values in the response. The middleware sits inside the agent's model-call path and rebinds the model's API base URL to NoPII's proxy, so the underlying OpenAI/Anthropic SDK still handles the HTTP call. Your existing API key is forwarded to NoPII for tenant identification.

- **Drop-in**: one middleware, no SDK
- **Deterministic tokenization**: same plaintext → same token, so the model can reason consistently across multi-turn conversations
- **Fail-safe**: requests are blocked if tokenization fails; PII never leaks
- **Full audit trail** of every entity detected and tokenized

## Installation

```bash
pip install langchain-nopii-middleware
```

Install with provider extras for the model you use:

```bash
pip install "langchain-nopii-middleware[openai]"
pip install "langchain-nopii-middleware[anthropic]"
```

## Quick start

```python
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from langchain_nopii_middleware import NoPIIMiddleware

agent = create_agent(
    model=ChatOpenAI(model="gpt-4.1"),
    tools=[...],
    middleware=[NoPIIMiddleware()],
)

result = agent.invoke({
    "messages": [
        {"role": "user", "content": "Email john.doe@example.com a meeting summary."}
    ]
})
```

The proxy receives the prompt with PII tokenized (e.g. `<EMAIL_a3f2>` in place of the address), forwards the tokenized prompt to OpenAI, and restores the original email in the response before it reaches the agent.

## Configuration

```python
NoPIIMiddleware(
    base_url="https://api.nopii.co",  # default; override for self-hosted or test environments
    session_id="user-42-thread-7",    # optional; pin a session for multi-turn token continuity
)
```

### Session continuity

By default each model call gets a fresh tokenization session from the proxy. For multi-turn agents where the same PII should map to the same token across calls, pass an explicit `session_id`:

```python
agent = create_agent(
    model=ChatAnthropic(model="claude-3-5-sonnet-latest"),
    tools=[...],
    middleware=[NoPIIMiddleware(session_id=conversation_id)],
)
```

Tokenization is deterministic at the proxy level regardless of session, but `session_id` is what lets the proxy detokenize tokens it issued on earlier turns when they appear in the model's response.

## Supported models

| Model class | Provider extra |
|---|---|
| `langchain_openai.ChatOpenAI` | `[openai]` |
| `langchain_openai.AzureChatOpenAI` | `[openai]` |
| `langchain_anthropic.ChatAnthropic` | `[anthropic]` |

Other LangChain chat models can be added on request. See [docs.nopii.co/integrations](https://docs.nopii.co/integrations) for the full list of LLM providers the underlying NoPII proxy supports.

## How it works

1. The agent calls `model.invoke(...)` (or `ainvoke`) as normal.
2. `NoPIIMiddleware.wrap_model_call` intercepts the call and produces a copy of the model whose API base URL points at the NoPII proxy.
3. The model's own SDK (`openai` or `anthropic`) sends the HTTP request — but to NoPII instead of the LLM provider.
4. NoPII detects PII, tokenizes it, forwards the tokenized request to the LLM, then restores PII in the response before returning it.
5. The agent receives the response with original PII intact.

The middleware does not introduce a second HTTP hop and does not buffer responses; streaming works.

## Authentication

NoPII identifies tenants by hashing the LLM API key on the incoming request. Provide your real OpenAI/Anthropic key to the LangChain model exactly as you would without NoPII, and NoPII will resolve it to your tenant configuration. No separate NoPII API key is required for the proxy path.

For account setup and key registration, see [docs.nopii.co/quickstart](https://docs.nopii.co/quickstart).

## License

Apache 2.0
