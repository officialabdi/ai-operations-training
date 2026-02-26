def calculate_discount(price,discount_percent):
    print(f"debug: price = {price}")
    print(f"debug: discount_percent = {discount_percent}")
    
    discount_decimal = discount_percent / 100
    print(f"debug: discount_decimal = {discount_decimal}")
    discount_amount = price * discount_decimal
    print(f"debug: discount_amount = {discount_amount}")
    final_price = price - discount_amount
    print(f"debug: final_price = {final_price}")
    return final_price

result = calculate_discount(100, 20)
print(f"\nprice after discount: ${result}")

# ========================================
# cleaned version (no debug prints)
# ========================================

def calculate_discount(price, discount_percent):
    
    discount_decimal = discount_percent / 100
    discount_amount = price * discount_decimal
    final_price = price - discount_amount
    return final_price

def calculate_tax(price):
    tax_rate = 0.23
    tax = price * tax_rate
    return tax
def calculate_total(price, discount_percent):
    print(f"\ndebug: starting with price = ${price}")
    discounted_price = calculate_discount(price, discount_percent)
    print(f"debug: after {discount_percent}% discount = ${discounted_price}")
    tax = calculate_tax(discounted_price)
    print(f"debug: tax caluculated on ${discounted_price} = ${tax}")
    total = discounted_price + tax
    print(f"debug: total = ${discounted_price} + ${tax} = ${total}")
    return total


# ========================================
# real business example: email validation bug
# ========================================

def validate_email(email):
    
    
    if "@" not in email:
        return False
    
    
    parts = email.split("@")
    
    
    if len(parts) != 2:
        return False
    
    
    username = parts[0]
    domain = parts[1]
    
    if len(username) > 0 and len(domain) > 0:
        return True
    else:
        return False


print("\n\n=== testing email validation ===")

test_emails = [
    "john@gmail.com",      
    "invalid.email",        
    "@gmail.com",          
    "john@",               
    "john@@gmail.com",    
]

for email in test_emails:
    result = validate_email(email)
    print(f"{email:20} -> {result}")

def calculate_monthly_revenue(daily_sales):
    """calculates total revenue from daily sales list."""
    print(f"\ndebug: received daily_sales = {daily_sales}")
    
    total = 0
    print(f"debug: starting total = {total}")
    
    for sale in daily_sales:
        total = total + sale
        print(f"debug: added ${sale}, total now = ${total}")
    
    print(f"debug: loop finished, final total = ${total}")
    return total
    
# test it
print("\n\n=== testing monthly revenue ===")

sales = [500, 600, 550]

result = calculate_monthly_revenue(sales)
print(f"sales for 3 days: {sales}")
print(f"total: ${sum(sales)}")
print(f"calculated monthly revenue: ${result}")
print(f"expected: $1650 (just sum of 3 days)")    

def calculate_monthly_revenue(daily_sales):
    """calculates total revenue from daily sales list."""
    total = 0
    for sale in daily_sales:
        total = total + sale
    return total


