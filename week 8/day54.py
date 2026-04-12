import anthropic
from dotenv import load_dotenv
import os

load_dotenv("env", override=True)

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

customer_complaint = "my pizza arrived cold and the wrong toppings were added. really disappointed."

step1_response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=50,
    messages=[
        {
            "role": "user",
            "content": f"Reply with one word only. No other text. Choose from exactly these three options: angry, neutral, or happy.\n\nComplaint: {customer_complaint}"

        }
    ]
)

step1_output = step1_response.content[0].text.strip()
print(f"step 1 - sentiment: {step1_output}")

step2_response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=150,
    messages=[
        {
            "role": "user",
            "content": f"a customer left a complaint. their sentiment has been classified as: {step1_output}.\n\nwrite a short, professional reply from luigis pizzeria. 2-3 sentences maximum."

        }
    ]

)

step2_output = step2_response.content[0].text.strip()
print(f"step 2 - reply: {step2_output}")


step3_response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=100,
    messages=[
        {
            "role": "user",
            "content": f"Condense this reply into one sentence suitable for an SMS.\n\nReply: {step2_output}"
        }
    ]
)

step3_output = step3_response.content[0].text.strip()
print(f"Step 3 - SMS: {step3_output}")

"""
What prompt chaining is
Prompt chaining is the technique of making multiple API calls in sequence, where the output of one call is passed as input to the next. Each call is isolated and focused on one job.
Why it exists
A single prompt attempting multiple tasks loses focus, and errors in one part contaminate everything else. There are no checkpoints to inspect or fix output mid-way. Chaining solves this by isolating each stage, allowing you to catch and handle errors between steps before they spread.
How it works
The Claude API has no memory between calls. Every call is completely fresh. You are responsible for carrying output forward manually. The pattern is:

Make API call → extract .content[0].text → store in a variable
Inject that variable into the next call's prompt
Repeat for as many steps as needed

There is no special chaining function. It is plain Python logic connecting standard API calls.
The .env file naming issue (session note)
If your env file is not named .env but something else (e.g. env), you must pass the filename explicitly to load_dotenv:
pythonload_dotenv("env", override=True)
```

The default behaviour of `load_dotenv()` looks for `.env` only.

**Strict prompt instructions**

When you need Claude to return a specific word or format, vague instructions fail. Be explicit:
```
Reply with one word only. No other text. Choose from exactly these three options: angry, neutral, or happy.
When to use chaining vs a single prompt
Use a single prompt when the task is simple, self-contained, and speed matters more than precision.
Use chaining when:

The task has distinct stages that depend on each other
You need to inspect output between steps
Errors in one step would ruin everything after it
Each step needs its own focused instruction
The output format changes between steps

Business application
A 3-step complaint handler for Luigi's Pizzeria:

Step 1 — classify sentiment from customer complaint
Step 2 — draft a professional reply based on sentiment
Step 3 — condense reply to one SMS sentence

This is a sellable automation for any Irish SME handling customer complaints.

"""