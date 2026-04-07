#AI EMAIL RESPONDER


import anthropic
import os
import dotenv


dotenv.load_dotenv("env")

incoming_email = "Hi, I ordered a Margherita pizza last night and it arrived cold and 45 minutes late. I'm really disappointed. Can you tell me what you're going to do about this?"

system_prompt = "You are a customer service assistant for Luigi's Pizzeria, a family-run Italian restaurant in Dublin. When you receive a customer email, reply professionally and warmly. Always acknowledge the customer's experience first, apologise sincerely, and offer a concrete resolution. Keep replies under 150 words. Never make promises about refunds without saying a manager will confirm."

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    system=system_prompt,
    messages=[
        {"role": "user", "content": incoming_email}
    ]
)
draft_reply = response.content[0].text

COST_PER_MILLION_INPUT_TOKENS = 0.80
COST_PER_MILLION_OUTPUT_TOKENS = 4.00


def calculate_cost(input_tokens, output_tokens):
    input_cost = input_tokens * (COST_PER_MILLION_INPUT_TOKENS / 1_000_000)
    output_cost = output_tokens * (COST_PER_MILLION_OUTPUT_TOKENS / 1_000_000)
    total_cost = input_cost + output_cost
    print(f"Input cost:  ${input_cost:.6f}")
    print(f"Output cost: ${output_cost:.6f}")
    print(f"Total cost:  ${total_cost:.6f}")
    return total_cost


print("--- DRAFT REPLY ---")
print(draft_reply)
print("--- END ---")

total_cost = calculate_cost(response.usage.input_tokens, response.usage.output_tokens)
print(f"Total cost of this email response: ${total_cost:.6f}")