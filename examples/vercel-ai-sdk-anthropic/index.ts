/**
 * Vercel AI SDK + Anthropic with NoPII PII Protection
 *
 * Anthropic has one inference API (Messages), so there's no Responses-vs-Chat
 * split — `createAnthropic` always targets `/messages` under whatever
 * baseURL you provide.
 *
 * Note the `/v1` suffix on `baseURL`. `@ai-sdk/anthropic` bakes `/v1` into
 * its default (`https://api.anthropic.com/v1`) and does not re-add it when
 * you override baseURL, so without `/v1` the SDK posts to `/messages` and
 * NoPII returns 404. The bare Anthropic Python SDK adds `/v1` for you;
 * this one does not.
 */

import { createAnthropic } from "@ai-sdk/anthropic";
import { generateText } from "ai";
import "dotenv/config";

const nopiiBase = process.env.NOPII_BASE_URL || "https://api.nopii.co";

const anthropic = createAnthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
  baseURL: `${nopiiBase}/v1`,
});

async function main() {
  const { text } = await generateText({
    model: anthropic("claude-sonnet-4-20250514"),
    prompt:
      "Draft a follow-up note for patient Maria Garcia (DOB: 03/15/1985). " +
      "Her SSN is 321-54-9876 and her email is maria.garcia@gmail.com. " +
      "She visited on 2024-01-15 for a routine checkup.",
  });

  console.log(text);
}

main();
