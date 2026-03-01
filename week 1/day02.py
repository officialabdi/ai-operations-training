customer = {
    "name": "  john MURPHY  ",
    "email": "  JOHN@GMAIL.COM  ",
    "phone": "087-123-4567"
}
customer["name"] = customer["name"].strip().title()
customer["email"] = customer["email"].strip().lower()
customer["phone"] = customer["phone"].replace("-", "")
print(customer)

customer2 = {
    "name": "  SIOBHAN kelly  ",
    "email": "",
    "phone": "086-999-1234"
}

customer2["name"] = customer2["name"].strip().title()
customer2["email"] = customer2["email"].lower()
customer2["phone"] = customer2["phone"].replace("-", "")

if customer2["email"]:
    customer2["email"] = customer2["email"].strip().lower()
else:
    customer2["email"] = "N/A"

print(customer2)

customer3 = {
    "name": "  BRIAN o'connor  ",
    "email": "",
    "phone": ""
}

for key, value in customer3.items():
    if not value:
        customer3[key] = "N/A"

print(customer3)

customer4 = {
    "name": "  AOIFE murphy  ",
    "email": "  AOIFE@GMAIL.COM  ",
    "phone": ""
}

for key, value in customer4.items():
    if not value:
        customer4[key] = "N/A"
    elif key == "name":
        customer4[key] = value.strip().title()
    else:
        customer4[key] = value.strip().lower()

print(customer4)


""" 
FULL NOTES — Day 2: Cleaning Dictionaries & Handling Missing Data
Dictionary
A data structure that stores information as key-value pairs. Each piece of data has a name (the key) and a value. Used to represent a real-world record like a customer, order, or product. Written with curly braces. Values are accessed using their key name in square brackets.
Accessing a dictionary value
You use the key name in square brackets to read or write a specific field. To clean a field, you access it, apply your cleaning methods, and assign the result back to the same key.
Handling empty values
An empty string is treated as False in Python. A string with content is treated as True. Before cleaning a field, check if it has content using an if statement. If it's empty, assign a safe default like "N/A" instead of trying to clean it.
not value
A way to check if a field is empty inside a loop. Means "if this value has nothing in it, do something."
.items()
A dictionary method that returns every key-value pair in the dictionary as a pair you can loop through. Used to process every field in a record without targeting them one by one.
elif
Short for "else if." Used when you have more than two possible conditions. Python checks each condition in order — if the first is true it runs that block, otherwise it checks the next one. Used to apply different cleaning logic to different field types inside a loop.
Universal cleaning loop pattern
Loop through every field using .items(). If the field is empty, set it to "N/A". If the field is a name, strip and title case it. For everything else, strip and lowercase it. One loop handles the entire record cleanly.

"""