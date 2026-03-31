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

# --- STEP 3: Condense the reply to one SMS sentence ---
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