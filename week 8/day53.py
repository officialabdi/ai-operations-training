import os
import json
from dotenv import load_dotenv
import anthropic

load_dotenv()

api_key = os.environ.get("ANTHROPIC_API_KEY")
print("API key loaded:", api_key[:8] + "..." if api_key else "NOT FOUND")

client = anthropic.Anthropic(api_key=api_key)

customer_question = input("Customer question: ")

response = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1024,
    system="You are an order handler for Luigi's Pizzeria. Return your response as JSON only, with no extra text. Use these fields: pizza_type, size, customer_name.",
    messages=[
        {"role": "user", "content": customer_question}
    ]
)

text = response.content[0].text

try:
    parsed = json.loads(text)
    print("\n--- Order Received ---")
    print(f"Customer: {parsed['customer_name']}")
    print(f"Pizza: {parsed['pizza_type']}")
    print(f"Size: {parsed['size']}")
    print("Status: Order sent to kitchen")
except json.JSONDecodeError:
    print("Error: Claude did not return valid JSON")
    print("Raw response was:", text)