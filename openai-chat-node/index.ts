/**
 * OpenAI Chat Completion with NoPII PII Protection (Node.js)
 *
 * Same concept as the Python example: change the baseURL, done.
 * PII in your prompts is automatically tokenized before reaching OpenAI,
 * and responses are detokenized before reaching your app.
 */

import OpenAI from "openai";
import "dotenv/config";

// The only change: point baseURL at NoPII
const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  baseURL: process.env.NOPII_BASE_URL || "https://api.nopii.co/v1",
});

async function main() {
  const response = await client.chat.completions.create({
    model: "gpt-4o",
    messages: [
      {
        role: "user",
        content:
          "Summarize the customer record for John Smith. " +
          "His SSN is 234-56-7891 and his email is john.smith@acme.com. " +
          "He called from 555-867-5309 about his credit card 4242-4242-4242-4242.",
      },
    ],
  });

  console.log(response.choices[0].message.content);
}

main();
