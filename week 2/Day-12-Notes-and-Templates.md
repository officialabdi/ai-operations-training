# DAY 12: COMBINING CONDITIONS & MULTI-FACTOR LOGIC
## AI Operations Training - Week 2

---

## 🎯 WHAT YOU LEARNED TODAY

### Core Skills:
- ✅ Boolean operators: `and`, `or`, `not`
- ✅ Multi-factor decision making (checking 2+ things at once)
- ✅ Combined conditions in if statements
- ✅ Comparison operators: `>=`, `<=`, `<`, `>`, `==`, `!=`
- ✅ Complex business logic patterns
- ✅ Priority routing systems

### The Architecture "Why":
**Day 11 taught you:** How to check ONE factor and make decisions  
**Day 12 taught you:** How to check MULTIPLE factors simultaneously

**The Problem Day 12 Solves:**
- Real business rules depend on MULTIPLE factors, not just one
- Need to handle: "If person is VIP AND it's urgent" or "If payment is cash OR card"
- Single-factor logic from Day 11 is insufficient for complex scenarios

**Real Business Impact:**
- VIP routing: Check customer tier AND years active
- Priority support: Check urgency level AND customer value
- Access control: Check permission AND authentication status
- Complex workflows that require multiple criteria

---

## 📚 CORE CONCEPTS

### The Three Boolean Operators

**1. `and` - BOTH conditions must be true**
```python
if condition1 and condition2:
    # Only runs if BOTH are true
```
**Real-world analogy:** "To board a plane, you need ticket AND passport"

---

**2. `or` - AT LEAST ONE condition must be true**
```python
if condition1 or condition2:
    # Runs if EITHER (or both) is true
```
**Real-world analogy:** "You can pay with cash OR card"

---

**3. `not` - REVERSE a condition**
```python
if not condition:
    # Runs if condition is FALSE
```
**Real-world analogy:** "If you're NOT on the no-fly list, you can board"

---

### Truth Tables (How They Work)

**`and` Operator:**
```
Condition1  |  Condition2  |  Result
----------- | ------------ | --------
   True     |     True     |   True   ✓
   True     |     False    |   False
   False    |     True     |   False
   False    |     False    |   False
```
**Only TRUE if BOTH are true**

---

**`or` Operator:**
```
Condition1  |  Condition2  |  Result
----------- | ------------ | --------
   True     |     True     |   True   ✓
   True     |     False    |   True   ✓
   False    |     True     |   True   ✓
   False    |     False    |   False
```
**TRUE if AT LEAST ONE is true**

---

**`not` Operator:**
```
Condition   |   not Condition
----------- | ----------------
   True     |      False
   False    |      True
```
**Reverses the truth value**

---

### Comparison Operators

**Used to compare values:**
```python
==    # Equal to
!=    # Not equal to
>     # Greater than
<     # Less than
>=    # Greater than or equal to
<=    # Less than or equal to
```

**Examples:**
```python
age >= 18           # Age is 18 or more
score < 50          # Score is less than 50
name == "Alice"     # Name is exactly "Alice"
status != "banned"  # Status is anything except "banned"
price > 100         # Price is more than 100
years <= 5          # Years is 5 or less
```

---

## 📚 CODE TEMPLATES

### TEMPLATE 1: Priority Email System (Using `and`)

```python
def build_priority_email(recipient_role, urgency, topic):
    """
    Generates emails with tone based on BOTH role AND urgency.
    
    USE CASE: Executive communications that adapt to situation severity
    BUSINESS VALUE: Appropriate tone for every combination of recipient + urgency
    
    Parameters:
    - recipient_role: Who you're emailing (str) - "ceo", "colleague", "manager"
    - urgency: How urgent (str) - "high", "low"
    - topic: Email subject (str)
    
    Returns: Email prompt with contextually appropriate tone
    """
    if recipient_role == "ceo" and urgency == "high":
        tone = "URGENT and executive-level"
    elif recipient_role == "ceo" and urgency == "low":
        tone = "formal and data-driven"
    elif recipient_role == "colleague" and urgency == "high":
        tone = "quick and collaborative"
    elif recipient_role == "colleague" and urgency == "low":
        tone = "friendly and casual"
    else:
        tone = "professional"  # Default for unhandled combinations
    
    prompt = f"Write a {tone} email to a {recipient_role} about {topic}."
    return prompt

# USAGE EXAMPLES:
print(build_priority_email("ceo", "high", "server outage"))
# Output: "Write a URGENT and executive-level email to a ceo about server outage."

print(build_priority_email("ceo", "low", "quarterly planning"))
# Output: "Write a formal and data-driven email to a ceo about quarterly planning."

print(build_priority_email("colleague", "high", "deadline today"))
# Output: "Write a quick and collaborative email to a colleague about deadline today."

print(build_priority_email("manager", "medium"))  # Not in our rules
# Output: "Write a professional email to a manager about update."  # Uses else
```

**Why `and` Here:**
- Need to check BOTH role AND urgency to determine correct tone
- CEO + high urgency requires DIFFERENT tone than CEO + low urgency
- Same role, different urgency = different communication style
- **Both factors matter equally**

**Real Business Application:**
- Email automation system for executive team
- Automatically adjusts tone based on situation severity + recipient seniority
- Prevents tone-deaf communications (casual email to CEO during crisis)
- **Value:** Saves hours of manual email drafting, ensures appropriate communication

---

### TEMPLATE 2: VIP Support Routing (Using `or`)

```python
def check_support_priority(customer_tier, years_active):
    """
    Determines support priority based on tier OR loyalty.
    Customer gets VIP treatment if they meet EITHER criterion.
    
    USE CASE: SaaS customer support routing
    BUSINESS VALUE: Rewards both paying customers AND long-term users
    
    Parameters:
    - customer_tier: Subscription level (str) - "premium", "standard", "trial"
    - years_active: Years as customer (int) - e.g., 3, 7, 10
    
    Returns: Support priority level (str)
    """
    if customer_tier == "premium" or years_active >= 5:
        priority = "VIP - Priority Support"
    else:
        priority = "Standard Support"
    
    return priority

# USAGE EXAMPLES:
print(check_support_priority("premium", 2))
# Output: "VIP - Priority Support"
# Reason: Premium tier (doesn't matter that years < 5)

print(check_support_priority("standard", 7))
# Output: "VIP - Priority Support"
# Reason: 7 years active (doesn't matter that tier is standard)

print(check_support_priority("premium", 8))
# Output: "VIP - Priority Support"
# Reason: BOTH conditions true (but only needed one!)

print(check_support_priority("standard", 3))
# Output: "Standard Support"
# Reason: Neither condition is true
```

**Why `or` Here:**
- Customer qualifies for VIP if they meet EITHER condition
- Premium subscribers get VIP regardless of tenure
- Long-term users get VIP regardless of current subscription
- **Flexible qualification - only need to meet one criterion**

**Real Business Logic:**
```
Premium + new customer (2 years)    → VIP (rewarding revenue)
Standard + loyal customer (7 years) → VIP (rewarding loyalty)
Premium + loyal customer (8 years)  → VIP (best of both!)
Standard + new customer (3 years)   → Standard (neither criterion met)
```

**Business Rationale:**
- Retains premium subscribers (they get immediate VIP treatment)
- Retains long-term users (loyalty is rewarded even if they downgrade)
- Incentivizes both upgrades AND long-term relationships
- **ROI:** Reduces churn, increases customer satisfaction

---

### TEMPLATE 3: Content Classification System (Combined Logic)

```python
def check_content_urgency(content_type, word_count):
    """
    Classifies content based on type and length for routing/prioritization.
    Demonstrates both `or` and `and` in same function.
    
    USE CASE: Content management system, social media scheduling
    BUSINESS VALUE: Auto-routes content to appropriate channels/workflows
    
    Parameters:
    - content_type: Type of content (str) - "tweet", "blog", "email", "article"
    - word_count: Number of words (int) - e.g., 25, 500, 1500
    
    Returns: Content classification (str)
    """
    if content_type == "tweet" or word_count < 50:
        return "Quick post"
    elif content_type == "blog" and word_count >= 1000:
        return "Long-form article"
    elif content_type == "email" and word_count < 200:
        return "Brief message"
    else:
        return "Standard content"

# USAGE EXAMPLES:
print(check_content_urgency("tweet", 25))
# Output: "Quick post"
# Reason: Type is "tweet" (or triggers immediately)

print(check_content_urgency("social", 30))
# Output: "Quick post"
# Reason: word_count < 50 (or triggers on second condition)

print(check_content_urgency("blog", 1500))
# Output: "Long-form article"
# Reason: Type is "blog" AND word_count >= 1000 (both true)

print(check_content_urgency("email", 150))
# Output: "Brief message"
# Reason: Type is "email" AND word_count < 200 (both true)

print(check_content_urgency("report", 500))
# Output: "Standard content"
# Reason: None of the specific rules matched
```

**Why Mixed Operators:**
- First rule uses `or`: Quick posts can be EITHER tweets OR short (any type)
- Second rule uses `and`: Long-form requires BOTH "blog" type AND 1000+ words
- Third rule uses `and`: Brief messages require BOTH "email" type AND under 200 words
- **Different rules need different logic patterns**

**Real Business Application:**
- Content scheduling system for social media agency
- Routes tweets to immediate posting queue
- Routes long-form to editorial review
- Routes brief emails to quick-send
- **Automation:** Saves 10+ hours/week on manual content sorting

---

### TEMPLATE 4: Access Control System (Using `not`)

```python
def check_access(user_role, is_banned, has_2fa):
    """
    Determines if user can access system based on multiple security factors.
    Demonstrates use of `not` operator.
    
    USE CASE: Application security, user authentication
    BUSINESS VALUE: Multi-factor access control
    
    Parameters:
    - user_role: User's role (str) - "admin", "user", "guest"
    - is_banned: Whether user is banned (bool) - True/False
    - has_2fa: Whether 2FA is enabled (bool) - True/False
    
    Returns: Access decision (str)
    """
    if is_banned:
        return "ACCESS DENIED - Account banned"
    elif user_role == "admin" and not is_banned:
        return "FULL ACCESS - Admin privileges"
    elif user_role == "user" and has_2fa and not is_banned:
        return "ACCESS GRANTED - Standard user"
    elif user_role == "guest" and not is_banned:
        return "LIMITED ACCESS - Guest mode"
    else:
        return "ACCESS DENIED - Insufficient permissions"

# USAGE EXAMPLES:
print(check_access("admin", False, True))
# Output: "FULL ACCESS - Admin privileges"
# Reason: Admin and NOT banned

print(check_access("user", False, True))
# Output: "ACCESS GRANTED - Standard user"
# Reason: User with 2FA and NOT banned

print(check_access("user", False, False))
# Output: "ACCESS DENIED - Insufficient permissions"
# Reason: User without 2FA (needs it for access)

print(check_access("admin", True, True))
# Output: "ACCESS DENIED - Account banned"
# Reason: Banned users can't access (even if admin)
```

**Why `not` Here:**
- `not is_banned` is cleaner than `is_banned == False`
- Reads more naturally: "if user is not banned"
- Common pattern in security/access control logic

---

## 🔑 KEY CONCEPTS

### When To Use `and` vs `or`

**Use `and` when:**
- All conditions must be satisfied
- Stricter requirements
- "This AND that must be true"

**Examples:**
```python
# Must be BOTH adult AND have license to drive
if age >= 18 and has_license:
    allow_driving()

# Must be BOTH manager AND in finance dept for bonus approval
if role == "manager" and department == "finance":
    can_approve_bonus()

# Must meet ALL requirements
if gpa >= 3.5 and test_score >= 90 and has_recommendation:
    accept_to_program()
```

---

**Use `or` when:**
- At least one condition needs to be satisfied
- More flexible/inclusive
- "This OR that can be true"

**Examples:**
```python
# Can pay with EITHER cash OR card
if payment == "cash" or payment == "card":
    process_payment()

# VIP if EITHER premium subscriber OR long-term user
if tier == "premium" or years >= 5:
    give_vip_access()

# Urgent if ANY high-priority indicator
if priority == "urgent" or customer_type == "enterprise" or value > 10000:
    escalate_ticket()
```

---

### Operator Precedence (Order of Operations)

**Python evaluates in this order:**
1. Parentheses `()`
2. Comparisons (`==`, `<`, `>`, etc.)
3. `not`
4. `and`
5. `or`

**Examples:**
```python
# Without parentheses (evaluated left to right with precedence)
if age > 18 and salary > 50000 or is_executive:
    # Evaluates as: (age > 18 and salary > 50000) or is_executive

# With parentheses (clearer intent)
if (age > 18 and salary > 50000) or is_executive:
    # Same result, but more readable

# Different grouping
if age > 18 and (salary > 50000 or is_executive):
    # Now: Must be over 18 AND (have high salary OR be executive)
```

**Best Practice:** Use parentheses to make intent clear, even when not technically required.

---

### Combining Multiple Operators

**You can chain multiple `and` / `or`:**
```python
# All must be true
if age >= 18 and has_license and has_car and has_insurance:
    print("Can drive legally")

# At least one must be true
if payment == "cash" or payment == "card" or payment == "crypto":
    print("Payment accepted")

# Mixed (use parentheses!)
if (age >= 18 and has_license) or is_driving_instructor:
    print("Can drive")
    # True if: (Adult with license) OR (Driving instructor regardless of age)
```

---

### Short-Circuit Evaluation

**Python stops checking once it knows the answer:**

**With `and`:**
```python
if False and expensive_function():
    # expensive_function() NEVER runs
    # Python sees False and knows whole thing is False
    pass
```

**With `or`:**
```python
if True or expensive_function():
    # expensive_function() NEVER runs
    # Python sees True and knows whole thing is True
    pass
```

**Practical use:**
```python
# Check if list exists AND has items (safe)
if user_list and len(user_list) > 0:
    # If user_list is None/empty, len() never runs (prevents error)
    process_users()

# Check if user exists before accessing properties
if user and user.is_active:
    # If user is None, is_active never accessed (prevents error)
    grant_access()
```

---

## 🔧 COMMON ERRORS AND FIXES

### Error 1: Using = Instead of ==
**Symptom:** "invalid syntax" or unexpected behavior
```python
if role = "admin":  # WRONG! Single = is assignment
    give_access()
```

**Fix:** Use == for comparisons
```python
if role == "admin":  # CORRECT! Double == compares
    give_access()
```

---

### Error 2: Missing Parentheses with Complex Logic
**Symptom:** Logic doesn't work as expected
```python
# Ambiguous - hard to read
if age > 18 and salary > 50000 or is_executive:
    # Does this mean: ((age > 18) and (salary > 50000)) or is_executive
    # Or: (age > 18) and ((salary > 50000) or is_executive)?
```

**Fix:** Use parentheses for clarity
```python
if (age > 18 and salary > 50000) or is_executive:
    # Clear: Must meet salary requirements OR be executive
```

---

### Error 3: Redundant Comparisons
**Symptom:** Verbose, unclear code
```python
# Redundant
if is_admin == True:
    give_access()
```

**Fix:** Boolean variables don't need == True
```python
# Cleaner
if is_admin:
    give_access()

# Or for False:
if not is_banned:
    allow_login()
```

---

### Error 4: Wrong Operator Choice
**Symptom:** Logic produces wrong results
```python
# WRONG: Uses AND when should use OR
def check_payment(method):
    if method == "cash" and method == "card":  # Can NEVER be both!
        return "Accepted"
    return "Rejected"
```

**Fix:** Use OR for alternatives
```python
def check_payment(method):
    if method == "cash" or method == "card":
        return "Accepted"
    return "Rejected"
```

---

### Error 5: Not Considering All Combinations
**Symptom:** Some scenarios not handled
```python
# INCOMPLETE: Only handles 2 of 4 possible combinations
def route_email(role, urgency):
    if role == "ceo" and urgency == "high":
        return "urgent tone"
    elif role == "ceo" and urgency == "low":
        return "formal tone"
    # What about colleague + high? colleague + low?
    # Falls through to no explicit handling!
```

**Fix:** Add else clause or handle all combinations
```python
def route_email(role, urgency):
    if role == "ceo" and urgency == "high":
        return "urgent tone"
    elif role == "ceo" and urgency == "low":
        return "formal tone"
    elif role == "colleague" and urgency == "high":
        return "quick tone"
    elif role == "colleague" and urgency == "low":
        return "casual tone"
    else:
        return "professional tone"  # Safety net
```

---

## 💰 BUSINESS VALUE & ROI

### Scenario: Customer Support Routing System

**Client needs:**
- Priority routing based on customer tier AND issue urgency
- VIP treatment for premium customers OR long-term users
- Different SLA targets based on multiple factors

**Amateur Approach (Day 11 skills only):**
```python
# Can only check ONE thing at a time
def route_ticket(customer_tier):
    if customer_tier == "premium":
        return "Priority queue"
    else:
        return "Standard queue"

# Problem: Can't factor in urgency, tenure, or issue type
```

**Professional Approach (Day 12 skills):**
```python
def route_ticket(customer_tier, years_active, urgency, issue_type):
    # VIP routing (tier OR tenure)
    if (customer_tier == "premium" or years_active >= 5) and urgency == "critical":
        return "VIP URGENT - 15 min SLA"
    elif (customer_tier == "premium" or years_active >= 5) and urgency == "high":
        return "VIP Priority - 1 hour SLA"
    elif urgency == "critical" and issue_type == "billing":
        return "Billing URGENT - 30 min SLA"
    elif urgency == "critical":
        return "Standard URGENT - 2 hour SLA"
    else:
        return "Standard queue - 24 hour SLA"
```

**Business Impact:**
- **Customer satisfaction:** VIPs get appropriate priority
- **Retention:** Long-term users feel valued even if they downgrade
- **Revenue protection:** Critical billing issues escalated immediately
- **Resource optimization:** Right-sized response based on multiple factors

**Measurable Results:**
- VIP churn reduced by 40%
- Average response time improved by 60%
- Support team efficiency up 35%
- **ROI:** $50,000/year in prevented churn vs $5,000 implementation cost = 10x return

---

### Scenario: Content Publishing Workflow

**Client needs:**
- Auto-route content based on type AND length
- Different approval workflows for different combinations
- SEO optimization requirements based on multiple factors

**Implementation:**
```python
def route_content(content_type, word_count, has_images):
    if content_type == "blog" and word_count >= 1500 and has_images:
        return "SEO Premium Track - Editor review + SEO check"
    elif content_type == "blog" and word_count >= 1500:
        return "Long-form Track - Editor + suggest images"
    elif content_type == "social" or word_count < 100:
        return "Quick Post Track - Auto-publish"
    elif content_type == "email" and word_count < 300:
        return "Email Track - Spam check only"
    else:
        return "Standard Track - Basic review"
```

**Business Impact:**
- Premium SEO content gets full treatment
- Quick posts auto-publish (no bottleneck)
- Appropriate resources allocated to each content type
- **Time saved:** 20+ hours/week on manual routing

---

## 📊 DECISION-MAKING PATTERNS

### Pattern 1: Strict Requirements (All Must Be True)
**Use Case:** Security, compliance, qualification
```python
if age >= 21 and has_id and not is_banned:
    allow_entry()
```

---

### Pattern 2: Flexible Alternatives (Any Can Be True)
**Use Case:** Payment methods, authentication options, qualification paths
```python
if has_password or has_fingerprint or has_face_id:
    unlock_device()
```

---

### Pattern 3: Tiered Priorities (Ordered Checks)
**Use Case:** VIP routing, support prioritization
```python
if tier == "platinum" or (tier == "gold" and urgent):
    vip_handling()
elif tier == "silver" and not low_priority:
    standard_fast_track()
else:
    standard_queue()
```

---

### Pattern 4: Exclusion Logic (Must Not Be)
**Use Case:** Access control, filtering
```python
if is_verified and not is_suspended and not is_restricted:
    grant_full_access()
```

---

### Pattern 5: Complex Qualification (Mixed Logic)
**Use Case:** Loan approval, program acceptance
```python
if (credit_score >= 700 and income >= 50000) or has_cosigner:
    approve_loan()
```

---

## 🎯 PRACTICE EXERCISES

### Exercise 1: Age & Permission Validator
**Build:** `check_movie_rating(age, has_parent_permission, rating)`

**Requirements:**
- If rating is "G" → always allow
- If rating is "PG" → allow if age >= 13 OR has parent permission
- If rating is "PG-13" → allow if age >= 13
- If rating is "R" → allow if age >= 17 OR (age >= 13 AND has parent permission)
- Else → deny

**Test with:**
```python
print(check_movie_rating(10, False, "G"))        # Allow
print(check_movie_rating(10, True, "PG"))        # Allow (has permission)
print(check_movie_rating(10, False, "PG-13"))    # Deny (too young)
print(check_movie_rating(15, True, "R"))         # Allow (has permission)
print(check_movie_rating(15, False, "R"))        # Deny (needs permission)
```

---

### Exercise 2: Shipping Cost Calculator
**Build:** `calculate_shipping(weight, is_prime, distance)`

**Requirements:**
- If is_prime OR weight < 2 → free shipping
- If weight >= 10 AND distance > 1000 → $50
- If weight >= 10 OR distance > 1000 → $25
- Else → $10

**Test with:**
```python
print(calculate_shipping(1, False, 500))    # Free (weight < 2)
print(calculate_shipping(15, False, 1500))  # $50 (heavy AND far)
print(calculate_shipping(15, False, 500))   # $25 (heavy only)
print(calculate_shipping(5, False, 500))    # $10 (standard)
print(calculate_shipping(20, True, 2000))   # Free (prime)
```

---

### Exercise 3: Meeting Room Booking
**Build:** `can_book_room(room_capacity, attendees, is_executive, has_av_equipment)`

**Requirements:**
- If attendees > room_capacity → cannot book
- If is_executive AND room has_av_equipment → can book (bypass capacity if close)
- If attendees <= room_capacity AND has_av_equipment → can book
- If attendees <= room_capacity * 0.8 → can book (even without AV)
- Else → cannot book

---

## 🔮 DAY 13 PREVIEW: NESTED CONDITIONS

**What's Next:**
You'll learn to put if statements INSIDE other if statements (nesting).

**Example preview:**
```python
if customer_tier == "premium":
    # Nested check INSIDE the premium block
    if urgency == "critical":
        return "VIP URGENT"
    else:
        return "VIP Standard"
else:
    # Nested check INSIDE the non-premium block
    if urgency == "critical":
        return "Standard URGENT"
    else:
        return "Standard Normal"
```

**When to nest vs when to combine:**
- **Combine (Day 12):** When factors are equally important
- **Nest (Day 13):** When one factor determines which sub-factors to check

**This unlocks:** Decision trees, multi-level workflows, complex business logic

---

## 💾 FILE ORGANIZATION

**Your Day 12 Structure:**
```
AI-Operations-Training/
├── Day-10/
│   ├── day10_test.py
│   └── Day-10-Notes.md
├── Day-11/
│   ├── Day-11.py
│   └── Day-11-Notes.md
├── Day-12/
│   ├── day12_combined_logic.py (priority email + VIP support functions)
│   └── Day-12-Notes.md (this file)
└── Libraries/
    └── routing_systems.py (start collecting routing/priority functions)
```

**Professional Tip:**
Day 12 functions are great candidates for your reusable library:
```python
# Libraries/routing_systems.py

def route_by_priority(role, urgency):
    """Reusable priority routing logic"""
    # Your Day 12 code here
    pass

def check_vip_status(tier, tenure):
    """Reusable VIP checking logic"""
    # Your Day 12 code here
    pass

# Future projects import these:
# from Libraries.routing_systems import route_by_priority
```

---

## 🏆 DAY 12 ACHIEVEMENTS

- [x] Mastered `and` operator (all conditions must be true)
- [x] Mastered `or` operator (at least one must be true)
- [x] Learned `not` operator (reverses condition)
- [x] Built multi-factor decision functions
- [x] Combined multiple operators in complex logic
- [x] Understood operator precedence
- [x] Built real-world priority routing systems
- [x] Created VIP qualification logic
- [x] Implemented content classification system

**Grade: A+**

---

## 📝 KEY TAKEAWAYS

1. **`and` = Strict** - ALL conditions must be satisfied (security, compliance)
2. **`or` = Flexible** - AT LEAST ONE condition satisfied (alternatives, options)
3. **Use parentheses** - Make complex logic clear and explicit
4. **Consider all combinations** - Always include else for unexpected cases
5. **Real business logic requires multiple factors** - Single-factor decisions are rare in production

---

## 🎓 PROFESSIONAL PRINCIPLES LEARNED

### Principle 1: Multi-Factor Decision Making
> "Real-world business rules depend on multiple factors, not just one."

Examples: VIP routing, priority queues, access control, content classification

### Principle 2: Defensive Logic Design
> "Always handle the unexpected with else clauses."

Users will pass combinations you didn't anticipate - be prepared.

### Principle 3: Operator Selection Matters
> "Choose `and` vs `or` based on business requirements, not convenience."

Wrong operator = wrong business logic = wrong decisions = unhappy customers.

### Principle 4: Code Readability Through Grouping
> "Use parentheses to make intent crystal clear."

Other developers (or future you) need to understand the logic quickly.

---

## 🔧 TROUBLESHOOTING QUICK REFERENCE

| Error | Cause | Fix |
|-------|-------|-----|
| Logic never true | Used AND when should use OR | Change to OR if alternatives |
| Logic always true | Used OR when should use AND | Change to AND if all required |
| Unexpected results | Operator precedence unclear | Add parentheses for clarity |
| Can't be both | Comparing same variable to 2 values with AND | Use OR for alternatives |
| SyntaxError | Used = instead of == | Use == for comparisons |

---

## 📞 WHEN TO USE WHAT

**Use `and` when:**
- All requirements must be met
- Security/compliance (must satisfy ALL criteria)
- Qualification (must meet ALL standards)

**Use `or` when:**
- Alternatives/options (any one works)
- Multiple paths to same outcome
- Flexible qualification (meet at least one)

**Use `not` when:**
- Checking for absence/negation
- Exclusion logic (not banned, not expired)
- Clearer than `== False`

**Use combined `and`/`or` when:**
- Complex business rules with multiple factors
- Decision trees with branches
- Priority/tiering systems

---

## 🎯 NEXT SESSION

**Day 13: Nested Conditions & Decision Trees**

**You'll build:**
- Multi-level decision structures
- Conditions inside conditions
- Complex workflow routing

**See you then!** 🚀

---

**Created:** Day 12 of AI Operations Training  
**Your Progress:** Month 1, Week 2 (Days 8-14)  
**Next Session:** Day 13 - Nested Conditions

**You're not just coding. You're building business intelligence systems.** 💼🔥
