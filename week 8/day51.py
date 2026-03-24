import anthropic
from dotenv import load_dotenv
import os

load_dotenv(override=True)

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
print("\nLuigi's Pizzeria Assistant:")
print(response.content[0].text)
print("\n--- Response Metadata ---")
print("Model used:", response.model)
print("Input tokens:", response.usage.input_tokens)
print("Output tokens:", response.usage.output_tokens)
print("Stop reason:", response.stop_reason)


"""
FULL NOTES — DAY 51
The Anthropic SDK
A Python library for calling Claude via API. Installed with py -m pip install anthropic. Gives you clean Python functions instead of raw HTTP requests.
How the call is structured

anthropic.Anthropic(api_key=...) — creates the client
client.messages.create() — sends the request
Required parameters: model, max_tokens, messages
System prompt goes in a separate system= parameter — not inside the messages list

How it differs from OpenAI

OpenAI: client.chat.completions.create(), system prompt inside messages list, response at response.choices[0].message.content
Claude: client.messages.create(), system prompt as separate parameter, response at response.content[0].text

Dynamic handler
Use input() to capture a customer question, pass it into the messages list using an f-string. Every question gets a fresh response.
Response object

response.content[0].text — the actual reply
response.model — which model was used
response.usage.input_tokens — tokens sent
response.usage.output_tokens — tokens returned
response.stop_reason — why Claude stopped (end_turn = completed normally)

Key loading issue
load_dotenv() won't override a value already set in the environment. Use load_dotenv(override=True) if you suspect a stale value. Always keep one .env in your root project folder — not inside subfolders.
"""