def check_type(value):
    print(f"value: {value}")
    print(f"is it an int? {isinstance(value, int)}")
    print(f"is it a str?{isinstance(value, str)}")
    print(f"is it a float? {isinstance(value, float)}")
    print("-"*30)

check_type(42)
check_type("42")
check_type(42.5)

def safe_multiply(value ,multiplier):
    if isinstance(value, (int, float)) and isinstance(multiplier, (int, float)):
        result = value * multiplier 
        return result
    else: 
        return "error: both inputs must be numbers"
    

print(safe_multiply(10, 5))


print(safe_multiply("10", 5))


print(safe_multiply("10", "5"))


print(safe_multiply(10.5, 2))    

def professional_divide(a, b):
    """
    professional_division with validation + error handling.
    layer 1: validate types
    layer 2: catch unexpected errors
    """
    if not isinstance(a, (int, float)):
        return "error: first number must be int or float"
    if not isinstance(b, (int, float)):
        return "error: second number must be int or float"
    try: 
        result = a / b 
        return result 
    except ZeroDivisionError:
        return "error: canoot divide by zero"
    
   
print(professional_divide(10, 2))


print(professional_divide("10", 2))


print(professional_divide(10, 0))


print(professional_divide("10", "2"))

def validate_string_input(user_input):
    """
    shows different string validation methods.
    """
    print(f"Input: '{user_input}'")
    print(f"  .isdigit(): {user_input.isdigit()}")    
    print(f"  .isalpha(): {user_input.isalpha()}")     
    print(f"  .isalnum(): {user_input.isalnum()}")     
    print(f"  .isnumeric(): {user_input.isnumeric()}") 
    print("-" * 40)


validate_string_input("123")
validate_string_input("abc")
validate_string_input("abc123")
validate_string_input("12.5")

def get_valid_age(user_input):
    """validates age input using string methods + isinstance.
    real-world example or proper validation.
    """
    if not isinstance(user_input, str):
        if isinstance(user_input, int):
            if 0 <= user_input <=120:
                return user_input
            else:
                return "error: age must be 0=120"
        return "error: invalid input type"
    if not user_input.isdigit():
        return "error: age must be a number (no decimals or letters)"
    age = int(user_input)
    if not (0 <= age <= 120):
        return "error: age must be between 0 and 120"
    return age
    
   
print(get_valid_age("25"))


print(get_valid_age(30))


print(get_valid_age("25.5"))


print(get_valid_age("twenty"))


print(get_valid_age("150"))

print(get_valid_age("-5"))

def bulletproof_track_email(customer_tier, email_type, tokens_used):
    """example shwoing validation + error handling together."""
    if not isinstance(customer_tier, str):
        return "error: customer_tier must be a string"
    if not customer_tier in ["vip", "standard"]:
        return f"error: customer_tier must be a 'vip' or 'standard', got '{customer_tier}'"
    if not isinstance(email_type, str):
        return "error: email_type must be a string"
    if isinstance(tokens_used, str):
        if not tokens_used.isdigit():
            return "error: tokens_used must be a number (no decimals or letters)"
        tokens_used = int(tokens_used,)
    elif not isinstance(tokens_used, int):    
        return "error: tokens_used must be int or numeric string"
    try:
        cost = (tokens_used / 1000)* 0.003
        print(f"logged: {customer_tier} {email_type} - ${cost:.4f}")
        return True
    except Exception as e:
        print(f"unexpected error: {e}")
        return False
    
   
print(bulletproof_track_email("vip", "complaint", 250))

print(bulletproof_track_email("standard", "support", "180"))

print(bulletproof_track_email("viip", "complaint", 250))

print(bulletproof_track_email("vip", "complaint", "250 tokens"))

print(bulletproof_track_email(123, "complaint", 250))