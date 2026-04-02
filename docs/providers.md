# Provider Compatibility

Any LLM provider that exposes an OpenAI-compatible API works with NoPII via `base_url`. NoPII detects the provider from your API key and routes automatically.

## Supported providers

| Provider | Integration | Endpoint |
|----------|-------------|----------|
| OpenAI | `base_url="https://api.nopii.co/v1"` | OpenAI-compatible |
| Anthropic | `base_url="https://api.nopii.co"` | Native Anthropic Messages API |
| DeepSeek | `base_url="https://api.nopii.co/v1"` | OpenAI-compatible |
| Google Gemini | `base_url="https://api.nopii.co/v1"` | OpenAI-compatible |
| xAI (Grok) | `base_url="https://api.nopii.co/v1"` | OpenAI-compatible |
| Mistral | `base_url="https://api.nopii.co/v1"` | OpenAI-compatible |
| Groq | `base_url="https://api.nopii.co/v1"` | OpenAI-compatible |
| Together | `base_url="https://api.nopii.co/v1"` | OpenAI-compatible |
| Fireworks | `base_url="https://api.nopii.co/v1"` | OpenAI-compatible |

## Anthropic note

Anthropic's SDK appends `/v1/` internally, so use the base domain without the `/v1` suffix. See the [anthropic-chat](../anthropic-chat) example.

```python
nopii_base = os.environ.get("NOPII_BASE_URL", "https://api.nopii.co/v1")
client = anthropic.Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"],
    base_url=nopii_base.removesuffix("/v1"),
)
```
