import anthropic
from dotenv import load_dotenv
import os

load_dotenv("env",override=True)

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

customer_question = input("customer question")
response = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1024,
    system="You are a helpful assistant for Luigi's Pizzeria in Dublin. Answer customer questions politely and concisely.",
    messages=[
        {"role": "user", "content": f"{customer_question}"}
    ]
)

budget_cap = 0.001
COST_PER_MILLION_INPUT = 0.80
COST_PER_MILLION_OUTPUT = 4.00


def calculate_cost(input_tokens, output_tokens):
    input_cost = input_tokens * (COST_PER_MILLION_INPUT / 1_000_000)
    output_cost = output_tokens * (COST_PER_MILLION_OUTPUT / 1_000_000)
    total_cost = input_cost + output_cost
    print(f"Input cost:  ${input_cost:.6f}")
    print(f"Output cost: ${output_cost:.6f}")
    print(f"Total cost:  ${total_cost:.6f}")
    return total_cost


total_session_cost = 0

if total_session_cost >= budget_cap:
    print("Budget cap reached!")
else:
    response1 = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=200,
    system="You are a helpful assistant for Luigi's Pizzeria in Dublin.",
    messages=[
        {"role": "user", "content": "what time do you open"}
    ]
)
    total_session_cost += calculate_cost(response1.usage.input_tokens, response1.usage.output_tokens)

if total_session_cost >= budget_cap:
    print("Budget cap reached!")
else:
    response2 = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=200,
    system="You are a helpful assistant for Luigi's Pizzeria in Dublin.",
    messages=[
        {"role": "user", "content": "does luigis do collection?"}
    ]
)
    total_session_cost += calculate_cost(response2.usage.input_tokens, response2.usage.output_tokens)


if total_session_cost >= budget_cap:
    print("Budget cap reached!")
else:
    response3 = client.messages.create(

    model="claude-3-haiku-20240307",
    max_tokens=200,
    system="You are a helpful assistant for Luigi's Pizzeria in Dublin.",
    messages=[
        {"role": "user", "content": "what is the main dish of luigis"}
    ]
)
    total_session_cost += calculate_cost(response3.usage.input_tokens, response3.usage.output_tokens)
print(f"\nTotal session cost: ${total_session_cost:.6f}")

