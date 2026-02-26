# DAY 16: INPUT VALIDATION & TYPE CHECKING
## AI Operations Training - Week 3, Day 2

---

## 🎯 WHAT YOU LEARNED TODAY

### Core Skills:
- ✅ Type checking with isinstance()
- ✅ String validation methods (.isdigit(), .isalpha(), etc.)
- ✅ Defense in depth (validation + error handling)
- ✅ Input sanitization
- ✅ Range validation
- ✅ Professional input handling

### The Architecture "Why":
**Day 15 taught you:** How to CATCH errors (reactive)  
**Day 16 teaches you:** How to PREVENT errors (proactive)

**The Problem Day 16 Solves:**
- Day 15 catches errors AFTER they happen (inefficient)
- Better to CHECK data BEFORE using it (prevent errors)
- Professional code validates input at boundaries
- Defense in depth: validation + error handling together
- One layer catches what the other misses

**Real Business Impact:**
- Errors prevented = faster performance
- Clear error messages = better UX
- Invalid data stopped at entry = cleaner system
- Defense in depth = bulletproof code
- **Error reduction: 70-90% through validation**

---

## 🔑 THE KEY CONCEPT: Defense in Depth

### **Two-Layer Security Model:**

**Layer 1: Validation (Proactive - Prevent)**
```python
if isinstance(value, int):
    # Safe to use as int
else:
    return "Error: Must be a number"
```

**Layer 2: Error Handling (Reactive - Catch)**
```python
try:
    process(value)
except Exception:
    return "Error: Processing failed"
```

**The Analogy:**
- **Validation** = Lock your door (prevent break-ins)
- **Error handling** = Home alarm (catch if they still get in)
- **Use BOTH** = Maximum security

**Why both matter:**
- Validation stops obvious errors (fast)
- Error handling catches unexpected errors (safety net)
- Together = bulletproof code

---

## 📚 CORE CONCEPTS

### What is isinstance()?

**isinstance() checks if a variable is a specific type.**

**Syntax:**
```python
isinstance(variable, type)
```

**Returns:** True or False

**Examples:**
```python
isinstance(42, int)           # True
isinstance("42", int)         # False
isinstance("42", str)         # True
isinstance(42.5, float)       # True
isinstance(42, (int, float))  # True - checks EITHER type
```

**Why this matters:**
- 42 and "42" LOOK the same to humans
- But Python treats them COMPLETELY differently
- isinstance() tells you which is which BEFORE you use it
- Prevents type errors before they happen

---

### String Validation Methods

**Python strings have built-in validation:**

| Method | What it checks | Example True | Example False |
|--------|---------------|--------------|---------------|
| `.isdigit()` | Only digits (0-9) | "123" | "12.5", "abc" |
| `.isalpha()` | Only letters (a-z, A-Z) | "abc" | "abc123", "12" |
| `.isalnum()` | Letters OR digits | "abc123" | "abc 123", "12.5" |
| `.isnumeric()` | Numeric characters | "123" | "12.5", "abc" |

**Key insights:**
- `.isdigit()` returns False for decimals ("12.5")
- `.isdigit()` returns False for negatives ("-5")
- All methods return False for strings with spaces
- All methods return False for empty strings

**Visual comparison:**
```python
Input: "123"
  .isdigit(): True   ✓
  .isalpha(): False
  .isalnum(): True   ✓
  .isnumeric(): True ✓

Input: "abc"
  .isdigit(): False
  .isalpha(): True   ✓
  .isalnum(): True   ✓
  .isnumeric(): False

Input: "abc123"
  .isdigit(): False
  .isalpha(): False
  .isalnum(): True   ✓ (ONLY this one passes!)
  .isnumeric(): False

Input: "12.5"
  .isdigit(): False  ← Decimal point fails!
  .isalpha(): False
  .isalnum(): False
  .isnumeric(): False
```

---

## 📚 CODE TEMPLATES

### TEMPLATE 1: Basic Type Checking with isinstance()

```python
def check_type(value):
    """
    Demonstrates isinstance() for type checking.
    
    USE CASE: Understanding what type a variable is
    BUSINESS VALUE: Educational example
    
    Parameters:
    - value: any type to check
    
    Returns: None (prints results)
    """
    print(f"Value: {value}")
    print(f"Is it an int? {isinstance(value, int)}")
    print(f"Is it a str? {isinstance(value, str)}")
    print(f"Is it a float? {isinstance(value, float)}")
    print("-" * 30)

# USAGE EXAMPLES:
check_type(42)      # Is int? True
check_type("42")    # Is str? True
check_type(42.5)    # Is float? True
```

**Key lesson:** Same-looking values can be different types!

---

### TEMPLATE 2: Validation Before Processing

```python
def safe_multiply(value, multiplier):
    """
    Multiplies numbers with type validation.
    
    USE CASE: Any mathematical operation with user input
    BUSINESS VALUE: Prevents type errors before they happen
    
    Parameters:
    - value: first number (should be int or float)
    - multiplier: second number (should be int or float)
    
    Returns: Result (int/float) or error message (str)
    """
    # VALIDATE: Check BOTH are numbers BEFORE multiplying
    if isinstance(value, (int, float)) and isinstance(multiplier, (int, float)):
        result = value * multiplier
        return result
    else:
        return "Error: Both inputs must be numbers"

# USAGE EXAMPLES:
print(safe_multiply(10, 5))      # 50 - works!
print(safe_multiply("10", 5))    # Error - caught before crash
print(safe_multiply("10", "5"))  # Error - caught before crash
print(safe_multiply(10.5, 2))    # 21.0 - floats work too
```

**Why This Pattern:**
- CHECK types first (validation)
- ONLY proceed if valid
- Error never happens (prevented)
- Clear error message if wrong type

**Compare to Day 15 (reactive):**
```python
# Day 15: Let it fail, then catch
try:
    result = "10" * 5  # Error HAPPENS
except TypeError:
    result = "Error"   # Then catch

# Day 16: Check first, prevent
if isinstance("10", (int, float)):  # Check FIRST
    result = "10" * 5
else:
    result = "Error"  # Error NEVER HAPPENS
```

---

### TEMPLATE 3: Defense in Depth (Validation + Error Handling)

```python
def professional_divide(a, b):
    """
    Professional division with two-layer security.
    
    USE CASE: Critical operations needing bulletproof code
    BUSINESS VALUE: Maximum reliability
    
    ARCHITECTURE:
    - Layer 1: Validate types (prevent obvious errors)
    - Layer 2: Error handling (catch unexpected errors)
    
    Parameters:
    - a: numerator (should be int or float)
    - b: denominator (should be int or float)
    
    Returns: Result or error message
    """
    # LAYER 1: VALIDATION (Day 16 - Prevent)
    if not isinstance(a, (int, float)):
        return "Error: First number must be int or float"
    
    if not isinstance(b, (int, float)):
        return "Error: Second number must be int or float"
    
    # LAYER 2: ERROR HANDLING (Day 15 - Catch)
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"

# USAGE EXAMPLES:
print(professional_divide(10, 2))    # 5.0 - both layers pass
print(professional_divide("10", 2))  # Layer 1 catches (validation)
print(professional_divide(10, 0))    # Layer 2 catches (error handling)
print(professional_divide("10", "2")) # Layer 1 catches first input
```

**How the layers work:**

**Test 1:** 10 ÷ 2
- Layer 1: ✅ Both numbers → pass through
- Layer 2: ✅ No error → success
- **Result:** 5.0

**Test 2:** "10" ÷ 2
- Layer 1: ❌ STOPPED! "10" is string
- Layer 2: Never reached
- **Result:** Error from validation

**Test 3:** 10 ÷ 0
- Layer 1: ✅ Both numbers → pass through
- Layer 2: ❌ CAUGHT! Division by zero
- **Result:** Error from error handling

**Why both layers:**
- Layer 1 stops 80% of errors (fast validation)
- Layer 2 catches 20% we can't predict (safety net)
- Together = 100% error coverage

---

### TEMPLATE 4: String Validation Methods

```python
def validate_string_input(user_input):
    """
    Demonstrates string validation methods.
    
    USE CASE: Understanding different string checks
    BUSINESS VALUE: Educational example
    
    Parameters:
    - user_input: string to validate
    
    Returns: None (prints results)
    """
    print(f"Input: '{user_input}'")
    print(f"  .isdigit(): {user_input.isdigit()}")     # Only digits?
    print(f"  .isalpha(): {user_input.isalpha()}")     # Only letters?
    print(f"  .isalnum(): {user_input.isalnum()}")     # Letters or digits?
    print(f"  .isnumeric(): {user_input.isnumeric()}") # Numeric?
    print("-" * 40)

# USAGE EXAMPLES:
validate_string_input("123")     # isdigit: True, isnumeric: True
validate_string_input("abc")     # isalpha: True, isalnum: True
validate_string_input("abc123")  # isalnum: True (ONLY)
validate_string_input("12.5")    # ALL False (decimal point!)
```

**Key patterns:**

| Input | isdigit() | isalpha() | isalnum() | isnumeric() |
|-------|-----------|-----------|-----------|-------------|
| "123" | ✓ | ✗ | ✓ | ✓ |
| "abc" | ✗ | ✓ | ✓ | ✗ |
| "abc123" | ✗ | ✗ | ✓ | ✗ |
| "12.5" | ✗ | ✗ | ✗ | ✗ |
| "-5" | ✗ | ✗ | ✗ | ✗ |
| "12 34" | ✗ | ✗ | ✗ | ✗ |

**Critical insight:** Decimals, negatives, and spaces fail ALL checks!

---

### TEMPLATE 5: Real-World Age Validation

```python
def get_valid_age(user_input):
    """
    Validates age input with multiple checks.
    Real-world example of comprehensive validation.
    
    USE CASE: User registration, forms, data entry
    BUSINESS VALUE: Clean data entry, prevent bad inputs
    
    VALIDATION LAYERS:
    1. Check if already correct type (int)
    2. If string, validate it's pure digits
    3. Convert and check range (0-120)
    
    Parameters:
    - user_input: age as string or int
    
    Returns: Valid age (int) or error message (str)
    """
    # CHECK 1: Is it NOT a string?
    if not isinstance(user_input, str):
        # If already an int, check if valid age
        if isinstance(user_input, int):
            if 0 <= user_input <= 120:
                return user_input
            else:
                return "Error: Age must be 0-120"
        return "Error: Invalid input type"
    
    # CHECK 2: Is string all digits? (No decimals, letters, etc.)
    if not user_input.isdigit():
        return "Error: Age must be a number (no decimals or letters)"
    
    # CHECK 3: Convert and check range
    age = int(user_input)
    if 0 <= age <= 120:
        return age
    else:
        return "Error: Age must be 0-120"

# USAGE EXAMPLES:
print(get_valid_age("25"))      # 25 - valid string
print(get_valid_age(30))        # 30 - valid int
print(get_valid_age("25.5"))    # Error - decimal (fails isdigit)
print(get_valid_age("twenty"))  # Error - letters (fails isdigit)
print(get_valid_age("150"))     # Error - out of range
print(get_valid_age("-5"))      # Error - negative (fails isdigit)
```

**How each test flows:**

**"25" (string):**
1. Is string? YES → continue
2. Is digits only? YES → continue
3. 0 ≤ 25 ≤ 120? YES → **Return 25**

**30 (int):**
1. Is string? NO → Is it int? YES
2. 0 ≤ 30 ≤ 120? YES → **Return 30**

**"25.5" (decimal):**
1. Is string? YES → continue
2. Is digits only? **NO** → **Stop immediately**

**"twenty" (letters):**
1. Is string? YES → continue
2. Is digits only? **NO** → **Stop immediately**

**"150" (out of range):**
1. Is string? YES → continue
2. Is digits only? YES → continue
3. 0 ≤ 150 ≤ 120? **NO** → **Error**

**"-5" (negative):**
1. Is string? YES → continue
2. Is digits only? **NO** (minus sign) → **Stop immediately**

**Why this pattern:**
- Handles both strings and ints
- Validates format before converting
- Checks range after converting
- Clear error messages for each case

---

### TEMPLATE 6: Bulletproof Email Tracking (Defense in Depth)

```python
def bulletproof_track_email(customer_tier, email_type, tokens_used):
    """
    Tracks email generation with comprehensive validation + error handling.
    Real-world application of Day 15 + Day 16 combined.
    
    USE CASE: Production email automation system
    BUSINESS VALUE: Bulletproof input handling, never crashes
    
    ARCHITECTURE:
    - Layer 1: Validation (prevent 80% of errors)
    - Layer 2: Error handling (catch remaining 20%)
    
    Parameters:
    - customer_tier: "VIP" or "standard" (str)
    - email_type: email category (str)
    - tokens_used: number of tokens (int or numeric string)
    
    Returns: True if logged, error message if invalid
    """
    # LAYER 1: VALIDATION (Day 16 - Prevent errors)
    
    # Validate customer_tier
    if not isinstance(customer_tier, str):
        return "Error: customer_tier must be a string"
    
    if customer_tier not in ["VIP", "standard"]:
        return f"Error: customer_tier must be 'VIP' or 'standard', got '{customer_tier}'"
    
    # Validate email_type
    if not isinstance(email_type, str):
        return "Error: email_type must be a string"
    
    # Validate tokens_used
    if isinstance(tokens_used, str):
        if not tokens_used.isdigit():
            return "Error: tokens_used must be a number"
        tokens_used = int(tokens_used)  # Convert if valid string
    elif not isinstance(tokens_used, int):
        return "Error: tokens_used must be int or numeric string"
    
    # LAYER 2: ERROR HANDLING (Day 15 - Catch unexpected)
    try:
        cost = (tokens_used / 1000) * 0.003
        print(f"✅ Logged: {customer_tier} {email_type} - ${cost:.4f}")
        return True
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

# USAGE EXAMPLES:
print(bulletproof_track_email("VIP", "complaint", 250))
# Output: ✅ Logged: VIP complaint - $0.0008
#         True

print(bulletproof_track_email("standard", "support", "180"))
# Output: ✅ Logged: standard support - $0.0005
#         True
# (Note: Converted string "180" to int automatically)

print(bulletproof_track_email("VIIP", "complaint", 250))
# Output: Error: customer_tier must be 'VIP' or 'standard', got 'VIIP'

print(bulletproof_track_email("VIP", "complaint", "250 tokens"))
# Output: Error: tokens_used must be a number

print(bulletproof_track_email(123, "complaint", 250))
# Output: Error: customer_tier must be a string
```

**Test results breakdown:**

**Test 1:** ("VIP", "complaint", 250)
- ✅ Validation: All checks pass
- ✅ Error handling: No errors
- **Result:** Successfully logged

**Test 2:** ("standard", "support", "180")
- ✅ Validation: String "180" is digits → converts to int
- ✅ Error handling: No errors
- **Result:** Successfully logged

**Test 3:** ("VIIP", "complaint", 250)
- ❌ Validation: "VIIP" not in allowed values
- **Result:** Stopped by validation

**Test 4:** ("VIP", "complaint", "250 tokens")
- ❌ Validation: "250 tokens" fails isdigit()
- **Result:** Stopped by validation

**Test 5:** (123, "complaint", 250)
- ❌ Validation: 123 is int, not string
- **Result:** Stopped by validation

**Why this works:**
- Validation catches 100% of the test errors
- Error handling stands ready for unexpected cases
- Clear, specific error messages
- Automatic type conversion when safe
- Never crashes on bad input

---

## 🔑 KEY CONCEPTS

### When To Use Validation vs Error Handling

**Use VALIDATION (Day 16) for:**
- ✅ Type checking (is it int/str/float?)
- ✅ Format checking (is it digits only?)
- ✅ Range checking (is it 0-120?)
- ✅ Value checking (is it in allowed list?)
- ✅ Known constraints (predictable rules)

**Use ERROR HANDLING (Day 15) for:**
- ✅ Division (can't predict zero ahead of time easily)
- ✅ File operations (file might not exist)
- ✅ API calls (network might be down)
- ✅ Unexpected errors (catch what validation missed)
- ✅ External failures (things outside your control)

**Use BOTH for:**
- ✅ Production systems
- ✅ User input handling
- ✅ Critical operations
- ✅ Client-facing code
- ✅ Any code that can't crash

---

### The Decision Tree

```
Is the error predictable?
    ↓
YES → Use validation
    |
    ├─ Is it type-related? → isinstance()
    ├─ Is it format-related? → .isdigit(), .isalpha()
    ├─ Is it range-related? → if 0 <= value <= 100
    └─ Is it value-related? → if value in allowed_list
    
NO → Use error handling
    |
    ├─ External resource? → try/except
    ├─ Runtime error? → try/except
    └─ Unknown error? → try/except
```

---

### isinstance() Advanced Usage

**Single type:**
```python
isinstance(value, int)  # Just int
```

**Multiple types (OR logic):**
```python
isinstance(value, (int, float))  # int OR float
isinstance(value, (int, float, str))  # int OR float OR str
```

**Checking NOT a type:**
```python
if not isinstance(value, str):
    # Value is NOT a string
```

**Common patterns:**
```python
# Accept numbers only
if isinstance(value, (int, float)):
    # Process as number

# Reject None
if value is not None and isinstance(value, str):
    # Process as string

# Convert if possible
if isinstance(value, str) and value.isdigit():
    value = int(value)  # Safe to convert
```

---

## 🔧 COMMON ERRORS AND FIXES

### Error 1: Using == Instead of isinstance()
**Symptom:** Type checks fail unexpectedly
```python
if type(value) == int:  # ❌ Doesn't work with subclasses
    process()
```

**Fix:** Use isinstance()
```python
if isinstance(value, int):  # ✅ Works with subclasses
    process()
```

**Why:** isinstance() is more flexible and professional

---

### Error 2: Forgetting Decimal Points Fail isdigit()
**Symptom:** Valid decimals rejected
```python
if user_input.isdigit():  # ❌ "12.5" returns False!
    value = int(user_input)
```

**Fix:** Handle decimals separately
```python
try:
    value = float(user_input)  # Works for both ints and floats
except ValueError:
    return "Error: Not a number"
```

**Or check for decimals:**
```python
if user_input.replace(".", "").isdigit():  # Remove decimal, then check
    value = float(user_input)
```

---

### Error 3: Validating After Converting
**Symptom:** Errors still happen during conversion
```python
age = int(user_input)  # ❌ Crashes if user_input = "abc"
if isinstance(age, int):  # Never reached if crashed!
    return age
```

**Fix:** Validate BEFORE converting
```python
if user_input.isdigit():  # ✅ Check FIRST
    age = int(user_input)  # Safe to convert now
    return age
else:
    return "Error: Must be a number"
```

---

### Error 4: Not Checking Both Sides of Operation
**Symptom:** Error on one valid, one invalid input
```python
if isinstance(a, int):  # ❌ Only checks first value!
    result = a / b  # Crashes if b is string
```

**Fix:** Validate ALL inputs
```python
if isinstance(a, (int, float)) and isinstance(b, (int, float)):  # ✅ Both
    result = a / b
else:
    return "Error: Both must be numbers"
```

---

### Error 5: Validation Without Error Handling
**Symptom:** Unexpected errors still crash
```python
if isinstance(value, int):  # ✅ Good validation
    result = process(value)  # ❌ But process() might still fail!
```

**Fix:** Defense in depth - both layers
```python
if isinstance(value, int):  # Layer 1: Validation
    try:  # Layer 2: Error handling
        result = process(value)
    except Exception:
        return "Error: Processing failed"
else:
    return "Error: Must be int"
```

---

## 💰 BUSINESS VALUE & ROI

### Scenario: E-Commerce Product Upload

**Client:** Online store uploading 1,000 products/day

**Without Validation (Amateur):**
```python
def add_product(name, price, quantity):
    # No validation - just add to database
    db.insert(name, price, quantity)
```

**Problems:**
- User enters price as "$19.99" (string with $)
- System crashes trying to calculate totals
- 500 products uploaded before crash
- 500 products lost
- 2 hours downtime
- **Cost:** $2,000 in lost sales + $500 developer fix = $2,500

---

**With Validation (Professional):**
```python
def add_product(name, price, quantity):
    # Validate name
    if not isinstance(name, str) or len(name) == 0:
        return "Error: Name must be non-empty string"
    
    # Validate price
    if isinstance(price, str):
        price = price.replace("$", "").replace(",", "")  # Clean it
        try:
            price = float(price)
        except ValueError:
            return "Error: Price must be a number"
    
    if not isinstance(price, (int, float)) or price <= 0:
        return "Error: Price must be positive number"
    
    # Validate quantity
    if not isinstance(quantity, int) or quantity < 0:
        return "Error: Quantity must be non-negative integer"
    
    # All validated - safe to insert
    try:
        db.insert(name, price, quantity)
        return "Success"
    except Exception as e:
        return f"Database error: {e}"
```

**Results:**
- Price "$19.99" → cleaned to 19.99 → works
- Invalid inputs caught immediately with helpful messages
- No crashes
- All 1,000 products uploaded successfully
- **Cost:** $0 downtime, $0 lost sales

**ROI:**
- Implementation: 30 minutes ($75)
- First prevented crash: Saved $2,500
- **Return:** 3,233% on first day

---

### Scenario: User Registration Form

**Client:** SaaS app with 100 registrations/day

**Without Validation:**
- Users enter anything
- Database gets corrupted data
- 20% of registrations have invalid emails
- 30% have invalid phone numbers
- Customer support overwhelmed with "can't login" tickets
- **Cost:** 5 support hours/day × $30/hour = $150/day = $4,500/month

**With Validation:**
```python
def validate_registration(email, phone, age):
    # Email validation
    if "@" not in email or "." not in email:
        return "Error: Invalid email format"
    
    # Phone validation
    phone = phone.replace("-", "").replace(" ", "")
    if not phone.isdigit() or len(phone) != 10:
        return "Error: Phone must be 10 digits"
    
    # Age validation
    if not isinstance(age, int) or not (13 <= age <= 120):
        return "Error: Age must be 13-120"
    
    return "Valid"
```

**Results:**
- Invalid emails rejected at signup
- Invalid phones caught immediately
- Support tickets reduced by 80%
- **Savings:** $3,600/month in support costs

**ROI:**
- Implementation: 1 hour ($150)
- Monthly savings: $3,600
- **Return:** 2,300% monthly

---

## 📊 VALIDATION PATTERNS

### Pattern 1: Type + Range Validation
```python
def validate_quantity(value):
    # Layer 1: Type
    if not isinstance(value, int):
        return "Error: Must be integer"
    
    # Layer 2: Range
    if value < 0:
        return "Error: Cannot be negative"
    
    if value > 10000:
        return "Error: Maximum is 10,000"
    
    return value  # Valid
```

**Use for:** Inventory, quantities, counts

---

### Pattern 2: Type + Format Validation
```python
def validate_email(email):
    # Layer 1: Type
    if not isinstance(email, str):
        return "Error: Must be string"
    
    # Layer 2: Format
    if "@" not in email:
        return "Error: Must contain @"
    
    if "." not in email:
        return "Error: Must contain ."
    
    # Layer 3: Basic structure
    if email.count("@") != 1:
        return "Error: Must have exactly one @"
    
    return email.lower()  # Valid + normalized
```

**Use for:** Emails, URLs, usernames

---

### Pattern 3: Type + Allowed Values
```python
def validate_status(status):
    # Layer 1: Type
    if not isinstance(status, str):
        return "Error: Must be string"
    
    # Layer 2: Allowed values
    allowed = ["pending", "approved", "rejected"]
    if status.lower() not in allowed:
        return f"Error: Must be one of {allowed}"
    
    return status.lower()  # Valid + normalized
```

**Use for:** Status fields, categories, enums

---

### Pattern 4: String Conversion with Validation
```python
def safe_int_convert(value):
    # Already an int?
    if isinstance(value, int):
        return value
    
    # String?
    if isinstance(value, str):
        # Remove common formatting
        value = value.strip().replace(",", "")
        
        # Check if digits
        if value.isdigit():
            return int(value)
        
        # Handle negatives
        if value.startswith("-") and value[1:].isdigit():
            return int(value)
        
        return "Error: Not a valid number"
    
    # Float?
    if isinstance(value, float):
        return int(value)  # Convert
    
    return "Error: Cannot convert to int"
```

**Use for:** Flexible input handling (forms, APIs)

---

## 🎯 PRACTICAL EXERCISES

### Exercise 1: Validate Password Strength
```python
def validate_password(password):
    """
    Validate password meets requirements:
    - At least 8 characters
    - Contains at least one digit
    - Contains at least one letter
    """
    # Your code here
```

**Solution approach:**
1. Check type (isinstance)
2. Check length (len >= 8)
3. Check has digit (any char.isdigit())
4. Check has letter (any char.isalpha())

---

### Exercise 2: Validate Price Input
```python
def validate_price(price):
    """
    Validate price:
    - Can be int, float, or string
    - If string, clean $ and , characters
    - Must be positive
    - Maximum $1,000,000
    """
    # Your code here
```

**Solution approach:**
1. Check type (isinstance)
2. If string, clean and convert
3. Check positive
4. Check maximum

---

### Exercise 3: Add Validation to Day 14 System
**Your task:** Add validation to your `route_email_request()` function:
- Validate customer_tier is string
- Validate customer_tier is "VIP" or "standard"
- Validate email_type is string
- Return helpful error messages

---

## 🔮 DAY 17 PREVIEW: ADVANCED VALIDATION PATTERNS

**Tomorrow you'll learn:**
- Regex basics (pattern matching)
- Complex string validation
- Data sanitization (cleaning messy input)
- Custom validation functions
- Validation libraries

**Example:**
```python
import re

def validate_email_advanced(email):
    # Regex pattern for email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    return False
```

**Why it matters:**
- Day 16 handles simple validation
- Day 17 handles complex patterns
- Together = professional input handling

---

## 💾 FILE ORGANIZATION

**Your Day 16 Structure:**
```
AI-Operations-Training/
├── Day-15/
│   ├── day15_error_handling.py
│   └── Day-15-Notes.md
├── Day-16/
│   ├── day16_input_validation.py (validation examples)
│   └── Day-16-Notes.md (this file)
└── Week-3-Video/
    └── watch-after-day-21.txt (Corey Schafer video reminder)
```

---

## 🏆 DAY 16 ACHIEVEMENTS

- [x] Learned isinstance() for type checking
- [x] Mastered string validation methods
- [x] Built validation functions
- [x] Combined validation + error handling (defense in depth)
- [x] Created bulletproof input handling
- [x] Applied to real-world scenarios
- [x] Understood when to validate vs error handle

**Grade: A+**

---

## 📝 KEY TAKEAWAYS

1. **isinstance() checks types** - Use before operating on data
2. **String methods validate format** - .isdigit(), .isalpha(), .isalnum()
3. **Validation prevents errors** - Better than catching them
4. **Defense in depth** - Validation + error handling together
5. **Check before converting** - Validate string before int()
6. **Clear error messages** - Tell user what's wrong
7. **Decimals fail isdigit()** - Common gotcha to remember

---

## 🎓 THE SIMPLE COMPARISON

### **Day 15 (Reactive):**
```python
try:
    # Let it fail
    result = risky_operation()
except:
    # Then catch it
    result = "Error"
```

### **Day 16 (Proactive):**
```python
if validate(data):
    # Prevent the fail
    result = safe_operation()
else:
    # Never even tried
    result = "Error"
```

### **Professional (Both):**
```python
if validate(data):  # Layer 1: Prevent
    try:  # Layer 2: Catch
        result = operation()
    except:
        result = "Error"
else:
    result = "Error"
```

---

## 🔧 TROUBLESHOOTING QUICK REFERENCE

| Error | Cause | Fix |
|-------|-------|-----|
| "12.5" fails isdigit() | Decimal point | Use try: float() or replace(".", "") |
| isinstance always False | Checking wrong type | Check actual type with type() |
| Validation after crash | Converting before checking | Check BEFORE converting |
| Still getting errors | Only validated one input | Validate ALL inputs |
| False negatives | Case sensitivity | Use .lower() to normalize |

---

## 📞 WHEN TO USE WHAT

**Use isinstance():**
- Checking if int, str, float, etc.
- Before mathematical operations
- When type matters

**Use .isdigit():**
- String contains only numbers (no decimals)
- Phone numbers
- Integers as strings

**Use .isalpha():**
- String contains only letters
- Names (simple check)
- Alphabetic codes

**Use .isalnum():**
- String contains letters or numbers
- Usernames
- Alphanumeric codes

**Use try/except:**
- After validation (defense in depth)
- Converting types (int(), float())
- External operations (files, APIs)

---

## 🎯 WEEK 3 PROGRESS

**Completed:** 
- ✅ Day 15 (Error Handling)
- ✅ Day 16 (Input Validation)

**Remaining in Week 3:**
- Day 17: Advanced Validation
- Day 18: Custom Exceptions
- Day 19: Logging
- Day 20: Debugging Techniques
- Day 21: Week 3 Integration

**After Day 21:** Watch Corey Schafer error handling video

---

**Created:** Day 16 of AI Operations Training  
**Your Progress:** Week 3, Day 2 (Day 16/168 total)  
**Next Session:** Day 17 - Advanced Validation Patterns

**You're building professional, bulletproof code now.** 🛡️💪
