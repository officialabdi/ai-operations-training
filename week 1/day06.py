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