name = "mario"
if name == "luigi":
    print("welcome back, boss")
else:
    print("who are you")

order_total = 65
if order_total >= 50:
    print("free delivery applied")
else:
    print("delivery charge applied")

order_total = 75
if order_total < 20:
    print("small order")
elif order_total <= 50:
    print("medium order")
else:
    print("large order")

total_spend = 120
order_count = 2
if total_spend > 100 and order_count > 3:
    print("eligible for loyalty discount.")
else:
    print("not eligible.")

customer_name = "maria"
phone_number = "087-123-4567"
if customer_name == "" or phone_number == "":
    print("incomplete record - flag for review.")
else:
    print("record is complete.")

customers = [
    {"name": "Maria", "phone": "087-111-2222", "spend": 200},
    {"name": "", "phone": "086-333-4444", "spend": 80},
    {"name": "Tony", "phone": "", "spend": 60},
    {"name": "Luigi", "phone": "085-555-6666", "spend": 45},
]

for customer in customers:
    if customer["name"] == "" or customer["phone"] == "":
        print("incomplete record - flag for review.")
    elif customer["spend"] > 150:
        print(customer["name"] + " - gold customer")
    elif customer["spend"] >= 50:
        print(customer["name"] + " - silver customer")
    else:
        print(customer["name"] + " - bronze customer")