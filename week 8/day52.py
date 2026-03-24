import anthropic
from dotenv import load_dotenv
import os
import json

load_dotenv(override=True)

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

customer_question = input("customer question")
response = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1024,
    system="You are an order handler for Luigi's Pizzeria. Return your response as JSON only, with no extra text. Use these fields: pizza_type, size, customer_name.",

    messages=[
    {"role": "user", "content": f"{customer_question}"}
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