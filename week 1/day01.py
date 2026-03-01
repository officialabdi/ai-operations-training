name = "  luigis pizzeria  "
cleaned_name = name.strip().title()
print(cleaned_name)

phone = "087-123-4567"
cleaned_phone = phone.replace("-", "")
print(cleaned_phone)

customers = ["  john murphy  ", "MARY O'BRIEN", "  pete KELLY"]
cleaned_customers = []
for customer in customers:
    cleaned = customer.strip().title()
    cleaned_customers.append(cleaned)

print(cleaned_customers)

emails = ["  JOHN@GMAIL.COM  ", "MARY@HOTMAIL.COM", "  pete@yahoo.com  "]

cleaned_email = []
for email in emails:
    cleaned = email.strip().lower()
    cleaned_email.append(cleaned)

print(cleaned_email)

"""
FULL NOTES — Day 1: Data Sanitization
Dirty data — Any data with errors, inconsistencies, or missing values that would produce wrong results or break a system. Common types: extra spaces, inconsistent capitalisation, wrong formats, duplicates, missing values.
String — Any text value in Python. Written inside quotes. All customer names, emails, phone numbers, and addresses are strings.
.strip() — Removes spaces from the left and right edges of a string. Does not touch spaces in the middle. Use this on any text field coming from a form, spreadsheet, or external source.
.lower() — Converts every character in a string to lowercase. Use for emails and any field where you need to compare or match values.
.upper() — Converts every character to uppercase.
.title() — Capitalises the first letter of every word. Use for customer names.
Chaining — Applying multiple string functions back to back on one line. Python executes them left to right. Example: .strip().title() strips first, then applies title case to the result.
.replace(old, new) — Finds every occurrence of old inside a string and replaces it with new. To delete something, replace it with "". Use for removing dashes from phone numbers or fixing consistent typos.
List — A collection of items stored in one variable. Written with square brackets [], items separated by commas. Use lists — not parentheses — for any data you intend to clean, modify, or pass through a pipeline.
Tuple — A collection written with parentheses (). Locked — cannot be modified. Do not use for data you're working with.
For loop — Goes through every item in a list one by one and runs the same code on each. Used to apply cleaning functions to an entire dataset automatically.
.append(item) — Adds an item to the end of an existing list. Used inside a loop to collect cleaned results into a new list for use in the next step."""