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



"""
How API pricing works
You are charged per token, not per request. A token is roughly 4 characters or ¾ of a word. There are two token types priced differently — input tokens are what you send to the model, output tokens are what the model sends back. Output costs more because the model generates each token individually.
Anthropic publishes prices per million tokens. For Claude Haiku (used today): input is $0.80 per million, output is $4.00 per million. To get price per single token you divide by 1,000,000.
In a prompt chain, the output of one step becomes the input of the next — meaning that text is billed twice. This compounds costs across multi-step chains.
The usage object
Every API response contains a usage block. You access it as:
pythonresponse.usage.input_tokens
response.usage.output_tokens
These are exact counts, not estimates. You use them to calculate real cost per call.
Calculating cost in code
Define pricing constants at the top of your script so they are easy to update if rates change:
pythonCOST_PER_MILLION_INPUT = 0.80
COST_PER_MILLION_OUTPUT = 4.00
Build a reusable function that takes token counts, calculates each cost, prints the breakdown, and returns the total:
pythondef calculate_cost(input_tokens, output_tokens):
    input_cost = input_tokens * (COST_PER_MILLION_INPUT / 1_000_000)
    output_cost = output_tokens * (COST_PER_MILLION_OUTPUT / 1_000_000)
    total_cost = input_cost + output_cost
    print(f"Input cost:  ${input_cost:.6f}")
    print(f"Output cost: ${output_cost:.6f}")
    print(f"Total cost:  ${total_cost:.6f}")
    return total_cost
:.6f inside an f-string means: display as a float with exactly 6 decimal places. This keeps small numbers readable instead of showing scientific notation.
Cumulative cost tracking
Initialise a session total at zero before any API calls. After each call, add that call's cost onto the running total using +=:
pythontotal_session_cost = 0
total_session_cost += calculate_cost(response.usage.input_tokens, response.usage.output_tokens)
Print the final total after all calls are complete.
Budget cap / cost guard
Define a spending limit as a variable. Before every API call, check whether the running total has already hit that limit. If it has, skip the call and print a warning. If it hasn't, proceed:
pythonbudget_cap = 0.003

if total_session_cost >= budget_cap:
    print("Budget cap reached!")
else:
    response = client.messages.create(...)
    total_session_cost += calculate_cost(...)
Use >= not > so the guard triggers exactly at the limit. The check must run before each individual call — not once at the end — so calls can actually be stopped in time.

"""