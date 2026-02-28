# DAY 11: CONDITIONAL PROMPT LOGIC & SMART TEMPLATES
## AI Operations Training - Week 2

---

## 🎯 WHAT YOU LEARNED TODAY

### Core Skills:
- ✅ Conditional logic with if/elif/else chains
- ✅ Building adaptive templates that "think"
- ✅ Default fallbacks with else clauses
- ✅ Case sensitivity in string comparisons
- ✅ Multiple condition checking
- ✅ Following exact client specifications

### The Architecture "Why":
**Day 10 taught you:** How to build templates with variables  
**Day 11 taught you:** How to make templates that ADAPT based on context

**The Problem Day 11 Solves:**
- Without conditional logic: 10 scenarios = 10 separate functions (code duplication)
- With conditional logic: 100 scenarios = 1 smart function (scalable, maintainable)

**Real Business Impact:**
- Client needs templates for 20 different recipient types
- Amateur approach: Write 20 separate functions (2 weeks)
- Professional approach: Add 20 elif statements to one function (30 minutes)
- **You just became 40x more efficient**

---

## 📚 CORE CONCEPTS

### Understanding if/elif/else

**The Flow:**
```
if condition1:           ← Check first condition
    do_this             ← If TRUE, run this and STOP
elif condition2:         ← Only checked if condition1 was FALSE
    do_that             ← If TRUE, run this and STOP
elif condition3:         ← Only checked if condition2 was also FALSE
    do_other            ← If TRUE, run this and STOP
else:                    ← Only runs if ALL conditions were FALSE
    do_default          ← Safety net / backup plan
```

**Key Rules:**
1. **Python checks conditions TOP to BOTTOM**
2. **Stops at the FIRST TRUE condition**
3. **Only ONE block of code runs** (never multiple)
4. **else is optional** but recommended as a safety net

---

### The Difference: Multiple if vs if/elif

**OPTION 1: Multiple if statements (checks ALL)**
```python
age = 15

if age < 13:
    print("child")
    
if age < 18:
    print("teenager")     # This runs
    
if age < 65:
    print("adult")        # This ALSO runs
```
**Output:** Both "teenager" and "adult" print

**Problem:** Checks EVERY condition even after finding a match

---

**OPTION 2: if/elif chain (stops at first match)**
```python
age = 15

if age < 13:
    print("child")
elif age < 18:
    print("teenager")     # This runs
elif age < 65:
    print("adult")        # This NEVER checked (already stopped)
```
**Output:** Only "teenager" prints

**Benefit:** More efficient, stops checking once condition is met

---

**When to use which:**
- **Multiple if:** When you need to check ALL conditions (rare)
- **if/elif/else:** When you want ONE result from multiple options (most common)

---

## 📚 CODE TEMPLATES

### TEMPLATE 1: Smart Email Builder (Role-Based Tone)

```python
def build_smart_email(recipient_role, topic):
    """
    Generates email prompts with adaptive tone based on recipient.
    
    USE CASE: One function handles all recipient types
    BUSINESS VALUE: Scales to 100+ roles without code duplication
    
    Parameters:
    - recipient_role: Who you're emailing (str) - e.g., "CEO", "colleague"
    - topic: Email subject (str) - e.g., "project update"
    
    Returns: Complete email prompt with appropriate tone
    """
    if recipient_role == "CEO":
        tone = "formal and data-driven"
    elif recipient_role == "colleague":
        tone = "friendly and collaborative"
    elif recipient_role == "customer":
        tone = "professional and helpful"
    elif recipient_role == "manager":
        tone = "respectful and concise"
    else:
        tone = "professional"  # Default for unknown roles
    
    prompt = f"Write a {tone} email to a {recipient_role} about {topic}."
    return prompt

# USAGE EXAMPLES:
print(build_smart_email("CEO", "Q4 revenue analysis"))
# Output: "Write a formal and data-driven email to a CEO about Q4 revenue analysis."

print(build_smart_email("colleague", "lunch plans"))
# Output: "Write a friendly and collaborative email to a colleague about lunch plans."

print(build_smart_email("intern", "orientation"))  # Not in our list
# Output: "Write a professional email to an intern about orientation."  # Uses else
```

**Customization Ideas:**
- Add more roles (VP, director, vendor, etc.)
- Add urgency parameter: if urgent → add "urgent" to tone
- Add length parameter: control word count
- Add language parameter: multi-language support

---

### TEMPLATE 2: Product Description Generator (Type-Based Style)

```python
def build_product_description(product_type, product_name):
    """
    Creates product descriptions with style adapted to product category.
    
    USE CASE: E-commerce sites with multiple product categories
    BUSINESS VALUE: Consistent brand voice per category at scale
    
    Parameters:
    - product_type: Product category (str) - e.g., "tech", "food", "clothing"
    - product_name: Specific product (str) - e.g., "wireless headphones"
    
    Returns: Product description prompt with category-appropriate style
    """
    if product_type == "tech":
        style = "innovative and cutting-edge"
    elif product_type == "food":
        style = "delicious and mouth-watering"
    elif product_type == "clothing":
        style = "stylish and comfortable"
    else:
        style = "high-quality"  # Generic default
    
    prompt = f"Write a {style} description for {product_name}"
    return prompt

# USAGE EXAMPLES:
print(build_product_description("tech", "wireless headphones"))
# Output: "Write a innovative and cutting-edge description for wireless headphones"

print(build_product_description("food", "chocolate cake"))
# Output: "Write a delicious and mouth-watering description for chocolate cake"

print(build_product_description("toy", "building blocks"))  # Not in list
# Output: "Write a high-quality description for building blocks"  # Uses else
```

**Real Business Application:**
- E-commerce platform with 1,000 products across 10 categories
- Without this: Manually write 1,000 prompts or use generic descriptions
- With this: Generate all 1,000 with appropriate style in seconds
- **Time saved:** 40+ hours of manual prompt writing

---

### TEMPLATE 3: Multi-Tier Service Response Generator

```python
def build_support_response(customer_tier, issue_type):
    """
    Generates customer support responses based on customer tier.
    Premium customers get priority language.
    
    USE CASE: SaaS companies with tiered pricing
    BUSINESS VALUE: VIP treatment for high-value customers
    
    Parameters:
    - customer_tier: Customer level (str) - "premium", "standard", "trial"
    - issue_type: Type of problem (str) - e.g., "bug", "feature_request"
    
    Returns: Support response prompt with tier-appropriate urgency
    """
    if customer_tier == "premium":
        urgency = "urgent and prioritized"
    elif customer_tier == "standard":
        urgency = "professional and helpful"
    elif customer_tier == "trial":
        urgency = "friendly and educational"
    else:
        urgency = "courteous"
    
    prompt = f"Write a {urgency} support response about {issue_type}."
    return prompt

# USAGE EXAMPLES:
print(build_support_response("premium", "data loss"))
# Output: "Write a urgent and prioritized support response about data loss."

print(build_support_response("trial", "how to export data"))
# Output: "Write a friendly and educational support response about how to export data."
```

**Why This Matters:**
- Premium customers (paying $500/mo) get immediate, urgent responses
- Trial users (paying $0/mo) get helpful but not urgent responses
- Automatically maintains service tier expectations
- **Result:** Higher retention, appropriate resource allocation

---

## 🔑 KEY CONCEPTS

### Case Sensitivity in Python

**CRITICAL:** Python treats these as DIFFERENT strings:
```python
"CEO" ≠ "ceo" ≠ "Ceo" ≠ "CeO"
"Manager" ≠ "manager"
"Tech" ≠ "tech"
```

**Common Error:**
```python
if recipient_role == "Manager":  # Checking for capital M
    tone = "respectful"

# Later in code:
build_smart_email("manager", "update")  # Passing lowercase m
# Result: Doesn't match! Goes to else clause instead
```

**Best Practice:**
- **Pick one style** (usually lowercase) and stick to it
- Document it: "All role parameters must be lowercase"
- Or use `.lower()` to force consistency:
```python
if recipient_role.lower() == "manager":  # Converts input to lowercase first
    tone = "respectful"
```

---

### The Importance of else Clauses

**Without else (Dangerous):**
```python
def build_email(role, topic):
    if role == "CEO":
        tone = "formal"
    elif role == "colleague":
        tone = "friendly"
    # No else clause!
    
    prompt = f"Write a {tone} email..."  # ERROR if role is neither!
    return prompt

build_email("vendor", "invoice")  # CRASH! 'tone' was never defined
```

**With else (Safe):**
```python
def build_email(role, topic):
    if role == "CEO":
        tone = "formal"
    elif role == "colleague":
        tone = "friendly"
    else:
        tone = "professional"  # Safety net
    
    prompt = f"Write a {tone} email..."  # Always works
    return prompt

build_email("vendor", "invoice")  # Works! Uses "professional"
```

**Professional Principle:**
> "Always code defensively. Assume users will pass unexpected inputs."

---

### Comparison Operators

**Used in conditions:**
```python
==    # Equal to (checking, not assigning)
!=    # Not equal to
>     # Greater than
<     # Less than
>=    # Greater than or equal to
<=    # Less than or equal to
```

**Examples:**
```python
if age == 18:           # Is age exactly 18?
if age != 18:           # Is age anything BUT 18?
if age > 18:            # Is age more than 18?
if age >= 18:           # Is age 18 or more?
if name == "Alice":     # Is name exactly "Alice"?
if status != "active":  # Is status anything except "active"?
```

**Common Mistake:**
```python
if role = "CEO":  # WRONG! Single = is assignment, not comparison
if role == "CEO": # CORRECT! Double == checks equality
```

---

## 🔧 COMMON ERRORS AND FIXES

### Error 1: IndentationError
**Symptom:** "expected an indented block after 'if' statement"
```python
if role == "CEO":
tone = "formal"  # ERROR! Not indented
```

**Fix:** Indent everything inside the if block
```python
if role == "CEO":
    tone = "formal"  # Correct
```

---

### Error 2: UnboundLocalError
**Symptom:** "cannot access local variable 'tone' where it is not associated with a value"
```python
def build_email(role):
    if role == "CEO":
        tone = "formal"
    # Missing else!
    return f"Write a {tone} email"  # ERROR if role != "CEO"

build_email("manager")  # Crashes!
```

**Fix:** Always include else clause
```python
def build_email(role):
    if role == "CEO":
        tone = "formal"
    else:
        tone = "professional"  # Safety net
    return f"Write a {tone} email"  # Always works
```

---

### Error 3: Case Sensitivity Mismatch
**Symptom:** Code goes to else when it should match a condition
```python
if role == "Manager":  # Capital M
    tone = "respectful"

build_email("manager", "update")  # lowercase m - doesn't match!
```

**Fix:** Use consistent casing (recommend lowercase)
```python
if role == "manager":  # lowercase
    tone = "respectful"

build_email("manager", "update")  # Matches!
```

---

### Error 4: Using = Instead of ==
**Symptom:** "invalid syntax" or unexpected behavior
```python
if role = "CEO":  # WRONG! Assignment operator
    tone = "formal"
```

**Fix:** Use == for comparisons
```python
if role == "CEO":  # CORRECT! Comparison operator
    tone = "formal"
```

---

## 💰 BUSINESS VALUE & ROI

### Scenario: E-Commerce Product Descriptions

**Client needs:**
- 5,000 products across 8 categories
- Each category needs distinct writing style

**Amateur Approach:**
```python
def tech_description(name):
    return f"Innovative {name}"

def food_description(name):
    return f"Delicious {name}"

# ... 6 more functions
# Total: 8 separate functions to maintain
```
**Problems:**
- Code duplication
- Hard to add new categories
- Difficult to update tone consistently

**Professional Approach (Your Template):**
```python
def build_product_description(product_type, product_name):
    if product_type == "tech":
        style = "innovative and cutting-edge"
    elif product_type == "food":
        style = "delicious and mouth-watering"
    # ... 6 more elif
    else:
        style = "high-quality"
    
    return f"Write a {style} description for {product_name}"
```
**Benefits:**
- ONE function handles all categories
- Add new category = add 2 lines of code (30 seconds)
- Update tone = change one string (10 seconds)

**Time Savings:**
- Setup: 2 hours vs 8 hours = **6 hours saved**
- Adding category: 30 seconds vs 1 hour = **99% faster**
- Updating tone: 10 seconds vs 1 hour (updating 8 functions) = **99.5% faster**

**Billing Impact:**
- Your hourly rate: $150/hour
- Time saved on this project: 20+ hours
- **Value delivered: $3,000+**
- Your actual time: 2 hours
- **Profit margin: 90%**

---

## 📊 WHEN TO USE CONDITIONAL LOGIC

### ✅ GOOD Use Cases:

1. **Different tones based on recipient**
   - CEO vs colleague vs customer
   - Premium vs standard customer tier

2. **Different styles based on category**
   - Tech vs food vs clothing products
   - Blog vs email vs social media content

3. **Different responses based on context**
   - Urgent vs routine requests
   - New vs returning customers
   - Error vs success scenarios

4. **Dynamic word limits**
   - Twitter (280 chars) vs blog (1000+ words)
   - Executive summary (100 words) vs full report (500 words)

5. **Multi-language support**
   - EN vs ES vs FR content
   - Region-specific phrasing

---

### ❌ BAD Use Cases (Overcomplicated):

1. **Only 1-2 options**
   ```python
   # Don't do this:
   if is_urgent:
       word_limit = 50
   else:
       word_limit = 200
   
   # Just do this:
   word_limit = 50 if is_urgent else 200
   ```

2. **Conditions that should be parameters**
   ```python
   # Don't hardcode choices:
   if product == "laptop":
       price = 999
   elif product == "mouse":
       price = 29
   
   # Use a lookup instead (Day 13 material):
   prices = {"laptop": 999, "mouse": 29}
   price = prices[product]
   ```

---

## 🎯 PRACTICE EXERCISES

### Exercise 1: Blog Post Tone Adjuster
**Build:** `build_blog_prompt(audience, topic)`

**Requirements:**
- If audience == "technical" → tone = "detailed and precise"
- If audience == "beginner" → tone = "simple and easy-to-understand"
- If audience == "executive" → tone = "high-level and strategic"
- Else → tone = "informative"

**Test with:**
```python
print(build_blog_prompt("technical", "API design patterns"))
print(build_blog_prompt("beginner", "what is AI"))
print(build_blog_prompt("general", "productivity tips"))
```

---

### Exercise 2: Social Media Post Generator
**Build:** `build_social_prompt(platform, message)`

**Requirements:**
- If platform == "twitter" → style = "concise (280 characters)"
- If platform == "linkedin" → style = "professional and thought-provoking"
- If platform == "instagram" → style = "visual and engaging"
- Else → style = "casual and friendly"

**Test with:**
```python
print(build_social_prompt("twitter", "product launch"))
print(build_social_prompt("linkedin", "industry insights"))
print(build_social_prompt("facebook", "community update"))
```

---

### Exercise 3: Add Multiple Conditions
**Expand your email function to also check urgency:**

```python
def build_advanced_email(recipient_role, topic, urgency):
    # Your task: combine role AND urgency
    # Examples:
    # - CEO + urgent → "urgent and executive-level"
    # - CEO + normal → "formal and data-driven"
    # - colleague + urgent → "quick and collaborative"
    # etc.
```

**Hint:** Day 12 will teach you how to do this with `and`/`or` operators!

---

## 🔮 DAY 12 PREVIEW: COMBINING CONDITIONS

**What's Next:**
You'll learn to check MULTIPLE things in one condition:

```python
if role == "CEO" and urgency == "high":
    tone = "urgent and executive-level"
elif role == "CEO" and urgency == "low":
    tone = "formal but relaxed"
```

**Also:**
- `or` operator: Check if ANY condition is true
- `not` operator: Reverse a condition
- Nested if statements: Conditions inside conditions

**This unlocks:**
- Complex business logic
- Multi-factor decision making
- Real-world scenario handling

---

## 💾 FILE ORGANIZATION

**Your Day 11 Structure:**
```
AI-Operations-Training/
├── Day-10/
│   ├── day10_test.py
│   └── Day-10-Notes.md
├── Day-11/
│   ├── Day-11.py (smart email + product description functions)
│   └── Day-11-Notes.md (this file)
└── Libraries/
    └── prompt_templates.py (start collecting reusable functions)
```

**Professional Tip:**
Start a `Libraries/prompt_templates.py` file and copy your best functions there:
```python
# Libraries/prompt_templates.py

def build_smart_email(recipient_role, topic):
    # ... your code ...
    pass

def build_product_description(product_type, product_name):
    # ... your code ...
    pass

# Future projects can import these:
# from Libraries.prompt_templates import build_smart_email
```

---

## 🏆 DAY 11 ACHIEVEMENTS

- [x] Built conditional logic from scratch
- [x] Created adaptive template functions
- [x] Mastered if/elif/else chains
- [x] Implemented default fallback patterns
- [x] Understood case sensitivity impacts
- [x] Followed exact client specifications
- [x] Tested code with multiple scenarios
- [x] Debugged common errors independently

**Grade: A+**

---

## 📝 KEY TAKEAWAYS

1. **if/elif/else stops at first match** - more efficient than multiple if statements
2. **else is your safety net** - always include it to handle unexpected inputs
3. **Case sensitivity matters** - "Manager" ≠ "manager" in Python
4. **One smart function beats many simple functions** - scalability principle
5. **Following specs exactly is professional** - creativity comes after requirements are met

---

## 🎓 PROFESSIONAL PRINCIPLES LEARNED

### Principle 1: Defensive Coding
> "Always code assuming users will pass unexpected inputs."

Use else clauses, validate inputs, provide defaults.

### Principle 2: DRY (Don't Repeat Yourself)
> "If you're copying code, you're doing it wrong."

One smart function with conditions > Many duplicate functions.

### Principle 3: Specification Compliance
> "Build what the client asked for first, suggest improvements second."

Follow requirements exactly before adding creative touches.

### Principle 4: Scalability Thinking
> "Will this work for 10 scenarios? How about 100?"

Always design for growth from day one.

---

## 🔧 TROUBLESHOOTING QUICK REFERENCE

| Error | Cause | Fix |
|-------|-------|-----|
| IndentationError | Code not indented inside if block | Add 4 spaces/1 tab before code |
| UnboundLocalError | Variable used before being defined | Add else clause to define default |
| Condition never matches | Case sensitivity mismatch | Use consistent casing (lowercase recommended) |
| SyntaxError: invalid syntax | Used = instead of == | Use == for comparisons, = for assignment |

---

## 📞 WHEN TO USE WHAT

**Use `if` alone when:**
- Only one condition to check
- Want to optionally do something

**Use `if/else` when:**
- Two mutually exclusive options
- Always need a result

**Use `if/elif/else` when:**
- Multiple options (3+)
- Want to stop at first match
- Need a default fallback

**Use multiple `if` when:**
- Need to check ALL conditions
- Multiple things can be true simultaneously
- Rare in prompt building

---

## 🎯 NEXT SESSION

**Day 12: Combining Conditions & Complex Logic**

**You'll build:**
- Multi-factor decision functions
- Nested conditional logic
- Boolean operators (and/or/not)

**See you then!** 🚀

---

**Created:** Day 11 of AI Operations Training  
**Your Progress:** Month 1, Week 2 (Days 8-14)  
**Next Session:** Day 12 - Combined Conditions & Boolean Logic

**You're not just learning code. You're learning to think like a systems architect.**
