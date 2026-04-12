import anthropic
from dotenv import load_dotenv

load_dotenv("env", override=True)

client = anthropic.Anthropic()

cost_per_input_token = 0.80 / 1_000_000
cost_per_output_token = 2.40 / 1_000_000

def stream_luigi_response(customer_question):
    print(f"\ncustomer: {customer_question}")
    print("luigis ai: ", end="", flush=True)

    full_response = ""

    with client.messages.stream(
        model="claude-3-haiku-20240307",
        max_tokens=300,
        system="You are a friendly assistant for Luigi's Pizzeria in Dublin. Keep answers brief and helpful.",
        messages=[
            {"role": "user", "content": customer_question}
        ]
    ) as stream:
        for event in stream:
            if event.type == "content_block_delta":
                print(event.delta.text, end="", flush=True)
                full_response += event.delta.text

    print("\n")

    final = stream.get_final_message()
    input_tokens = final.usage.input_tokens
    output_tokens = final.usage.output_tokens
    cost = (input_tokens * cost_per_input_token) + (output_tokens * cost_per_output_token)

    print(f"[Tokens: {input_tokens} in / {output_tokens} out | Cost: ${cost:.6f}]")
    return full_response


stream_luigi_response("What time do you close on Sundays?")
stream_luigi_response("Do you have a gluten-free base?")