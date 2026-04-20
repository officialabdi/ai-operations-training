from anthropic import Anthropic
from dotenv import load_dotenv 
import json

load_dotenv("AS.txt")

client = Anthropic()

SYSTEM_PROMPT = """
You are a customer service assistant for Luigi's Pizzeria in Dublin.
Your job is to answer menu questions and take customer orders.

Rules:
- Never process refunds or payments
- Never make promises about delivery times or discounts
- If a customer requests something outside your scope, set action to "escalate_to_human" and tell them a team member will follow up
- Keep all replies short, friendly, and professional
- Never use emojis

You must always respond in this exact JSON format:
{
  "intent": "<what the customer is trying to do>",
  "reply": "<your short reply to the customer>",
  "action": "<continue | confirm_order | escalate_to_human>",
  "order": {
    "name": "<customer name or null>",
    "items": "<items ordered or null>",
    "address": "<delivery address or null>"
  }
}
"""

messages = []

print("luigis pizzeria assistant, type 'quit' to exit.\n")



def get_menu():
    return {
        "pizzas": ["margherita", "pepperoni", "bbq chicken", "veggie supreme" ],
        "sizes": ["small", "medium", "large"],
        "prices": {"small": 10, "medium": 15, "large": 18}
    }


tools = [
    {
        "name": "get_menu",
        "description": "Returns the current Luigi's Pizzeria menu including pizzas, sizes and prices",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

def parse_response(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        text = text.rsplit("```", 1)[0]
    return json.loads(text.strip())


while True:
    user_input = input("you: ")

    if user_input.lower() == "quit":
        break

    messages.append({"role": "user", "content": user_input})

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        tools=tools,
        messages=messages
    )

    if response.stop_reason == "tool_use":
        tool_result = get_menu()
        messages.append({"role": "assistant", "content": response.content})
        messages.append({
            "role": "user",
            "content": [{
                "type": "tool_result",
                "tool_use_id": response.content[0].id,
                "content": json.dumps(tool_result)
            }]
        })

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=tools,
            messages=messages
        )
    

    with client.messages.stream(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        tools=tools,
        messages=messages
    ) as stream:
        reply = ""
        for text in stream.text_stream:
            reply += text

        
    
    messages.append({"role": "assistant", "content": reply})

    try:
        parsed = parse_response(reply)
        print(f"\nluigis bot: {parsed['reply']}")
        print(f"[action: {parsed['action']} | intent: {parsed['intent']}]\n")

        if parsed['action'] == "escalate_to_human":
            print("--- escalating to luigis team. a staff member will follow up. ---\n")
            break

    except json.JSONDecodeError:
        print("\nLuigi's Bot: Sorry, something went wrong. Please try again.\n")
    