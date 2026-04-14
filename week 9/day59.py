import anthropic
from dotenv import load_dotenv

load_dotenv("AS.txt")

client = anthropic.Anthropic()

def get_order_status(order_id: str) -> str:
    orders = {
        "ORD-42": "Out for delivery. Arriving in 15 minutes.",
        "ORD-43": "Being prepared in the kitchen.",
        "ORD-44": "Order received. Preparation starting soon.",
    }
    return orders.get(order_id, f"No order found with ID {order_id}.")


tools = [
    {
        "name": "get_order_status",
        "description": "Looks up the current status of a customer order at Luigi's Pizzeria using the order ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The unique ID of the customer's order, e.g. ORD-42"
                }
            },
            "required": ["order_id"]
        }
    }
]


system_prompt = "You are a helpful assistant for Luigi's Pizzeria. Answer customer questions in a friendly, concise way."

messages = [
    {"role": "user", "content": "Hi, can you check the status of my order? My order ID is ORD-42."}

]

print("--- sending first api call ---")


first_response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    system=system_prompt,
    tools=tools,
    messages=messages
)

print(f"stop reason: {first_response.stop_reason}")
print(f"First call — input tokens: {first_response.usage.input_tokens} | output tokens: {first_response.usage.output_tokens}")


if first_response.stop_reason == "tool_use":

    tool_call = next(block for block in first_response.content if block.type == "tool_use")

    print(f"\nclaude wants to use tool: {tool_call.name}")
    print(f"with arguments: {tool_call.input}")


    order_id = tool_call.input["order_id"]
    result = get_order_status(order_id)

    print(f"function returned: {result}")


    messages.append({"role": "assistant", "content": first_response.content})
    messages.append({
        "role": "user",
        "content": [
            {
                "type": "tool_result",
                "tool_use_id": tool_call.id,
                "content": result
            }
        ]
    })

    # ── SECOND API CALL ───────────────────────────────────────
    # Claude now reads the result and writes its final reply.

    print("\n--- Sending second API call ---")

    second_response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=system_prompt,
        tools=tools,
        messages=messages
    )

    print(f"Second call — input tokens: {second_response.usage.input_tokens} | output tokens: {second_response.usage.output_tokens}")

    total_input = first_response.usage.input_tokens + second_response.usage.input_tokens
    total_output = first_response.usage.output_tokens + second_response.usage.output_tokens
    print(f"\nTotal tokens — input: {total_input} | output: {total_output}")

    # ── FINAL REPLY ───────────────────────────────────────────

    final_reply = second_response.content[0].text
    print(f"\nClaude's final reply to the customer:\n{final_reply}")

else:
    # Claude answered directly without needing a tool
    print(f"\nClaude replied directly:\n{first_response.content[0].text}")
