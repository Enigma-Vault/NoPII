# Provider Compatibility

Any LLM provider that exposes an OpenAI-compatible API works with NoPII via `base_url`. NoPII detects the provider from your API key and routes automatically.

## Supported providers

| Provider | Integration | Endpoint |
|----------|-------------|----------|
| OpenAI | `base_url="https://api.nopii.co"` | OpenAI-compatible |
| Anthropic | `base_url="https://api.nopii.co"` | Native Anthropic Messages API |
| DeepSeek | `base_url="https://api.nopii.co"` | OpenAI-compatible |
| Google Gemini | `base_url="https://api.nopii.co"` | OpenAI-compatible |
| xAI (Grok) | `base_url="https://api.nopii.co"` | OpenAI-compatible |
| Mistral | `base_url="https://api.nopii.co"` | OpenAI-compatible |
| Groq | `base_url="https://api.nopii.co"` | OpenAI-compatible |
| Together | `base_url="https://api.nopii.co"` | OpenAI-compatible |
| Fireworks | `base_url="https://api.nopii.co"` | OpenAI-compatible |

## Anthropic note

Anthropic's SDK works with the same base URL. See the [anthropic-chat](../examples/anthropic-chat) example.

```python
nopii_base = os.environ.get("NOPII_BASE_URL", "https://api.nopii.co")
client = anthropic.Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"],
    base_url=nopii_base,
)
```
