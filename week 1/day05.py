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