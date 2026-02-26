def demonstrate_cleaning(messy_input):
    print(f"orginal: '{messy_input}")
    print(f"   .strip(): '{messy_input.strip()}")
    print(f"   .lower(): '{messy_input.lower()}")
    print(f"   .upper(): '{messy_input.upper()}")
    print(f"   .replace(' ', ''): '{messy_input.replace(' ', '')}")
    print("-" * 50)


demonstrate_cleaning("  USER@EMAIL.COM  ")


demonstrate_cleaning("  john  smith  ")


demonstrate_cleaning("JoHn_SmItH_123")    

def clean_email(messy_email):
    cleaned = messy_email.strip()
    cleaned = cleaned.lower()
    cleaned = cleaned.replace(" ", "")
    return cleaned


print(clean_email("  USER@EMAIL.COM  "))


print(clean_email("user @ email . com"))


print(clean_email("user@email.com"))

def clean_phone_number(messy_phone):
    cleaned = messy_phone.strip()
    cleaned = cleaned.replace("(", "")
    cleaned = cleaned.replace(")", "")
    cleaned = cleaned.replace("-", "")
    cleaned = cleaned.replace(".", "")
    cleaned = cleaned.replace(" ", "")
    return cleaned

print(clean_phone_number("(555) 123-4567"))

print(clean_phone_number("555.123.4567"))


print(clean_phone_number("555 123 4567"))


print(clean_phone_number("5551234567"))


print(clean_phone_number("+1 (555) 123-4567"))

def clean_phone_advanced(messy_phone):
    digits_only = ""
    for character in messy_phone:
        if character.isdigit():
            digits_only += character

    return digits_only        


print(clean_phone_advanced("+1 (555) 123-4567"))
print(clean_phone_advanced("555-abc-1234")) 
print(clean_phone_advanced("Call me at 5551234567 please"))

def validate_phone_number(messy_phone):
    digits_only = ""
    for char in messy_phone:
        if char.isdigit():
            digits_only += char

    if len(digits_only) == 10:
        return f"valid: {digits_only}"
    elif len(digits_only) == 11 and digits_only[0] == "1":
        return f"valid: {digits_only[1:]}"
    else:
        return f"error: need 10 digits, got {len(digits_only)}"
    
print(validate_phone_number("(555) 123-4567"))


print(validate_phone_number("+1 (555) 123-4567"))

print(validate_phone_number("555-1234"))


print(validate_phone_number("555-123-4567-8900"))


print(validate_phone_number("555-abc-1234"))

import re 
def validate_email_basic(email):
    email = email.strip().lower()
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return f"valid: {email}"
    else:
        return f"invalid: {email}"
    
    
print(validate_email_basic("user@email.com"))


print(validate_email_basic("john.doe@company.co.uk"))


print(validate_email_basic("useremail.com"))


print(validate_email_basic("user@"))


print(validate_email_basic("  USER@EMAIL.COM  ")) 

def process_user_registration(email, phone, age):
    clean_email = email.strip().lower().replace(" ", "")
    if "@" not in clean_email or "." not in clean_email:
        return "error: invalid email format"
    clean_phone = ""
    for char in phone:
        if char.isdigit():
            clean_phone += char
    if len(clean_phone) == 11 and clean_phone[0] == "1":
        clean_phone = clean_phone[1:]
    if len(clean_phone) != 10:
            return f"error: phone must be 10 digits, got {len(clean_phone)}"
    if isinstance(age, str):
        age = age.strip()
        if not age.isdigit():
            return "error: age must be a number"
        age = int(age)
    if not isinstance(age, int) or not (13 <= age <= 120):
        return "error: age must be 13-120"
    return {
        "email": clean_email,
        "phone": clean_phone,
        "age": age,
        "status": "success"
    }

print(process_user_registration(
    "  USER@EMAIL.COM  ",
    "(555) 123-4567",
    "25"
))

print(process_user_registration(
    "john@company.com",
    "+1-555-123-4567",
    30
))


print(process_user_registration(
    "useremail.com",
    "5551234567",
    25
))


print(process_user_registration(
    "user@email.com",
    "555-1234",
    25
))


print(process_user_registration(
    "user@email.com",
    "5551234567",
    10
))


print(process_user_registration(
    "bad-email",
    "123",
    25
))