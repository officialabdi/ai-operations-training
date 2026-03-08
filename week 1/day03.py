"""exercise 1
names = ["  luigi  ", "MARIO", "sofia"]
cleaned_names = []

for name in names:
    clean_name = name.strip().title()
    cleaned_names.append(clean_name)
print(cleaned_names)"""

"""exercise 2
customer = {
    "name": "  LUIGI RUSSO  ",
    "email": "LUIGI@PIZZA.COM  ",
    "city": "  dublin"
}

for key, value in customer.items():
    if key == "email":
        print(key, value.strip().lower())
    else:
        print(key, value.strip().title()) 


#exercise 3

customers = ["  luigi russo  ", "MARIO COSTA", "sofia   ", "  ANNA MURPHY"]
emails = ["LUIGI@PIZZA.COM  ", "mario@costa.ie", "  SOFIA@GMAIL.COM", "anna@murphy.ie  "]

cleaned_customers = []
cleaned_emails = []

for name in customers:
    cleaned_customers.append(name.strip().title())

for email in emails:
    cleaned_emails.append(email.strip().lower())

print(cleaned_customers)
print(cleaned_emails)
"""

customers = [
    {"name": "  LUIGI RUSSO  ", "email": "LUIGI@PIZZA.COM  ", "city": "  dublin"},
    {"name": "mario costa", "email": "  MARIO@COSTA.IE", "city": "CORK  "},
    {"name": "  SOFIA MURPHY", "email": "SOFIA@GMAIL.COM", "city": "  galway  "}
]

cleaned_customers = []
for customer in customers:
    cleaned = {}
    for key, value in customer.items():
        if key == "email":
            cleaned[key] = value.strip().lower()
        else:
            cleaned[key] = value.strip().title()
    cleaned_customers.append(cleaned)
for customer in cleaned_customers:
    print(customer)
