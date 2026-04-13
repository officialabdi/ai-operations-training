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

"""
FULL NOTES — DAY 57: STREAMING API RESPONSES
What streaming is
A streaming API call sends the response back in small chunks as Claude generates them, rather than waiting until the full response is ready. Your code receives and processes each chunk the moment it arrives.
How it differs from a standard call
A standard call blocks your code until the full response is ready, then returns it all at once. A streaming call returns a stream object immediately and delivers text progressively through events.
The method used
client.messages.stream() — provided by the Anthropic SDK specifically for streaming. Takes the same parameters as client.messages.create(). Must be used inside a with statement so the connection is opened and closed properly.
The with statement
Wrapping the stream in with ... as stream: ensures the live connection is managed correctly — opened when the block starts, closed when it ends, even if an error occurs.
Events and event types
The stream delivers a series of events. Not all events contain text. The only event type that contains actual text is content_block_delta. You check for this with event.type == "content_block_delta".
Accessing the text in a chunk
event.delta.text — this is the text fragment inside a content_block_delta event.
Printing chunks correctly
print(event.delta.text, end="", flush=True)

end="" prevents Python adding a newline after each chunk
flush=True forces Python to display the chunk immediately without buffering

Capturing the full response
The stream does not store the complete text for you. To capture it, initialise an empty string before the loop (full_response = "") and concatenate each chunk as it arrives (full_response += event.delta.text).
Cost tracking with streaming
Call stream.get_final_message() after the with block closes. This returns a full response object containing usage.input_tokens and usage.output_tokens, identical to what you used on Day 55.
The full pattern
full_response = ""
with client.messages.stream(...) as stream:
    for event in stream:
        if event.type == "content_block_delta":
            print(event.delta.text, end="", flush=True)
            full_response += event.delta.text
final = stream.get_final_message()


"""