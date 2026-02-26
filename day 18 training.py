# Custom exception classes (PascalCase - Python convention)
class InvalidPhoneError(Exception):
    """Raised when phone number is invalid"""
    pass

class InvalidEmailError(Exception):
    """Raised when email format is invalid"""
    pass

class InvalidAgeError(Exception):
    """Raised when age is out of range"""
    pass

class InvalidUsernameError(Exception):
    """Raised when username doesn't meet requirements"""
    pass

# Functions using the exceptions
def validate_phone(phone):
    """Validates phone number, raises custom error if invalid"""
    digits = ""
    for char in phone:
        if char.isdigit():
            digits += char
    if len(digits) != 10:
        raise InvalidPhoneError(f"Phone must be 10 digits, got {len(digits)}")
    return digits

def register_user(email, phone, age, username):
    """Registers user with specific error types for each validation."""
    if "@" not in email or "." not in email:
        raise InvalidEmailError(f"Email '{email}' must contain @ and .")
    
    digits = ""
    for char in phone:
        if char.isdigit():
            digits += char
    if len(digits) != 10:
        raise InvalidPhoneError(f"Phone must be 10 digits, got {len(digits)}")
    
    if not isinstance(age, int) or not (13 <= age <= 120):
        raise InvalidAgeError(f"Age must be 13-120, got {age}")
    
    if len(username) < 3:
        raise InvalidUsernameError(f"Username must be at least 3 characters, got {len(username)}")
    
    return "Registration successful!"

# Test validate_phone
try:
    result = validate_phone("555-123-4567")
    print(f"Success: {result}")
except InvalidPhoneError as e:
    print(f"Caught InvalidPhoneError: {e}")

try:
    result = validate_phone("555-1234")
    print(f"Success: {result}")
except InvalidPhoneError as e:
    print(f"Caught InvalidPhoneError: {e}")

# Test register_user
try:
    result = register_user("user@email.com", "555-123-4567", 25, "john123")
    print(f"Test 1: {result}")
except (InvalidEmailError, InvalidPhoneError, InvalidAgeError, InvalidUsernameError) as e:
    print(f"Test 1 Error: {type(e).__name__}: {e}")

try:
    result = register_user("useremail.com", "555-123-4567", 25, "john123")
    print(f"Test 2: {result}")
except (InvalidEmailError, InvalidPhoneError, InvalidAgeError, InvalidUsernameError) as e:
    print(f"Test 2 Error: {type(e).__name__}: {e}")

try:
    result = register_user("user@email.com", "555-1234", 25, "john123")
    print(f"Test 3: {result}")
except (InvalidEmailError, InvalidPhoneError, InvalidAgeError, InvalidUsernameError) as e:
    print(f"Test 3 Error: {type(e).__name__}: {e}")

try:
    result = register_user("user@email.com", "555-123-4567", 10, "john123")
    print(f"Test 4: {result}")
except (InvalidEmailError, InvalidPhoneError, InvalidAgeError, InvalidUsernameError) as e:
    print(f"Test 4 Error: {type(e).__name__}: {e}")

try:
    result = register_user("user@email.com", "555-123-4567", 25, "ab")
    print(f"Test 5: {result}")
except (InvalidEmailError, InvalidPhoneError, InvalidAgeError, InvalidUsernameError) as e:
    print(f"Test 5 Error: {type(e).__name__}: {e}")

class validationerror(Exception):
    """base class for all validation errors"""
    pass

class invalidphoneerrorv2(validationerror):
    """raised when phone number is invalid"""
    pass
class invalidemailerrorv2(validationerror):
    """raised when email format is invalid"""
    pass
class invalidageerrorv2(validationerror):
    """raised when age is out of range"""
    pass

def validate_user_v2(email, phone, age):
    """validates user data with hierarchical exceptions"""
    if "@" not in email:
        raise invalidemailerrorv2("email must contain @")
    
    digits = "".join(char for char in phone if char.isdigit())
    if len(digits) != 10:
        raise invalidphoneerrorv2(f"phone must be 10 digits, got {len(digits)}")
    
    if not (13 <= age <= 120):
        raise invalidageerrorv2(f"age must be 13-120, got {age}")
    
    return "valid"

print("=== PATTERN 1: Catch ALL validation errors together ===")
try:
    validate_user_v2("user@email.com", "555-123-4567", 25)
    print("Success: All valid")
except validationerror as e:
    print(f"Caught ANY validation error: {type(e).__name__}: {e}")

try:
    validate_user_v2("useremail.com", "555-123-4567", 25)
    print("Success: All valid")
except validationerror as e:
    print(f"Caught ANY validation error: {type(e).__name__}: {e}")

try:
    validate_user_v2("user@email.com", "555-1234", 25)
    print("Success: All valid")
except validationerror as e:
    print(f"Caught ANY validation error: {type(e).__name__}: {e}")

print("\n=== PATTERN 2: Catch SPECIFIC errors separately ===")
try:
    validate_user_v2("useremail.com", "555-123-4567", 25)
except invalidemailerrorv2:
    print("Handle email error specifically")
except invalidphoneerrorv2:
    print("Handle phone error specifically")
except invalidageerrorv2:
    print("Handle age error specifically")

try:
    validate_user_v2("user@email.com", "555-1234", 25)
except invalidemailerrorv2:
    print("Handle email error specifically")
except invalidphoneerrorv2:
    print("Handle phone error specifically")
except invalidageerrorv2:
    print("Handle age error specifically")