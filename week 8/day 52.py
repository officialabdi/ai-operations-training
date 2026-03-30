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


"""
Full Notes — Day 52: Parsing JSON Responses
The Claude API response object
The API returns a structured object, not a plain string. Key fields: content (list of response blocks), model, stop_reason, usage (input and output token counts). The actual message text is at response.content[0].text. Content is a list because Claude can return multiple blocks in one response.
Accessing text content
response.content[0].text — go into the content list, take the first item, access its text field. For a second block it would be response.content[1].text.
Prompting Claude to return JSON
Set the system prompt to instruct Claude to return JSON only with no extra text, and specify the exact fields you want. Claude will return a raw JSON string instead of prose.
Parsing JSON with json.loads()
json is a built-in Python module. json.loads(text) takes a JSON string and converts it into a Python dictionary. Without this step the response is just a string — you cannot access fields from it.
Accessing dictionary fields
Once parsed, use square bracket notation with the key name as a string: parsed["customer_name"], parsed["pizza_type"], parsed["size"].
Handling parse failures
Wrap json.loads() in a try/except block catching json.JSONDecodeError. If Claude returns something that isn't valid JSON the program logs the error and the raw response instead of crashing.
Business application
This pattern turns Claude into a structured data extraction layer. A customer types a natural language order, Claude extracts the fields, your code uses those fields to trigger next steps — logging, routing, confirmation messages.

"""