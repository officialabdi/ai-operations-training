def greet_customer(name):
    message = "hello " + name + ", welcome to luigis pizzeria!"
    return message
result = greet_customer("maria")
print(result)

def calculate_order_total(price, quantity):
    total = price * quantity
    return total
order = calculate_order_total(12.50, 3)
print("order total: \u20ac" + str(order))

def apply_discount(price, discount_percent):
    discoun_amount = price * discount_percent / 100
    final_price = price - discoun_amount
    return final_price
order = apply_discount(14.00, 10)
print("order total: \u20ac" + str(order))

def process_order(name, price, quantity, discount_percent):
    total = calculate_order_total(price, quantity)
    final_amount = apply_discount(total, discount_percent)
    return name + " owes \u20ac" + str(final_amount)

result = process_order("maria", 12.50, 3, 10)
print(result)

"""
Today you learned what functions are and why they exist. A function is a named block of code that does one specific job. You write it once and reuse it as many times as you need. This matters for client work because it means when logic needs to change, you fix it in one place instead of hunting through your entire script.
You learned that a function takes inputs called parameters, does something with them, and hands back a result using return. The function doesn't print anything — it just returns a value. Printing is a separate step.
You also learned that functions can call other functions. Instead of rewriting logic, you pass data through functions you already built. That's how real pipelines work — each function does one job, and a master function chains them together.
You built this from scratch: a greeting function, an order total calculator, a discount calculator, and a master order processor that used the other two inside it.

FULL NOTES — DAY 6: FUNCTIONS INTRODUCTION
What a function is
A function is a named block of code that performs one specific job. You define it once and call it by name whenever you need it.
Why functions exist
Without functions, the same logic gets repeated throughout a script. If that logic needs to change, every copy needs to be updated. Functions centralise that logic — fix it once, everything using it updates automatically.
The four parts of a function

def — the keyword that tells Python you are defining a function
Name — what you call the function when you want to use it
Parameters — the inputs the function receives, listed inside brackets
Return — the value the function hands back when it finishes

Parameters
Parameters are the inputs you pass into a function. Inside the function they behave as normal variables. You can have one parameter, multiple parameters, or none at all.
Return
The return statement ends the function and sends a value back to whoever called it. A function that has no return statement hands back nothing. Return does not print — it passes a value back silently.
Calling a function
To run a function you already defined, write its name followed by brackets containing the values you want to pass in. Store the result in a variable if you need to use it.
Functions calling other functions
A function can call another function inside its body. This allows you to chain logic — each function does one job, and a master function coordinates them in sequence. This is how real data pipelines are structured.
Client value
Functions make code reusable, easier to fix, and easier to hand off. For an Irish SME client, this means faster turnaround when business rules change and cleaner deliverables that won't break when one thing is updated.


"""