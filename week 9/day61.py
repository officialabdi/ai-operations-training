from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv("AS.txt")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You extract order details and return them as JSON. Return a JSON object with this structure: {\"order\": {\"items\": [{\"name\": string, \"quantity\": integer}], \"delivery_address\": string, \"total_items\": integer}}"},
        {"role": "user", "content": "Hi, I'd like a Margherita pizza and a Coke please. Delivering to 14 Main Street."}
    ],
    response_format={"type": "json_object"}
)

print(response.choices[0].message.content)
data = json.loads(response.choices[0].message.content)
print(data["order"]["total_items"])

def validate_order(order):
    if not isinstance(order["delivery_address"], str):
        print("Error: delivery_address is missing or not a string")
        return
    if not isinstance(order["items"], list) or len(order["items"]) == 0:
        print("Error: items is missing or empty")
        return
    if not isinstance(order["total_items"], int):
        print("Error: total_items is missing or not an integer")
        return
    print("Order validated successfully.")

validate_order(data["order"])