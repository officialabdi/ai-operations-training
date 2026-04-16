import anthropic
from dotenv import load_dotenv

load_dotenv("AS.txt")

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    system="You are an ordering assistant for Luigi's Pizzeria in Dublin. When given a complex order or decision, think step by step before giving your final answer. Show your reasoning first, then state your conclusion clearly and No emojis.",
    messages=[
        {"role": "user", "content": " A customer wants to schedule a pickup for a small pizza,"},
        {"role": "assistant", "content": "sure, when would you like to pickup the small pizza and what toppings would you like on it?"},
        {"role": "user", "content": "Can i order cookies but gluten free?"},
        {"role": "assistant", "content": "yes, we do have gluten free cookies available. Do you want the 6 cookie deal or 4 cookie deal?"},
        {
            "role": "user",
            "content": """A customer wants to order a family order. They are choosing between 2 options:
        1. 2 large pizzas at 14 euros each.
        2. 3 medium pizzas at 9 each for a group of 6.
        which options is cheaper in total and by how much?

        think step by step before giving your final answer."""
        }
    ]
)

print(response.content[0].text)
