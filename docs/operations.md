# Operational Notes

## Latency

NoPII adds processing overhead for PII detection and tokenization/detokenization on each request and response. The overhead scales with the amount of text processed and the density of PII entities detected. Benchmark with your actual workload before deploying to latency-sensitive paths.

Streaming is fully supported. Detokenization happens per-chunk with no buffering.

<!-- TODO: Add specific p50/p95 latency benchmarks once measured -->

## Availability

NoPII operates as a proxy between your application and your LLM provider. If NoPII is unavailable, requests will not reach the LLM provider. Plan for this dependency in your architecture the same way you would plan for the LLM provider itself being unavailable.

## Failure modes

| Scenario | Behavior |
|----------|----------|
| NoPII is unreachable | Request fails (connection error from your SDK) |
| PII detection fails | Request is **blocked**. PII never leaks |
| LLM provider is down | Error is passed through from the provider |
| Detokenization fails | Response is returned with vault tokens visible (no PII exposure) |
| Unrecognized PII | Not tokenized. Detection depends on configured entity types and confidence thresholds |

## Rate limits

NoPII enforces its own rate limits independently of your LLM provider's limits. Limits are plan-dependent. Check your plan's limits in the admin console at [app.nopii.co](https://app.nopii.co).
