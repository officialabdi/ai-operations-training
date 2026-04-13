import os 
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv("AS.txt")

client = Anthropic()

messages = []

system_prompt = "You are a helpful assistant for Luigi's Pizzeria in Dublin. Answer questions about the menu, opening hours, and taking orders."

print("Luigi's pizzeria assistant - type 'quit' to exit\n")

total_input = 0
total_output = 0

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        print("ending conversation.")
        break

    messages.append({"role": "user", "content": user_input})

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=system_prompt,
        messages=messages

    )
    reply = response.content[0].text

    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens#

    total_input += input_tokens
    total_output += output_tokens

    
    print(f"[Turn cost — Input: {input_tokens} | Output: {output_tokens}]")
    print(f"[Running total — Input: {total_input} | Output: {total_output}]\n")

    messages.append({"role": "assistant", "content": reply})

    print(f"luigi's ai: {reply}\n")
