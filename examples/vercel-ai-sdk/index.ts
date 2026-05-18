/**
 * Vercel AI SDK with NoPII PII Protection
 *
 * Same idea as the bare-OpenAI example: point the provider at NoPII.
 * The Vercel AI SDK exposes a `createOpenAI` factory for exactly this —
 * configure the base URL once and every model created from the provider
 * routes through NoPII. PII in prompts is tokenized before the request
 * reaches OpenAI, and the response is detokenized before it reaches your app.
 *
 * Use `openai.chat(...)` rather than `openai(...)`: the default `openai(...)`
 * factory targets OpenAI's Responses API (`/responses`), which NoPII does
 * not proxy. `openai.chat(...)` targets `/chat/completions`, which it does.
 */

import { createOpenAI } from "@ai-sdk/openai";
import { generateText } from "ai";
import "dotenv/config";

const openai = createOpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  baseURL: process.env.NOPII_BASE_URL || "https://api.nopii.co",
});

async function main() {
  const { text } = await generateText({
    model: openai.chat("gpt-4o"),
    prompt:
      "Summarize the customer record for John Smith. " +
      "His SSN is 234-56-7891 and his email is john.smith@acme.com. " +
      "He called from 555-867-5309 about his credit card 4242-4242-4242-4242.",
  });

  console.log(text);
}

main();
