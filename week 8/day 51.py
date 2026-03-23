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
