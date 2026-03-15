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

"""
Today was about making Python make decisions.
Before today, your scripts ran the same code every time regardless of the data. That's useless in the real world — real data is inconsistent and your scripts need to respond differently depending on what they find.
if and else give you two paths — do this if the condition is true, do that if it's not. elif adds more paths in between when two outcomes aren't enough. and and or let you combine conditions — and requires both to be true, or only needs one.
You finished by combining everything into a loop over real customer data — flagging incomplete records first, then categorising complete ones by spend tier. That's a billable script. A client with a messy CRM export would pay for exactly that.

FULL NOTES — DAY 4: If/Else Logic Basics
if / else
Runs one block of code if a condition is True, a different block if it's False. Indentation defines which code belongs to which block.
elif
Sits between if and else. Lets you check additional conditions when two outcomes aren't enough. Python reads top to bottom and stops at the first True condition.
Comparison operators
Used to build conditions. Return True or False.

== equal to
!= not equal to
> greater than
< less than
>= greater than or equal to
<= less than or equal to

and
Both conditions must be True for the block to run.
or
At least one condition must be True for the block to run.
Order of checking
Python evaluates conditions top to bottom. The moment it finds one that's True, it runs that block and ignores the rest. This means you must order your conditions correctly — most specific first.
Session capstone
Combined a for loop (Day 3) with if/elif/else and and/or to triage a list of customer dictionaries — flagging incomplete records and categorising complete ones by spend tier.
"""