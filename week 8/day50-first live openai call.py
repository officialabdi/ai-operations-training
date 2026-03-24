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

"""
Q: What is an API in plain English?
A: A way for two pieces of software to talk to each other automatically — you send a request, it sends back a response.
Q: What is the key difference between using ChatGPT and calling the OpenAI API?
A: ChatGPT requires a human typing manually. The API lets your code send and receive messages automatically with no human involved.
Q: Why would a client pay for an API-based system when ChatGPT exists for free?
A: ChatGPT is a generic tool. An API-based system is tailored to their business, automated, and integrated into their workflow.
Q: What is an API key?
A: A unique credential that identifies your OpenAI account on every request. OpenAI uses it to track usage and bill you.
Q: What happens if your API key is exposed publicly?
A: Anyone can make API calls that bill to your account. Revoke it immediately and generate a new one.
Q: What is a .env file and why do you use one?
A: A plain text file that stores secrets like API keys. Keeps sensitive credentials out of your code and off GitHub.
Q: What does load_dotenv() do?
A: Reads your .env file and loads its contents into memory so your code can access them as variables.
Q: What does adding .env to .gitignore do — and what doesn't it do?
A: It stops Git from tracking the file going forward. It does not remove the file from commits that have already been made.
Q: What are the three message roles in the OpenAI API?
A: System — background instructions for the AI. User — the message you send. Assistant — the AI's reply.
Q: What is the system role used for in a client automation?
A: To give the AI its identity and behaviour rules before the conversation starts — the client never sees it.
Q: Where is the actual reply text inside an OpenAI response object?
A: Inside choices[0].message.content.
Q: What does finish_reason of 'stop' mean in an API response?
A: The model completed its response naturally with no errors or cutoffs.
Q: What are tokens and why do they matter for client work?
A: Roughly one token per word. OpenAI charges per token. You track token usage to calculate automation costs and price your services.
Q: What is an f-string and why is it useful in API calls?
A: A Python string prefixed with f that lets you embed variables using curly braces. Makes API messages dynamic instead of hardcoded.
Q: What is the business value of combining a system prompt with dynamic user data in an API call?
A: It creates a personalised, automated AI response for each customer — the foundation of any client-facing AI product.
"""