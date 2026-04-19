import requests

url = "https://hook.eu1.make.com/3o1f3lizf9fduu71l2uapl2pkbqoz4m2"

payload = {"message": "What time do you close on Sundays?"}

response = requests.post(url, json=payload)
print(response.text)



"""FULL NOTES — Day 62: Connecting API to No-Code (Make + OpenAI)
What this session covered
The goal of Day 62 was to take the OpenAI API knowledge built in Days 50–61 and move the API call from Python into a Make.com scenario. Instead of a developer running a script to trigger an AI response, Make handles the entire call automatically based on an incoming trigger.

Why connect API to no-code
Python API calls require a developer to run the script. Make scenarios run automatically in response to events — emails, forms, webhooks, schedules. For Irish SME clients who are not developers, Make is the practical delivery vehicle. You build it once, they own the workflow, and it runs without you. That is the billable model.
Python is still better for complex logic, batch jobs, and data transformation. Make is better for event-driven, multi-app workflows that clients need to monitor and manage themselves.

Two ways to call OpenAI from Make
The native OpenAI module is a pre-built Make integration. You connect your API key, pick an action from a dropdown, fill in your prompt, and Make handles the request. It is fast to set up and easy for a client to read. Use it for simple ChatGPT workflows.
The HTTP module is a general-purpose request builder. You manually set the URL, headers, and JSON body — exactly like a Python requests call. It works for any API including Claude, custom endpoints, and non-standard configurations. Use it when the native module cannot do what you need or when you need full control.

The scenario built today
Three modules in sequence:
Module 1 — Custom Webhook. Receives incoming data from any external source. Make generates a unique URL. Anything posted to that URL triggers the scenario. The data sent in the request body becomes available to all downstream modules.
Module 2 — HTTP module (Make a request). Sends a POST request to https://api.openai.com/v1/chat/completions. Authentication is set via the Authentication field using Bearer sk-... format — the word Bearer, a space, then the actual key. Body content type is application/json, body input method is JSON string. Parse response is set to Yes so Make understands the response structure.
Module 3 — Webhook Response. Sends the OpenAI reply back to whatever triggered the webhook. The body is mapped to 2. Data.choices[]: message.content — the parsed reply text from the HTTP module.
A fourth module — Google Sheets Add a Row — was added to log every interaction. The Question column maps to {{1.message}} and the Answer column maps to 2. Data.choices[]: message.content.

Dynamic data with {{module.field}} syntax
Make uses double curly braces to reference data from previous modules. {{1.message}} means: go to module 1 (the webhook) and get the field called message. This is inserted into the prompt body before Make sends the request to OpenAI, so every incoming message becomes the user's question rather than a hardcoded string.
The number always refers to the module position in the scenario. The word after the dot is the exact field name from the incoming data.

Parsing the OpenAI response
OpenAI returns a full JSON object containing metadata, token usage, model information, and the reply text. The reply text is nested at choices > 0 > message > content. Make exposes this path in the mapping panel after the scenario has run once with real data — before that first run, the Data field cannot be expanded because Make has not seen the response structure yet.

How the test was run
A Python script using the requests library sent a POST request to the Make webhook URL with a JSON body containing a message field. Make received it, injected the message into the OpenAI prompt, received the reply, returned it to the script, and logged it to Google Sheets. The terminal displayed Luigi's answer directly."""