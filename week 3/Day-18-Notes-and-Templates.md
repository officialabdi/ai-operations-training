# DAY 18: CUSTOM EXCEPTIONS & ERROR CLASSES
## AI Operations Training - Week 3, Day 4

---

## 🎯 WHAT YOU LEARNED TODAY

### Core Skills:
- ✅ Creating custom exception classes
- ✅ Raising custom exceptions
- ✅ Catching custom exceptions
- ✅ Exception hierarchies (parent/child)
- ✅ Generic vs specific exception catching
- ✅ Professional error naming conventions
- ✅ Descriptive error messages

### The Architecture "Why":
**Days 15-17 taught you:** Handle Python's built-in errors (ValueError, TypeError)  
**Day 18 teaches you:** CREATE YOUR OWN error types

**The Problem Day 18 Solves:**
- Generic errors are unclear ("ValueError" could be anything)
- Can't catch specific validation errors separately
- Error names don't document what went wrong
- Debugging is harder with generic errors
- Professional code uses descriptive custom errors

**Real Business Impact:**
- Clear error names = faster debugging
- Specific error types = better error handling
- Custom messages = easier troubleshooting
- Exception hierarchies = flexible error catching
- **Debugging time reduced by 40-60%**

---

## 🔑 THE KEY CONCEPT: Descriptive Error Types

### What Are Custom Exceptions?

**Custom exceptions = Error types YOU create for YOUR specific needs**

**Generic error (unprofessional):**
```python
if len(phone) != 10:
    raise ValueError("Invalid phone")  # Too generic!
```
**Problem:** ValueError could be ANYTHING (age, price, email, etc.)

**Custom error (professional):**
```python
if len(phone) != 10:
    raise InvalidPhoneError(f"Need 10 digits, got {len(phone)}")
```
**Better:**
- Error name says WHAT failed (phone validation)
- Message says WHY (wrong length)
- Can catch phone errors specifically
- Self-documenting code

---

### Why Create Custom Exceptions?

**1. Clarity**
```python
raise InvalidPhoneError("...")  # Clear: phone validation failed
raise ValueError("...")         # Unclear: what value?
```

**2. Specificity**
```python
try:
    validate_user(data)
except InvalidPhoneError:
    send_phone_help_message()  # Handle phone errors specifically
except InvalidEmailError:
    send_email_help_message()  # Handle email errors differently
```

**3. Documentation**
```python
def validate_phone(phone):
    """
    Validates phone number.
    
    Raises:
        InvalidPhoneError: If phone is not 10 digits
    """
```
Error types document what can go wrong!

**4. Professional Code**
- Shows expertise
- Industry standard
- Easier maintenance
- Better debugging

---

## 📚 CORE CONCEPTS

### Creating Custom Exception Classes

**Basic syntax:**
```python
class YourErrorName(Exception):
    """Description of when this error is raised"""
    pass
```

**Parts explained:**
- `class YourErrorName` → Name of your exception (PascalCase)
- `(Exception)` → Inherits from Python's base Exception class
- Docstring → Explains when this error occurs
- `pass` → Empty class body (uses default Exception behavior)

**Example:**
```python
class InvalidPhoneError(Exception):
    """Raised when phone number is invalid"""
    pass
```

**Now `InvalidPhoneError` is a new error type you can use!**

---

### Raising Custom Exceptions

**Syntax:**
```python
raise YourErrorName("Error message here")
```

**Example:**
```python
if len(phone) != 10:
    raise InvalidPhoneError(f"Phone must be 10 digits, got {len(phone)}")
```

**What happens:**
1. Python creates an InvalidPhoneError object
2. Attaches your message to it
3. Stops execution and looks for except block
4. If no except catches it, program crashes with your error

---

### Catching Custom Exceptions

**Syntax:**
```python
try:
    risky_operation()
except YourErrorName as e:
    handle_error(e)
```

**Example:**
```python
try:
    validate_phone("555-1234")
except InvalidPhoneError as e:
    print(f"Phone error: {e}")
```

**What happens:**
1. `try` block runs
2. If InvalidPhoneError is raised
3. `except` block catches it
4. Variable `e` contains the error object
5. Can access message with `str(e)` or just `e`

---

### Exception Hierarchies (Parent/Child)

**Create a parent exception:**
```python
class ValidationError(Exception):
    """Base class for all validation errors"""
    pass
```

**Create child exceptions that inherit from parent:**
```python
class InvalidPhoneError(ValidationError):
    """Raised when phone is invalid"""
    pass

class InvalidEmailError(ValidationError):
    """Raised when email is invalid"""
    pass

class InvalidAgeError(ValidationError):
    """Raised when age is invalid"""
    pass
```

**The hierarchy:**
```
Exception (Python's base)
    ↓
ValidationError (YOUR parent)
    ↓
    ├── InvalidPhoneError (child)
    ├── InvalidEmailError (child)
    └── InvalidAgeError (child)
```

**The power:** Catch ALL validation errors OR catch specific ones!

---

## 📚 CODE TEMPLATES

### TEMPLATE 1: Basic Custom Exception

```python
class InvalidPhoneError(Exception):
    """
    Raised when phone number validation fails.
    
    USE CASE: Phone validation in any system
    BUSINESS VALUE: Clear error identification
    
    Example:
        raise InvalidPhoneError("Phone must be 10 digits")
    """
    pass

def validate_phone(phone):
    """
    Validates phone number format.
    
    Parameters:
    - phone: Phone number to validate (str)
    
    Returns: Cleaned phone (str) with digits only
    
    Raises:
        InvalidPhoneError: If phone doesn't have 10 digits
    """
    # Clean phone - extract only digits
    digits = ""
    for char in phone:
        if char.isdigit():
            digits += char
    
    # Validate length - raise custom error if invalid
    if len(digits) != 10:
        raise InvalidPhoneError(f"Phone must be 10 digits, got {len(digits)}")
    
    return digits

# USAGE EXAMPLES:

# Valid phone - no error
try:
    result = validate_phone("555-123-4567")
    print(f"Success: {result}")  # Success: 5551234567
except InvalidPhoneError as e:
    print(f"Error: {e}")

# Invalid phone - raises InvalidPhoneError
try:
    result = validate_phone("555-1234")
    print(f"Success: {result}")
except InvalidPhoneError as e:
    print(f"Error: {e}")  # Error: Phone must be 10 digits, got 7
```

**Why this works:**
- Clear error name (InvalidPhoneError)
- Descriptive message (exact digit count)
- Can catch phone errors specifically
- Self-documenting code

---

### TEMPLATE 2: Multiple Custom Exceptions

```python
# Create multiple custom exception types
class InvalidEmailError(Exception):
    """Raised when email format is invalid"""
    pass

class InvalidPhoneError(Exception):
    """Raised when phone number is invalid"""
    pass

class InvalidAgeError(Exception):
    """Raised when age is out of range"""
    pass

class InvalidUsernameError(Exception):
    """Raised when username doesn't meet requirements"""
    pass

def register_user(email, phone, age, username):
    """
    Registers user with specific error types for each validation.
    
    USE CASE: User registration systems
    BUSINESS VALUE: Specific error handling per field
    
    Parameters:
    - email: User email (str)
    - phone: User phone (str)
    - age: User age (int)
    - username: Desired username (str)
    
    Returns: Success message (str)
    
    Raises:
        InvalidEmailError: If email missing @ or .
        InvalidPhoneError: If phone not 10 digits
        InvalidAgeError: If age not 13-120
        InvalidUsernameError: If username too short
    """
    # Validate email
    if "@" not in email or "." not in email:
        raise InvalidEmailError(f"Email '{email}' must contain @ and .")
    
    # Validate phone
    digits = ""
    for char in phone:
        if char.isdigit():
            digits += char
    if len(digits) != 10:
        raise InvalidPhoneError(f"Phone must be 10 digits, got {len(digits)}")
    
    # Validate age
    if not isinstance(age, int) or not (13 <= age <= 120):
        raise InvalidAgeError(f"Age must be 13-120, got {age}")
    
    # Validate username
    if len(username) < 3:
        raise InvalidUsernameError(f"Username must be at least 3 characters, got {len(username)}")
    
    return "Registration successful!"

# USAGE EXAMPLES:

# Test 1: All valid - success
try:
    result = register_user("user@email.com", "555-123-4567", 25, "john123")
    print(f"Test 1: {result}")
except (InvalidEmailError, InvalidPhoneError, InvalidAgeError, InvalidUsernameError) as e:
    print(f"Test 1 Error: {type(e).__name__}: {e}")
# Output: Test 1: Registration successful!

# Test 2: Invalid email - specific error
try:
    result = register_user("useremail.com", "555-123-4567", 25, "john123")
    print(f"Test 2: {result}")
except (InvalidEmailError, InvalidPhoneError, InvalidAgeError, InvalidUsernameError) as e:
    print(f"Test 2 Error: {type(e).__name__}: {e}")
# Output: Test 2 Error: InvalidEmailError: Email 'useremail.com' must contain @ and .

# Test 3: Invalid phone - specific error
try:
    result = register_user("user@email.com", "555-1234", 25, "john123")
    print(f"Test 3: {result}")
except (InvalidEmailError, InvalidPhoneError, InvalidAgeError, InvalidUsernameError) as e:
    print(f"Test 3 Error: {type(e).__name__}: {e}")
# Output: Test 3 Error: InvalidPhoneError: Phone must be 10 digits, got 7

# Test 4: Invalid age - specific error
try:
    result = register_user("user@email.com", "555-123-4567", 10, "john123")
    print(f"Test 4: {result}")
except (InvalidEmailError, InvalidPhoneError, InvalidAgeError, InvalidUsernameError) as e:
    print(f"Test 4 Error: {type(e).__name__}: {e}")
# Output: Test 4 Error: InvalidAgeError: Age must be 13-120, got 10

# Test 5: Invalid username - specific error
try:
    result = register_user("user@email.com", "555-123-4567", 25, "ab")
    print(f"Test 5: {result}")
except (InvalidEmailError, InvalidPhoneError, InvalidAgeError, InvalidUsernameError) as e:
    print(f"Test 5 Error: {type(e).__name__}: {e}")
# Output: Test 5 Error: InvalidUsernameError: Username must be at least 3 characters, got 2
```

**Why multiple exceptions:**
- Each validation gets its own error type
- Error name tells you which field failed
- Can handle each error differently
- Clear debugging (know exactly what failed)

---

### TEMPLATE 3: Exception Hierarchies (Parent/Child)

```python
# Parent exception - base for all validation errors
class ValidationError(Exception):
    """
    Base class for all validation errors.
    
    USE CASE: When you want to catch ALL validation errors together
    BUSINESS VALUE: Flexible error handling
    
    This is the PARENT - all validation errors inherit from this
    """
    pass

# Child exceptions - specific validation errors
class InvalidPhoneError(ValidationError):
    """Raised when phone number is invalid"""
    pass

class InvalidEmailError(ValidationError):
    """Raised when email format is invalid"""
    pass

class InvalidAgeError(ValidationError):
    """Raised when age is out of range"""
    pass

def validate_user(email, phone, age):
    """
    Validates user data with hierarchical exceptions.
    
    USE CASE: User validation with flexible error catching
    BUSINESS VALUE: Can catch all errors OR specific errors
    
    The hierarchy:
        ValidationError (parent)
            ├── InvalidPhoneError
            ├── InvalidEmailError
            └── InvalidAgeError
    
    Parameters:
    - email: User email (str)
    - phone: User phone (str)
    - age: User age (int)
    
    Returns: "Valid!" if all checks pass
    
    Raises:
        InvalidEmailError: If email missing @
        InvalidPhoneError: If phone not 10 digits
        InvalidAgeError: If age not 13-120
    """
    # Validate email
    if "@" not in email:
        raise InvalidEmailError("Email must contain @")
    
    # Validate phone
    digits = "".join(char for char in phone if char.isdigit())
    if len(digits) != 10:
        raise InvalidPhoneError(f"Phone must be 10 digits, got {len(digits)}")
    
    # Validate age
    if not (13 <= age <= 120):
        raise InvalidAgeError(f"Age must be 13-120, got {age}")
    
    return "Valid!"

# USAGE PATTERN 1: Catch ALL validation errors together
print("=== PATTERN 1: Catch ALL validation errors ===")

try:
    validate_user("user@email.com", "555-123-4567", 25)
    print("Success: All valid")
except ValidationError as e:
    print(f"Caught ANY validation error: {type(e).__name__}: {e}")
# Output: Success: All valid

try:
    validate_user("useremail.com", "555-123-4567", 25)
    print("Success: All valid")
except ValidationError as e:
    print(f"Caught ANY validation error: {type(e).__name__}: {e}")
# Output: Caught ANY validation error: InvalidEmailError: Email must contain @

try:
    validate_user("user@email.com", "555-1234", 25)
    print("Success: All valid")
except ValidationError as e:
    print(f"Caught ANY validation error: {type(e).__name__}: {e}")
# Output: Caught ANY validation error: InvalidPhoneError: Phone must be 10 digits, got 7

# USAGE PATTERN 2: Catch SPECIFIC errors separately
print("\n=== PATTERN 2: Catch SPECIFIC errors ===")

try:
    validate_user("useremail.com", "555-123-4567", 25)
except InvalidEmailError:
    print("Handle email error specifically")
except InvalidPhoneError:
    print("Handle phone error specifically")
except InvalidAgeError:
    print("Handle age error specifically")
# Output: Handle email error specifically

try:
    validate_user("user@email.com", "555-1234", 25)
except InvalidEmailError:
    print("Handle email error specifically")
except InvalidPhoneError:
    print("Handle phone error specifically")
except InvalidAgeError:
    print("Handle age error specifically")
# Output: Handle phone error specifically
```

**How hierarchies work:**

**Catching with parent:**
```python
except ValidationError as e:
    # Catches ALL child exceptions:
    # - InvalidPhoneError
    # - InvalidEmailError
    # - InvalidAgeError
```

**Catching with child:**
```python
except InvalidPhoneError:
    # ONLY catches phone errors
    # Email and age errors NOT caught here
```

**When to use each:**
- **Parent (ValidationError):** Same handling for all validation errors
- **Child (InvalidPhoneError):** Different handling per error type

---

### TEMPLATE 4: Real-World Application (Email System from Day 14)

```python
# Custom exceptions for email automation system
class EmailSystemError(Exception):
    """Base exception for email system errors"""
    pass

class InvalidCustomerTierError(EmailSystemError):
    """Raised when customer tier is invalid"""
    pass

class InvalidEmailTypeError(EmailSystemError):
    """Raised when email type is invalid"""
    pass

class InvalidTokenCountError(EmailSystemError):
    """Raised when token count is invalid"""
    pass

def process_email_request(customer_tier, email_type, tokens_used):
    """
    Processes email request with custom error handling.
    
    USE CASE: Production email automation (Day 14 system)
    BUSINESS VALUE: Clear error messages for debugging
    
    Parameters:
    - customer_tier: "VIP" or "standard" (str)
    - email_type: Email category (str)
    - tokens_used: Number of tokens (int or str)
    
    Returns: Processing result (dict)
    
    Raises:
        InvalidCustomerTierError: If tier not VIP or standard
        InvalidEmailTypeError: If email_type not string
        InvalidTokenCountError: If tokens invalid
    """
    # Validate customer tier
    valid_tiers = ["VIP", "standard"]
    if customer_tier not in valid_tiers:
        raise InvalidCustomerTierError(
            f"Customer tier must be {valid_tiers}, got '{customer_tier}'"
        )
    
    # Validate email type
    if not isinstance(email_type, str):
        raise InvalidEmailTypeError(
            f"Email type must be string, got {type(email_type).__name__}"
        )
    
    # Validate and clean tokens
    if isinstance(tokens_used, str):
        if not tokens_used.isdigit():
            raise InvalidTokenCountError(
                f"Token count must be numeric, got '{tokens_used}'"
            )
        tokens_used = int(tokens_used)
    
    if not isinstance(tokens_used, int) or tokens_used < 0:
        raise InvalidTokenCountError(
            f"Token count must be positive integer, got {tokens_used}"
        )
    
    # Process email (all validations passed)
    cost = (tokens_used / 1000) * 0.003
    return {
        "tier": customer_tier,
        "type": email_type,
        "tokens": tokens_used,
        "cost": cost,
        "status": "success"
    }

# USAGE EXAMPLES:

# Valid request - success
try:
    result = process_email_request("VIP", "complaint", 250)
    print(f"Success: {result}")
except EmailSystemError as e:
    print(f"Error: {type(e).__name__}: {e}")
# Output: Success: {'tier': 'VIP', 'type': 'complaint', 'tokens': 250, 'cost': 0.00075, 'status': 'success'}

# Invalid tier - specific error
try:
    result = process_email_request("VIIP", "complaint", 250)
    print(f"Success: {result}")
except EmailSystemError as e:
    print(f"Error: {type(e).__name__}: {e}")
# Output: Error: InvalidCustomerTierError: Customer tier must be ['VIP', 'standard'], got 'VIIP'

# Invalid tokens - specific error
try:
    result = process_email_request("VIP", "complaint", "250 tokens")
    print(f"Success: {result}")
except EmailSystemError as e:
    print(f"Error: {type(e).__name__}: {e}")
# Output: Error: InvalidTokenCountError: Token count must be numeric, got '250 tokens'
```

**Real-world benefits:**
- Client sees clear error messages
- Developer knows exactly what failed
- System doesn't crash on bad input
- Easy to debug production issues

---

## 🔑 KEY CONCEPTS

### When to Create Custom Exceptions

**✅ CREATE custom exceptions when:**

**1. Domain-specific validations**
```python
class InvalidPhoneError(Exception):  # Phone is domain-specific
    pass
```

**2. Multiple related errors**
```python
class ValidationError(Exception):  # Parent
    pass
class InvalidEmailError(ValidationError):  # Child 1
    pass
class InvalidPhoneError(ValidationError):  # Child 2
    pass
```

**3. Need specific error handling**
```python
try:
    validate_user(data)
except InvalidPhoneError:
    show_phone_help()  # Phone-specific help
except InvalidEmailError:
    show_email_help()  # Email-specific help
```

**4. Professional APIs/libraries**
```python
class DatabaseError(Exception):  # Library-specific errors
    pass
class ConnectionError(DatabaseError):
    pass
class QueryError(DatabaseError):
    pass
```

---

**❌ DON'T create custom exceptions when:**

**1. Built-in exception is clear enough**
```python
# ❌ Don't create custom exception
class NotANumberError(Exception):
    pass

# ✅ Use built-in
raise ValueError("Must be a number")
```

**2. One-time use**
```python
# ❌ Overkill for one function
class TemporaryError(Exception):
    pass

# ✅ Use generic Exception
raise Exception("Temporary issue")
```

**3. Generic programming errors**
```python
# ❌ Don't create custom for programming errors
class WrongTypeError(Exception):
    pass

# ✅ Use built-in TypeError
raise TypeError("Expected int, got str")
```

---

### Exception Naming Conventions

**Follow Python conventions:**

**1. Use PascalCase (CapitalizeEachWord)**
```python
class InvalidPhoneError(Exception):  # ✅ Correct
class invalidphoneerror(Exception):  # ❌ Wrong
class invalid_phone_error(Exception):  # ❌ Wrong
```

**2. End with "Error"**
```python
class InvalidPhoneError(Exception):  # ✅ Correct
class InvalidPhone(Exception):       # ❌ Missing Error
```

**3. Be descriptive**
```python
class InvalidPhoneError(Exception):  # ✅ Clear
class PhoneError(Exception):         # ⚠️ Vague
class Error(Exception):              # ❌ Too generic
```

**4. Use proper hierarchy names**
```python
class ValidationError(Exception):    # ✅ Parent
class InvalidPhoneError(ValidationError):  # ✅ Child
```

---

### Generic vs Specific Catching

**Pattern 1: Catch ALL related errors (generic)**
```python
try:
    validate_user(data)
except ValidationError as e:  # Catches ALL validation errors
    log_error(e)
    return "Validation failed"
```

**Use when:**
- Same handling for all errors
- Logging all validation failures
- Generic error message to user

---

**Pattern 2: Catch SPECIFIC errors (specific)**
```python
try:
    validate_user(data)
except InvalidPhoneError:
    return "Phone format incorrect. Use: 555-123-4567"
except InvalidEmailError:
    return "Email must contain @ and ."
except InvalidAgeError:
    return "Must be 13 or older"
```

**Use when:**
- Different handling per error
- Specific help messages
- Different logging per error type

---

**Pattern 3: Combination (best of both)**
```python
try:
    validate_user(data)
except InvalidPhoneError:
    # Specific handling for phone
    log_phone_error()
    return "Phone error"
except InvalidEmailError:
    # Specific handling for email
    log_email_error()
    return "Email error"
except ValidationError:
    # Generic catch for any other validation error
    log_generic_error()
    return "Validation error"
```

**Use when:**
- Need specific handling for some errors
- Generic handling for others
- Maximum flexibility

---

## 🔧 COMMON ERRORS AND FIXES

### Error 1: Not Inheriting from Exception
**Symptom:** Custom exception doesn't work
```python
class InvalidPhoneError:  # ❌ Missing (Exception)
    pass
```

**Fix:** Inherit from Exception
```python
class InvalidPhoneError(Exception):  # ✅ Correct
    pass
```

---

### Error 2: Using Lowercase Class Names
**Symptom:** Works but unprofessional
```python
class invalidphoneerror(Exception):  # ❌ Lowercase
    pass
```

**Fix:** Use PascalCase
```python
class InvalidPhoneError(Exception):  # ✅ PascalCase
    pass
```

---

### Error 3: Generic Error Messages
**Symptom:** Hard to debug
```python
raise InvalidPhoneError("Invalid")  # ❌ Not helpful
```

**Fix:** Descriptive messages
```python
raise InvalidPhoneError(f"Phone must be 10 digits, got {len(phone)}")  # ✅ Clear
```

---

### Error 4: Wrong Parent in Hierarchy
**Symptom:** Parent catch doesn't work
```python
class ValidationError(Exception):
    pass

class InvalidPhoneError(Exception):  # ❌ Should inherit from ValidationError
    pass

try:
    raise InvalidPhoneError("...")
except ValidationError:
    # Never caught! InvalidPhoneError doesn't inherit from ValidationError
    pass
```

**Fix:** Correct inheritance
```python
class ValidationError(Exception):
    pass

class InvalidPhoneError(ValidationError):  # ✅ Inherits from parent
    pass

try:
    raise InvalidPhoneError("...")
except ValidationError:
    # Now it catches! ✅
    pass
```

---

### Error 5: Too Many Custom Exceptions
**Symptom:** Code cluttered with exception classes
```python
class InvalidPhoneError(Exception): pass
class InvalidPhone2Error(Exception): pass
class PhoneError(Exception): pass
class BadPhoneError(Exception): pass
# ❌ Too many similar exceptions!
```

**Fix:** One exception per concept
```python
class InvalidPhoneError(Exception):  # ✅ One phone exception
    pass
```

---

## 💰 BUSINESS VALUE & ROI

### Scenario: Production API Debugging

**Client:** SaaS API with 10,000 requests/day

**Without Custom Exceptions:**
```python
def process_request(data):
    if not valid(data):
        raise ValueError("Invalid")  # Generic error
```

**Problems:**
- "ValueError: Invalid" - what's invalid?
- Check logs: 50 ValueErrors/day
- Which ones are phone? Email? Age?
- Developer spends 2 hours/day debugging
- **Cost:** 2 hours × $75/hour × 20 days = $3,000/month

---

**With Custom Exceptions:**
```python
def process_request(data):
    if not valid_phone(data.phone):
        raise InvalidPhoneError(f"Phone invalid: {data.phone}")
    if not valid_email(data.email):
        raise InvalidEmailError(f"Email invalid: {data.email}")
```

**Results:**
- Clear error names in logs
- "InvalidPhoneError: Phone invalid: 555-123" → immediately know what failed
- Can filter logs by error type
- Can alert on specific errors
- Developer debugging: 20 min/day (down from 2 hours)
- **Savings:** 1.67 hours × $75/hour × 20 days = $2,500/month

**ROI:**
- Implementation: 4 hours ($300)
- Monthly savings: $2,500
- **Return:** 733% monthly

---

### Scenario: User Registration System

**Client:** E-commerce with 500 registrations/day

**Without Custom Exceptions:**
```python
def register(email, phone, age):
    if bad_data:
        return "Error: Invalid input"
```

**Problems:**
- Generic error message
- User doesn't know what to fix
- Support gets 50 tickets/day asking "what's wrong?"
- **Cost:** 2 hours support/day × $30/hour = $60/day = $1,800/month

---

**With Custom Exceptions:**
```python
def register(email, phone, age):
    try:
        validate(email, phone, age)
    except InvalidEmailError as e:
        return f"Email error: {e}"
    except InvalidPhoneError as e:
        return f"Phone error: {e}"
    except InvalidAgeError as e:
        return f"Age error: {e}"
```

**Results:**
- Specific error messages: "Phone error: Must be 10 digits"
- Users fix their own errors
- Support tickets: 10/day (down from 50)
- **Savings:** 1.33 hours/day × $30/hour × 30 days = $1,200/month

**ROI:**
- Implementation: 2 hours ($300)
- Monthly savings: $1,200
- **Return:** 300% monthly

---

## 🎯 PRACTICAL EXERCISES

### Exercise 1: Create Custom Exceptions
```python
"""
Create custom exceptions for a banking system:
1. InsufficientFundsError - not enough balance
2. InvalidAccountError - account doesn't exist
3. InvalidAmountError - negative or zero amount
"""
# Your code here
```

---

### Exercise 2: Use Exception Hierarchy
```python
"""
Create a hierarchy:
- PaymentError (parent)
  - InvalidCardError (child)
  - ExpiredCardError (child)
  - InsufficientFundsError (child)

Then write a process_payment() function that raises these errors
"""
# Your code here
```

---

### Exercise 3: Apply to Day 14 System
```python
"""
Add custom exceptions to your Day 14 email system:
1. InvalidCustomerTierError
2. InvalidEmailTypeError
3. InvalidTokenCountError

Update route_email_request() to raise these
"""
# Your code here
```

---

## 🔮 DAY 19 PREVIEW: LOGGING

**Tomorrow you'll learn:**
- Logging vs printing
- Log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Writing logs to files
- Professional error tracking

**Example:**
```python
import logging

logging.info("User registration started")
logging.error("Phone validation failed", exc_info=True)
logging.warning("Token count high: 5000")
```

**Why it matters:**
- `print()` disappears after running
- Logs persist in files
- Can filter by severity
- Essential for production systems
- Track errors over time

**Connects to Day 18:**
- Custom exceptions → caught and logged
- Error messages → written to log files
- Professional error tracking system

---

## 💾 FILE ORGANIZATION

**Your Day 18 Structure:**
```
AI-Operations-Training/
├── Day-15/
│   ├── day15_error_handling.py
│   └── Day-15-Notes.md
├── Day-16/
│   ├── day16_input_validation.py
│   └── Day-16-Notes.md
├── Day-17/
│   ├── day17_advanced_validation.py
│   └── Day-17-Notes.md
├── Day-18/
│   ├── day18_custom_exceptions.py (all exception examples)
│   └── Day-18-Notes.md (this file)
└── Week-3-Video/
    └── watch-after-day-21.txt (Corey Schafer reminder)
```

---

## 🏆 DAY 18 ACHIEVEMENTS

- [x] Created custom exception classes
- [x] Raised custom exceptions with descriptive messages
- [x] Caught custom exceptions
- [x] Built exception hierarchies (parent/child)
- [x] Used generic catching (parent)
- [x] Used specific catching (child)
- [x] Applied to real-world validation
- [x] Understood naming conventions

**Grade: A+**

---

## 📝 KEY TAKEAWAYS

1. **Custom exceptions = descriptive error types** - Name tells you what failed
2. **Inherit from Exception** - class YourError(Exception)
3. **Use PascalCase** - InvalidPhoneError not invalidphoneerror
4. **Descriptive messages** - Include details (what, why, values)
5. **Hierarchies = flexibility** - Catch all OR catch specific
6. **Parent catches children** - except ValidationError catches InvalidPhoneError
7. **Professional code uses custom exceptions** - Industry standard

---

## 🎓 THE SIMPLE SUMMARY

### **Generic Errors (Unprofessional):**
```python
raise ValueError("Invalid")
# What's invalid? Who knows! 🤷
```

### **Custom Errors (Professional):**
```python
raise InvalidPhoneError("Phone must be 10 digits, got 7")
# Immediately clear what failed and why! ✓
```

### **Exception Hierarchy:**
```
ValidationError (parent)
    ├── InvalidPhoneError (child)
    ├── InvalidEmailError (child)
    └── InvalidAgeError (child)

Catch parent → Gets ALL validation errors
Catch child → Gets ONLY that specific error
```

---

## 🔧 TROUBLESHOOTING QUICK REFERENCE

| Problem | Cause | Fix |
|---------|-------|-----|
| Exception doesn't work | Not inheriting from Exception | Add (Exception) |
| Parent doesn't catch child | Child doesn't inherit from parent | Use (ParentError) |
| Error message unclear | Generic message | Add details (what, why, values) |
| Unprofessional naming | lowercase | Use PascalCase |
| Can't catch specific error | Using generic Exception | Create custom exception |

---

## 📞 DECISION GUIDE

**Should I create a custom exception?**

**YES if:**
- ✅ Domain-specific error (InvalidPhoneError)
- ✅ Need specific error handling
- ✅ Building library/API
- ✅ Multiple related errors

**NO if:**
- ❌ Built-in is clear enough (ValueError)
- ❌ One-time use
- ❌ Generic programming error (TypeError)

**Use hierarchy if:**
- ✅ Multiple related errors
- ✅ Want to catch all OR specific
- ✅ Building complex system

---

## 🎯 WEEK 3 PROGRESS

**Completed:**
- ✅ Day 15 (Error Handling - try/except)
- ✅ Day 16 (Input Validation - isinstance, isdigit)
- ✅ Day 17 (Data Sanitization - cleaning messy input)
- ✅ Day 18 (Custom Exceptions - your own error types)

**Remaining in Week 3:**
- Day 19: Logging
- Day 20: Debugging Techniques
- Day 21: Week 3 Integration

**After Day 21:** Watch Corey Schafer error handling video

---

**Created:** Day 18 of AI Operations Training  
**Your Progress:** Week 3, Day 4 (Day 18/168 total)  
**Next Session:** Day 19 - Logging

**You're building professional, enterprise-grade error handling now.** 💪🏆
