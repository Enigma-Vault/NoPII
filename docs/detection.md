# PII Detection Catalog

NoPII detects 38+ PII entity types across multiple categories. Each entity type is individually configurable in the [admin console](https://app.nopii.co). You can enable or disable types, adjust confidence thresholds, and preview detection on sample text.

## Categories

### Global
Person names, locations, phone numbers, emails, credit cards, IBANs, crypto wallets, dates/times, IP addresses, MAC addresses, nationality/religion/political affiliations, medical licenses, URLs

### USA
SSNs, bank accounts, driver's licenses, ITINs, Medicare IDs, passports

### UK
NHS numbers, National Insurance numbers

### Europe
Spanish and Italian national ID formats

### Security
API keys, secrets, database connection strings, tokens

### Other
PANs, NRC/FIN, ISN, ACN, TFN, Aadhaar, PESEL, Personal IDs, and more

## Edge cases

Detection is based on pattern matching and NLP models. Be aware of these limitations:

- **PII split across message boundaries.** If a PII value spans two messages or is split across chunks in an unusual way, it may not be detected as a single entity.
- **PII embedded in code blocks.** Code-like strings may or may not trigger detection depending on format.
- **Unusual name formats.** Names from underrepresented locales or non-standard formats may have lower detection confidence.
- **Ambiguous values.** Short numbers or common words that happen to match PII patterns may produce false positives.

Test with representative data from your application and tune confidence thresholds before going to production.
