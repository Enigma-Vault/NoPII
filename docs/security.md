# Security and Trust

## Where do tokens live?

Tokenization is handled by [Enigma Vault](https://www.enigmavault.io)'s Data Vault platform. PII values are replaced with vault tokens (`VAULT_...`) that are opaque references. They cannot be reversed without access to the vault. The vault is the single source of truth for the PII-to-token mapping.

## Is raw PII stored?

NoPII itself does not store raw PII values. The proxy is stateless with respect to PII content. It tokenizes on the way in, detokenizes on the way out, and does not persist request or response bodies. PII-to-token mappings are managed by the underlying Data Vault.

## What gets logged?

NoPII logs PII **detections** for audit purposes: entity type, confidence score, timestamp, and the token that was substituted. The original PII values are not included in logs. This gives you an audit trail of what was protected without creating a secondary store of sensitive data.

## Deterministic token scope

Deterministic tokenization is scoped to your account. The same PII value produces the same token consistently within your account, which is what enables multi-turn coherence. Different accounts produce different tokens for the same input. There is no cross-tenant token collision.

## Tenant isolation

Each NoPII account operates with its own tokenization context. API keys, detection configurations, vault mappings, and audit logs are isolated per tenant. There is no shared state between accounts.

## API key flow

You register your upstream LLM provider API keys (OpenAI, Anthropic, etc.) in the NoPII admin console. NoPII uses those keys to forward sanitized requests to the provider on your behalf. Your application authenticates to NoPII using the same API key. NoPII identifies the provider from the key format and routes accordingly. You retain full ownership and control of your provider API keys.

## Certifications

Enigma Vault holds the following certifications and partnerships:

- **PCI DSS Level 1** certified. The highest level of payment card industry compliance, validated by an independent Qualified Security Assessor.
- **SOC 2 Type II** audited. Independent verification of controls for security, availability, and confidentiality over a sustained audit period.
- **AWS Partner**. Infrastructure runs on AWS with access to partner-tier support, security reviews, and architectural guidance.

## Compliance

NoPII is designed to reduce PII exposure to third-party LLM providers, which supports compliance with GDPR, HIPAA, CCPA, and similar regulations. NoPII is not a compliance product by itself. It is a technical control that reduces the surface area of PII exposure in your LLM pipeline.

> For detailed security documentation, see [docs.nopii.co](https://docs.nopii.co).
