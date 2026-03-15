email = "  luigi@pizza.ie  "
cleaned = email.strip()
print(cleaned)
print(len("  luigi@pizza.ie  "))
print(len("luigi@pizza.ie"))

name = "LUIGI NAPOLI"
cleaned = name.strip().lower()
print(cleaned)

phone = "087-123-4567"
cleaned = phone.replace("-", "").replace(" ", "")
print(cleaned)

customers = [
    {"name": "  LUIGI Napoli  ", "email": "  luigi@pizza.ie  ", "phone": "087-111-2222"},
    {"name": "maria murphy", "email": "MARIA@PIZZA.IE", "phone": "086 333 4444"},
    {"name": "SEAN O BRIEN  ", "email": "  sean@pizza.ie", "phone": "085-555-6666"},
    {"name": "  Aoife Ryan", "email": "aoife@pizza.ie  ", "phone": ""},
]
missing_count = 0

for customer in customers:
    customer["name"] = customer["name"].strip().lower()
    customer["email"] = customer["email"].strip().lower()
    if customer["phone"]:
        customer["phone"] = customer["phone"].replace("-", "").replace(" ", "")
    else:
        customer["phone"] = "MISSING"
        missing_count += 1
    print(customer)
print("---")
print("total records:", len(customers))
print("missing phone numbers:", missing_count)


"""
Today you built a data cleaner that processes a simulated spreadsheet of messy customer records.
You learned three string cleaning methods. .strip() removes invisible whitespace from the start and end of a value — essential for any field that comes from a form. .lower() standardises capitalisation so the same name entered different ways is treated as one record. .replace() swaps out unwanted characters — used to strip dashes and spaces from phone numbers so they're in a consistent format.
You chained these methods together on single lines, which is how real cleaning code is written.
You then simulated a real client problem — a missing phone field — and handled it with if/else logic. If the field has a value, clean it. If it's empty, flag it as MISSING so it's visible and actionable rather than silently broken.
Finally you added a summary counter so the output tells Luigi exactly how many records need follow-up. That's the difference between raw code output and a deliverable you can hand to a client.
The two indentation errors you hit today were genuine mistakes and you fixed both. That's the skill — reading the output, identifying what went wrong, fixing it.

FULL NOTES — DAY 5: Cleaning Messy Data
What was covered
Simulating a real spreadsheet as a list of dictionaries, and writing a loop that cleans every record in one pass.

.strip()
Removes whitespace — spaces, tabs — from the start and end of a string. Does not touch characters in the middle. Returns the cleaned string.
Used on name and email fields where accidental spaces cause mismatches in any downstream system.

.lower()
Converts every character in a string to lowercase. Returns the lowercased string.
Used to standardise names and emails so that "LUIGI", "Luigi", and "luigi" are all treated as the same value.

Method chaining
You can call multiple methods on the same line. Each method runs on the result of the one before it. .strip().lower() first strips whitespace, then lowercases the result.

.replace(a, b)
Finds every occurrence of a in a string and replaces it with b. If b is an empty string "", the character is deleted entirely.
Used to remove dashes and spaces from phone numbers. Multiple .replace() calls can be chained to handle more than one character.

Handling missing fields with if/else
Before cleaning a field, check if it contains a value. An empty string "" is falsy in Python — an if check on it returns False. If the field is empty, assign the string "MISSING" instead of attempting to clean it.

Counter variable
A variable set to 0 before the loop. Inside the loop, += 1 adds one to it each time a missing field is found. After the loop, it holds the total count of missing records.

len()
Returns the number of items in a list. Used here to report total records processed.

Indentation rules reinforced
Code inside a for loop is indented one level. Code inside an if or else block is indented one further level. Code that runs after the loop finishes has no indentation. Placing code at the wrong level changes when and how many times it runs.

"""