# FAQ

**Does NoPII add latency?**
Yes. PII detection and tokenization add overhead per request. The exact overhead depends on prompt length and PII density. Streaming is supported with per-chunk detokenization. For latency-sensitive applications, benchmark with your actual workload. See [Operational Notes](operations.md) for more detail.

**Do I need to change my application code?**
For most SDK-based integrations, you change the `base_url` in your client configuration. Your application logic, prompts, and response handling stay exactly the same.

**What if PII is not detected?**
NoPII's detection depends on the entity types you've enabled and the confidence thresholds you've configured. If a PII value doesn't match any enabled detector, it passes through unprotected. Review and tune your detection settings in the admin console, and test with representative data before going to production. See [Detection Catalog](detection.md) for edge cases.

**What happens with partial PII or edge cases?**
Detection is based on pattern matching and NLP models. Edge cases (e.g., PII split across message boundaries, PII embedded in code blocks, unusual name formats) may not be detected. Test your specific data patterns and adjust confidence thresholds as needed.

**Is my data stored?**
NoPII does not store request or response bodies. It logs PII detections (entity type, confidence score, timestamp) for audit purposes but does not log the original PII values. Tokenization mappings are managed by Enigma Vault's Data Vault. See [Security and Trust](security.md).

**Who controls the upstream LLM API keys?**
You do. You register your provider API keys in the NoPII admin console. NoPII uses them to forward sanitized requests on your behalf. You retain full ownership and can rotate or revoke keys at any time.

**What if I use multiple LLM providers?**
One NoPII account protects traffic to all supported providers. Configure your API keys in the admin console and point each client to the appropriate NoPII endpoint. PII tokens are consistent across providers within your account.

**What about prompt caching?**
LLM provider prompt caching (e.g., OpenAI's cached prompts) works with NoPII because the tokenized form of a prompt is deterministic. The same input produces the same tokenized prompt, so cache hits are preserved.

**Does NoPII work with function/tool calling?**
Yes. PII in tool call arguments and responses is tokenized and detokenized. The tool calling protocol is passed through transparently.

**Is there a free tier?**
Yes. 1M protected tokens per month at no cost. No credit card required.
