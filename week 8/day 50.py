from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

customer_name = "marco"
order = "pepperoni pizza and a side of garlic bread"

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant for Luigi's Pizzeria. Keep replies short and friendly."},
        {"role": "user", "content": f"My name is {customer_name} and I want to order: {order}"}
    ]
)

print(response.choices[0].message.content)
