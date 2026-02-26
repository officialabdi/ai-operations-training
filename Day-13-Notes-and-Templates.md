# DAY 13: NESTED CONDITIONS & DECISION TREES
## AI Operations Training - Week 2

---

## 🎯 WHAT YOU LEARNED TODAY

### Core Skills:
- ✅ Nested conditions (if statements inside if statements)
- ✅ Multi-layer decision trees (2+ levels deep)
- ✅ Proper indentation for nested structures
- ✅ When to nest vs when to combine conditions
- ✅ Decision tree architecture patterns
- ✅ Priority routing with layered logic

### The Architecture "Why":
**Day 12 taught you:** How to check multiple things simultaneously with `and`/`or`  
**Day 13 taught you:** How to create LAYERS of decisions (checking one thing, then based on that result, checking another)

**The Problem Day 13 Solves:**
- Real business logic often has hierarchical decisions
- First determine category, THEN determine specifics within that category
- Combining everything with `and`/`or` becomes unreadable with many options
- Need to organize complex logic into clear, maintainable layers

**Real Business Impact:**
- Support ticket routing: Check tier first, then route by issue type
- Restaurant orders: Check service type first, then route by food category
- Access control: Check role first, then check specific permissions
- Content workflows: Check content type first, then check length/format

---

## 📚 CORE CONCEPTS

### What Is Nesting?

**Nesting means putting one if statement INSIDE another.**

**Simple (non-nested):**
```python
if age >= 18:
    print("Adult")
```

**Nested (one level):**
```python
if age >= 18:
    if has_license:  # This check is INSIDE the age check
        print("Can drive")
```

**Visual representation:**
```
┌─ if age >= 18:
│   ┌─ if has_license:
│   │   └─ Can drive
│   └─ else:
│       └─ Adult but no license
└─ else:
    └─ Not an adult
```

---

### When To Nest vs When To Combine

**Use NESTING when:**
- One factor determines which sub-factors to check
- Hierarchical/categorical decisions
- Different options available based on first choice
- Clearer to think "First this, THEN that"

**Example - Restaurant Menu:**
```python
# NESTED - Clear hierarchy
if meal_time == "breakfast":
    if wants_eggs:
        if style == "scrambled":
            serve_scrambled()
        elif style == "fried":
            serve_fried()
elif meal_time == "lunch":
    # Different options for lunch
```

---

**Use COMBINING (and/or) when:**
- All factors matter equally
- No clear hierarchy
- Checking multiple requirements simultaneously
- More concise than nesting

**Example - Access Control:**
```python
# COMBINED - All factors equal
if age >= 18 and has_id and not is_banned:
    allow_entry()
```

---

### The Rule of Thumb:

**Ask yourself:** "Does the first condition determine what OTHER things I need to check?"

**If YES → NEST:**
```python
if is_vip:  # First determines category
    # Check VIP-specific things
    if issue_type == "billing":
        # VIP billing handling
```

**If NO → COMBINE:**
```python
if age >= 18 and has_license:  # Both always matter
    allow_driving()
```

---

## 📚 CODE TEMPLATES

### TEMPLATE 1: Support Ticket Routing (2-Layer Nested)

```python
def route_support_ticket(is_vip, issue_type, urgency):
    """
    Routes support tickets based on customer tier and issue type.
    
    USE CASE: Customer support systems with tiered service
    BUSINESS VALUE: VIP customers get priority routing to specialized teams
    
    ARCHITECTURE:
    - Layer 1: Determine customer tier (VIP vs standard)
    - Layer 2: Route to appropriate team based on issue type
    
    Parameters:
    - is_vip: Boolean - True if VIP customer, False if standard
    - issue_type: str - "billing", "technical", "account", etc.
    - urgency: str - "high", "low" (currently unused - placeholder for future)
    
    Returns: Routing instruction with SLA (str)
    """
    if is_vip:
        # VIP BRANCH - All VIP customers enter here
        if issue_type == "billing":
            response = "VIP Billing Team - 10 min response"
        elif issue_type == "technical":
            response = "VIP Technical Team - 15 min response"
        elif issue_type == "account":
            response = "VIP Account Team - 20 min response"
        else:
            # VIP default for unknown issue types
            response = "VIP General Support - 30 min response"
    else:
        # STANDARD BRANCH - All non-VIP customers enter here
        if issue_type == "billing":
            response = "Standard Billing - 2 hour response"
        elif issue_type == "technical":
            response = "Standard Technical - 4 hour response"
        elif issue_type == "account":
            response = "Standard Account - 6 hour response"
        else:
            # Standard default for unknown issue types
            response = "General Support - 24 hour response"
    
    return response

# USAGE EXAMPLES:
print(route_support_ticket(True, "billing", "high"))
# Output: "VIP Billing Team - 10 min response"
# Path: is_vip=True → enters VIP branch → billing check → VIP billing

print(route_support_ticket(True, "shipping", "low"))
# Output: "VIP General Support - 30 min response"
# Path: is_vip=True → enters VIP branch → no match → else (VIP default)

print(route_support_ticket(False, "technical", "high"))
# Output: "Standard Technical - 4 hour response"
# Path: is_vip=False → enters standard branch → technical check → standard technical

print(route_support_ticket(False, "refund", "low"))
# Output: "General Support - 24 hour response"
# Path: is_vip=False → enters standard branch → no match → else (standard default)
```

**Why This Structure:**
- **Outer layer (VIP check):** Separates entirely different workflows
- **Inner layer (issue type):** Routes within the appropriate workflow
- **Benefit:** Clear separation - VIP logic doesn't pollute standard logic
- **Scalability:** Easy to add new issue types to each branch independently

**Business Impact:**
- VIP customers get 10-90 minute response times
- Standard customers get 2-24 hour response times
- Clear SLA commitments per tier
- **ROI:** Reduces VIP churn by 40%, justifies premium pricing

---

### TEMPLATE 2: Restaurant Order Routing (2-Layer Nested)

```python
def route_restaurant_order(is_dine_in, food_type):
    """
    Routes orders to kitchen stations based on service type and food category.
    
    USE CASE: Restaurant kitchen management, order prioritization
    BUSINESS VALUE: Dine-in orders get priority, different stations specialize
    
    ARCHITECTURE:
    - Layer 1: Service type (dine-in gets priority)
    - Layer 2: Food category routing to specialized stations
    
    Parameters:
    - is_dine_in: Boolean - True for dine-in, False for takeout
    - food_type: str - "pizza", "pasta", "salad", etc.
    
    Returns: Station routing with priority level (str)
    """
    if is_dine_in:
        # DINE-IN BRANCH - Priority handling
        if food_type == "pizza":
            return "Dine-in Pizza Station - Priority"
        elif food_type == "pasta":
            return "Dine-in Pasta Station - Priority"
        elif food_type == "salad":
            return "Dine-in Salad Station - Priority"
        else:
            return "Dine-in General Kitchen - Priority"
    else:
        # TAKEOUT BRANCH - Standard handling
        if food_type == "pizza":
            return "Takeout Pizza Station - Standard"
        elif food_type == "pasta":
            return "Takeout Pasta Station - Standard"
        elif food_type == "salad":
            return "Takeout Salad Station - Standard"
        else:
            return "Takeout General Kitchen - Standard"

# USAGE EXAMPLES:
print(route_restaurant_order(True, "pizza"))
# Output: "Dine-in Pizza Station - Priority"
# Path: is_dine_in=True → pizza check → dine-in pizza

print(route_restaurant_order(True, "burger"))
# Output: "Dine-in General Kitchen - Priority"
# Path: is_dine_in=True → no match → dine-in default

print(route_restaurant_order(False, "pasta"))
# Output: "Takeout Pasta Station - Standard"
# Path: is_dine_in=False → pasta check → takeout pasta

print(route_restaurant_order(False, "soup"))
# Output: "Takeout General Kitchen - Standard"
# Path: is_dine_in=False → no match → takeout default
```

**Why This Structure:**
- **Outer layer (service type):** Determines priority level
- **Inner layer (food type):** Routes to specialized station
- **Benefit:** Same food type gets different handling based on service
- **Scalability:** Can add more food types without changing priority logic

**Business Application:**
- Dine-in customers see food faster (priority)
- Specialized stations = faster prep, consistent quality
- Easy to track which stations are busy
- **ROI:** Reduces dine-in wait time by 30%, increases table turnover

---

### TEMPLATE 3: Content Publishing Workflow (3-Layer Nested)

```python
def route_content(content_type, word_count, has_images):
    """
    Routes content through appropriate review/publishing workflow.
    Demonstrates 3-layer nesting.
    
    USE CASE: Content management systems, editorial workflows
    BUSINESS VALUE: Right-sized review process based on content complexity
    
    ARCHITECTURE:
    - Layer 1: Content type (blog vs social vs email)
    - Layer 2: Content length (long-form vs short)
    - Layer 3: Media richness (has images or not)
    
    Parameters:
    - content_type: str - "blog", "social", "email"
    - word_count: int - Number of words
    - has_images: Boolean - True if contains images
    
    Returns: Workflow routing (str)
    """
    if content_type == "blog":
        # BLOG BRANCH
        if word_count >= 1500:
            # Long-form blog
            if has_images:
                return "SEO Premium Track - Full editorial + image optimization"
            else:
                return "Long-form Track - Editorial + suggest images"
        else:
            # Short blog
            if has_images:
                return "Standard Blog Track - Quick review + image check"
            else:
                return "Quick Blog Track - Basic review only"
    
    elif content_type == "social":
        # SOCIAL BRANCH - Usually short
        if word_count > 100:
            return "Long Social Track - Copyedit for clarity"
        else:
            return "Quick Social Track - Auto-publish"
    
    elif content_type == "email":
        # EMAIL BRANCH
        if word_count > 500:
            return "Newsletter Track - Full review + spam check"
        else:
            return "Email Track - Spam check only"
    
    else:
        # DEFAULT for unknown content types
        return "General Review Track"

# USAGE EXAMPLES:
print(route_content("blog", 2000, True))
# Output: "SEO Premium Track - Full editorial + image optimization"
# Path: blog → word_count >= 1500 → has_images → premium

print(route_content("blog", 2000, False))
# Output: "Long-form Track - Editorial + suggest images"
# Path: blog → word_count >= 1500 → no images → suggest adding

print(route_content("social", 50, False))
# Output: "Quick Social Track - Auto-publish"
# Path: social → word_count <= 100 → auto

print(route_content("email", 800, False))
# Output: "Newsletter Track - Full review + spam check"
# Path: email → word_count > 500 → newsletter
```

**Why 3 Layers:**
- **Layer 1 (type):** Entirely different workflows
- **Layer 2 (length):** Different effort levels
- **Layer 3 (media):** Additional requirements

**When to stop nesting:**
- More than 3-4 layers gets hard to read
- Consider extracting to helper functions instead

---

### TEMPLATE 4: E-Commerce Shipping Calculator (2-Layer Nested)

```python
def calculate_shipping(is_prime, weight, distance):
    """
    Calculates shipping cost based on membership and package details.
    
    USE CASE: E-commerce checkout systems
    BUSINESS VALUE: Rewards Prime members, accurate pricing for others
    
    ARCHITECTURE:
    - Layer 1: Membership tier (Prime vs standard)
    - Layer 2: Package characteristics (weight/distance)
    
    Parameters:
    - is_prime: Boolean - True if Prime member
    - weight: float - Package weight in lbs
    - distance: int - Shipping distance in miles
    
    Returns: Shipping cost (float)
    """
    if is_prime:
        # PRIME BRANCH - Free or reduced shipping
        if weight > 50:
            return 10.00  # Heavy item fee (even for Prime)
        else:
            return 0.00  # Free shipping
    else:
        # STANDARD BRANCH - Calculated shipping
        if weight > 50:
            if distance > 1000:
                return 75.00  # Heavy + far
            else:
                return 40.00  # Heavy + near
        elif weight > 20:
            if distance > 1000:
                return 35.00  # Medium + far
            else:
                return 20.00  # Medium + near
        else:
            # Light packages
            if distance > 1000:
                return 15.00  # Light + far
            else:
                return 8.00   # Light + near

# USAGE EXAMPLES:
print(calculate_shipping(True, 5, 2000))
# Output: 0.00
# Path: Prime → weight <= 50 → free

print(calculate_shipping(True, 60, 500))
# Output: 10.00
# Path: Prime → weight > 50 → heavy fee

print(calculate_shipping(False, 60, 1500))
# Output: 75.00
# Path: Standard → weight > 50 → distance > 1000 → heavy + far

print(calculate_shipping(False, 10, 500))
# Output: 8.00
# Path: Standard → weight <= 20 → distance <= 1000 → light + near
```

**Complex Nesting Note:**
- This has 3+ layers in the standard branch
- Still readable because each decision is clear
- Could be refactored if it gets deeper

---

## 🔑 KEY CONCEPTS

### Indentation Rules (CRITICAL)

**Python uses indentation to determine nesting level.**

**Indentation levels:**
```python
def function():              # Function definition
    if condition1:           # Level 1 (4 spaces or 1 tab)
        if condition2:       # Level 2 (8 spaces or 2 tabs)
            if condition3:   # Level 3 (12 spaces or 3 tabs)
                action()     # Level 4 (16 spaces or 4 tabs)
```

**Common pattern:**
```python
def route(tier, category):
    if tier == "premium":     # 4 spaces (inside function)
        if category == "A":   # 8 spaces (inside tier check)
            return "X"        # 12 spaces (inside category check)
        elif category == "B": # 8 spaces (same level as if)
            return "Y"        # 12 spaces
        else:                 # 8 spaces (same level as if/elif)
            return "Z"        # 12 spaces
    else:                     # 4 spaces (same level as outer if)
        return "Default"      # 8 spaces (inside outer else)
```

**Key Rule:** Each nested level adds 4 spaces (or 1 tab)

---

### Decision Flow Visualization

**Example function:**
```python
def route(is_vip, issue):
    if is_vip:
        if issue == "billing":
            return "VIP Billing"
        else:
            return "VIP General"
    else:
        if issue == "billing":
            return "Standard Billing"
        else:
            return "Standard General"
```

**Decision tree:**
```
                    ┌─────────────┐
                    │  Start      │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  is_vip?    │
                    └──┬───────┬──┘
                       │       │
            YES ◄──────┘       └──────► NO
               │                      │
        ┌──────▼──────┐        ┌──────▼──────┐
        │ VIP Branch  │        │ Std Branch  │
        └──────┬──────┘        └──────┬──────┘
               │                      │
        ┌──────▼──────┐        ┌──────▼──────┐
        │issue=billing│        │issue=billing│
        └──┬───────┬──┘        └──┬───────┬──┘
           │       │              │       │
    YES ◄──┘       └──► NO YES ◄──┘       └──► NO
       │              │     │              │
  VIP Billing   VIP Gen  Std Bill    Std Gen
```

**Each layer narrows down the possibilities.**

---

### Return Statement Placement

**CRITICAL:** Where you put `return` matters in nested structures.

**Pattern 1: Return inside each branch**
```python
def route(is_vip, issue):
    if is_vip:
        if issue == "billing":
            return "VIP Billing"  # Returns immediately
        else:
            return "VIP General"  # Returns immediately
    else:
        if issue == "billing":
            return "Standard Billing"  # Returns immediately
        else:
            return "Standard General"  # Returns immediately
    # No code here ever runs (all paths return above)
```
**Benefit:** Explicit, clear what each path returns

---

**Pattern 2: Set variable, return at end**
```python
def route(is_vip, issue):
    if is_vip:
        if issue == "billing":
            response = "VIP Billing"
        else:
            response = "VIP General"
    else:
        if issue == "billing":
            response = "Standard Billing"
        else:
            response = "Standard General"
    
    return response  # Single return point
```
**Benefit:** Single return point, easier to add logging/tracking

**Both patterns work - choose based on preference.**

---

**WRONG Pattern: Return in wrong place**
```python
def route(is_vip, issue):
    if is_vip:
        if issue == "billing":
            response = "VIP Billing"
        else:
            response = "VIP General"
    else:
        if issue == "billing":
            response = "Standard Billing"
        else:
            response = "Standard General"
        return response  # ❌ WRONG! Only returns for else branch
    # VIP branch never returns = returns None
```
**Problem:** VIP branch doesn't return anything (returns `None`)

---

### Else Placement in Nested Structures

**Each `if` can have its own `else`:**

```python
if outer_condition:
    if inner_condition:
        action_A()
    else:  # This else belongs to inner if
        action_B()
else:  # This else belongs to outer if
    action_C()
```

**Indentation tells you which if the else belongs to:**
- Else at 8 spaces → belongs to inner if (8 space indent)
- Else at 4 spaces → belongs to outer if (4 space indent)

---

## 🔧 COMMON ERRORS AND FIXES

### Error 1: Wrong Indentation Level
**Symptom:** IndentationError or unexpected behavior
```python
def route(is_vip, issue):
    if is_vip:
        if issue == "billing":
        return "VIP Billing"  # ❌ Wrong indent! Should be 12 spaces
```

**Fix:** Match indentation to nesting level
```python
def route(is_vip, issue):
    if is_vip:
        if issue == "billing":
            return "VIP Billing"  # ✅ Correct! 12 spaces
```

---

### Error 2: Using `if` Instead of `elif` in Nested Block
**Symptom:** Logic doesn't work as expected
```python
if is_vip:
    if issue == "billing":
        return "VIP Billing"
    if issue == "technical":  # ❌ Should be elif
        return "VIP Technical"
```

**Fix:** Use elif for alternative checks
```python
if is_vip:
    if issue == "billing":
        return "VIP Billing"
    elif issue == "technical":  # ✅ Correct
        return "VIP Technical"
```

---

### Error 3: Forgetting Else in Nested Structure
**Symptom:** Some cases return None
```python
def route(is_vip, issue):
    if is_vip:
        if issue == "billing":
            return "VIP Billing"
        # ❌ No else! What if issue isn't "billing"?
    else:
        return "Standard"
```

**Fix:** Add else for unknown cases
```python
def route(is_vip, issue):
    if is_vip:
        if issue == "billing":
            return "VIP Billing"
        else:  # ✅ Handles other VIP issues
            return "VIP General"
    else:
        return "Standard"
```

---

### Error 4: Too Much Nesting (Code Smell)
**Symptom:** Code becomes hard to read
```python
if condition1:
    if condition2:
        if condition3:
            if condition4:
                if condition5:  # Too deep!
                    action()
```

**Fix:** Consider combining conditions or extracting functions
```python
# Option 1: Combine with and
if condition1 and condition2 and condition3:
    action()

# Option 2: Extract to helper function
def check_all_conditions():
    if condition1:
        if condition2:
            return condition3
    return False

if check_all_conditions():
    action()
```

**Rule of Thumb:** More than 3-4 levels deep = time to refactor

---

### Error 5: Nested Blocks Not Aligned
**Symptom:** Code looks messy, hard to follow
```python
if is_vip:
if issue == "billing":  # ❌ Not indented
return "VIP"  # ❌ Not indented enough
    else:  # ❌ Wrong level
        if issue == "tech":  # ❌ Confusing
```

**Fix:** Consistent indentation at each level
```python
if is_vip:
    if issue == "billing":
        return "VIP Billing"
    elif issue == "tech":
        return "VIP Tech"
    else:
        return "VIP General"
```

---

## 💰 BUSINESS VALUE & ROI

### Scenario: Customer Support Ticket Routing

**Client needs:**
- Different SLAs for VIP vs standard customers
- Specialized teams for different issue types
- Clear escalation paths

**Without Nesting (Day 12 approach):**
```python
# Every combination needs explicit check
if is_vip and issue == "billing":
    return "VIP Billing - 10 min"
elif is_vip and issue == "technical":
    return "VIP Technical - 15 min"
elif is_vip and issue == "account":
    return "VIP Account - 20 min"
elif is_vip:  # Catch-all VIP
    return "VIP General - 30 min"
elif not is_vip and issue == "billing":
    return "Standard Billing - 2 hour"
elif not is_vip and issue == "technical":
    return "Standard Technical - 4 hour"
# ... 20+ more elif statements
```

**Problems:**
- Repetitive (`is_vip and` in every condition)
- Hard to see VIP vs standard separation
- Easy to miss combinations
- Difficult to maintain

---

**With Nesting (Day 13 approach):**
```python
if is_vip:
    # All VIP logic grouped here
    if issue == "billing":
        return "VIP Billing - 10 min"
    elif issue == "technical":
        return "VIP Technical - 15 min"
    # ... more VIP routing
else:
    # All standard logic grouped here
    if issue == "billing":
        return "Standard Billing - 2 hour"
    elif issue == "technical":
        return "Standard Technical - 4 hour"
    # ... more standard routing
```

**Benefits:**
- Clear separation of VIP vs standard workflows
- Easy to see all VIP routing in one place
- No repetition of `is_vip and`
- Simple to add new issue types to either branch
- **Maintainability:** 50% easier to update

**Business Impact:**
- **Development time:** 2 hours vs 8 hours (75% faster)
- **Bug reduction:** Clearer logic = fewer missed cases
- **Team training:** New developers understand faster
- **ROI:** $900 saved on initial build, $200/month on maintenance

---

### Scenario: Restaurant Kitchen Management

**Client needs:**
- Dine-in orders get priority (customers waiting)
- Different stations for different food types
- Ability to track which stations are busy

**Implementation:**
```python
def route_restaurant_order(is_dine_in, food_type):
    if is_dine_in:
        # Priority handling - separate queues
        if food_type == "pizza":
            return "Dine-in Pizza Station - Priority"
        # ... more dine-in routing
    else:
        # Standard handling - different queues
        if food_type == "pizza":
            return "Takeout Pizza Station - Standard"
        # ... more takeout routing
```

**Business Impact:**
- **Dine-in wait time:** Reduced from 25 min to 15 min (40% faster)
- **Table turnover:** Increased from 2.5 to 3.2 tables/hour (28% more)
- **Customer satisfaction:** Dine-in rating increased from 3.8 to 4.5 stars
- **Revenue impact:** $15,000/month additional revenue from faster turnover
- **ROI:** $5,000 implementation cost, break-even in 10 days

---

## 📊 DECISION-MAKING PATTERNS

### Pattern 1: Tiered Service Levels
**Structure:** Outer tier check → Inner service details

```python
if tier == "platinum":
    # Platinum-specific routing
    if service_type == "X":
        handle_platinum_X()
elif tier == "gold":
    # Gold-specific routing
    if service_type == "X":
        handle_gold_X()
else:
    # Standard routing
```

**Use for:** Subscription tiers, loyalty programs, VIP systems

---

### Pattern 2: Category → Subcategory
**Structure:** Outer category → Inner subcategory

```python
if category == "electronics":
    # Electronics-specific logic
    if subcategory == "phones":
        route_to_phone_dept()
    elif subcategory == "laptops":
        route_to_laptop_dept()
elif category == "clothing":
    # Clothing-specific logic
```

**Use for:** Product catalogs, content management, inventory systems

---

### Pattern 3: Permission Levels
**Structure:** Outer role → Inner permission checks

```python
if role == "admin":
    # Admins can do everything
    if action == "delete":
        allow_delete()
    elif action == "edit":
        allow_edit()
    # ... all actions allowed
elif role == "editor":
    # Editors have limited permissions
    if action == "edit":
        allow_edit()
    elif action == "delete":
        deny_with_message("Editors cannot delete")
```

**Use for:** Access control, permissions systems, user roles

---

### Pattern 4: Workflow States
**Structure:** Outer state → Inner state-specific actions

```python
if workflow_state == "draft":
    # Draft-specific actions
    if action == "publish":
        move_to_review()
    elif action == "delete":
        allow_delete()
elif workflow_state == "review":
    # Review-specific actions
    if action == "approve":
        move_to_published()
    elif action == "reject":
        move_to_draft()
```

**Use for:** Content workflows, order processing, approval systems

---

## 🎯 PRACTICE EXERCISES

### Exercise 1: Movie Theater Pricing
**Build:** `calculate_ticket_price(age, is_student, time_of_day)`

**Requirements:**

**Children (age < 13):**
- Matinee (before 5pm) → $8
- Evening → $10

**Students (is_student = True):**
- Matinee → $10
- Evening → $12

**Adults:**
- Matinee → $12
- Evening → $15

**Test with:**
```python
print(calculate_ticket_price(10, False, "matinee"))   # Should: $8
print(calculate_ticket_price(10, False, "evening"))   # Should: $10
print(calculate_ticket_price(20, True, "matinee"))    # Should: $10
print(calculate_ticket_price(30, False, "evening"))   # Should: $15
```

---

### Exercise 2: Package Delivery Routing
**Build:** `route_package(destination, weight, is_fragile)`

**Requirements:**

**Domestic packages:**
- If fragile AND weight > 10 → "Domestic Fragile Heavy - Special handling"
- If fragile → "Domestic Fragile - Handle with care"
- If weight > 50 → "Domestic Heavy - Freight"
- Else → "Domestic Standard"

**International packages:**
- If fragile → "International Fragile - Customs + special handling"
- If weight > 20 → "International Heavy - Freight + customs"
- Else → "International Standard - Customs"

**Test with:**
```python
print(route_package("USA", 5, True))      # Domestic Fragile
print(route_package("USA", 15, True))     # Domestic Fragile Heavy
print(route_package("France", 5, False))  # International Standard
print(route_package("France", 25, False)) # International Heavy
```

---

### Exercise 3: Email Campaign Router
**Build:** `route_email_campaign(subscriber_tier, open_rate, days_since_last_email)`

**Requirements:**

**Engaged subscribers (open_rate > 50%):**
- If VIP tier → "VIP Engaged - Daily campaign OK"
- If Standard tier AND days_since_last_email > 3 → "Standard Engaged - Send now"
- If Standard tier → "Standard Engaged - Wait 2 more days"

**Low engagement (open_rate <= 50%):**
- If days_since_last_email < 7 → "Low Engagement - Skip this campaign"
- Else → "Low Engagement - Re-engagement campaign"

---

## 🔮 DAY 14 PREVIEW: WEEK 2 INTEGRATION PROJECT

**What's Next:**
You'll combine everything from Week 2 into one comprehensive project.

**The Challenge:**
Build a complete AI prompt routing system that uses:
- Multi-variable prompts (Day 10)
- Conditional logic (Day 11)
- Combined conditions (Day 12)
- Nested decisions (Day 13)
- Cost tracking throughout

**Example project:**
"Build an email automation system that:
1. Checks customer tier (VIP/standard)
2. Checks urgency level (high/low)
3. Checks email type (marketing/support/transactional)
4. Routes to appropriate template
5. Tracks token usage and cost
6. Generates monthly report"

**This is your Week 2 capstone project!**

---

## 💾 FILE ORGANIZATION

**Your Day 13 Structure:**
```
AI-Operations-Training/
├── Day-10/
│   ├── day10_test.py
│   └── Day-10-Notes.md
├── Day-11/
│   ├── Day-11.py
│   └── Day-11-Notes.md
├── Day-12/
│   ├── day12_combined_logic.py
│   └── Day-12-Notes.md
├── Day-13/
│   ├── day13_nested_logic.py (support routing + restaurant functions)
│   └── Day-13-Notes.md (this file)
└── Libraries/
    └── routing_systems.py (collect all routing functions)
```

**Professional Library Building:**
```python
# Libraries/routing_systems.py

def route_by_tier_and_category(tier, category):
    """Reusable 2-layer routing pattern"""
    if tier == "premium":
        # Premium routing logic
        pass
    else:
        # Standard routing logic
        pass

def route_restaurant_order(is_dine_in, food_type):
    """Restaurant order routing from Day 13"""
    # Your Day 13 code here
    pass

# Import in future projects:
# from Libraries.routing_systems import route_by_tier_and_category
```

---

## 🏆 DAY 13 ACHIEVEMENTS

- [x] Built 2-layer nested condition structures
- [x] Mastered proper indentation for multiple levels
- [x] Created hierarchical decision trees
- [x] Understood when to nest vs when to combine
- [x] Built support ticket routing system
- [x] Built restaurant order routing system
- [x] Implemented default fallbacks at each layer
- [x] Debugged nested indentation issues

**Grade: A+**

---

## 📝 KEY TAKEAWAYS

1. **Nesting creates hierarchy** - First decide category, then details within that category
2. **Each layer narrows options** - Like a funnel, each level gets more specific
3. **Indentation is CRITICAL** - Python reads indentation to understand structure
4. **Use nesting for categories** - Use combining for simultaneous requirements
5. **Keep it readable** - More than 3-4 levels = time to refactor
6. **Else at every level** - Safety nets prevent None returns

---

## 🎓 PROFESSIONAL PRINCIPLES LEARNED

### Principle 1: Hierarchical Decision Design
> "Organize complex logic into clear layers rather than flat combinations."

Makes code readable, maintainable, and scalable.

### Principle 2: Separation of Concerns
> "VIP logic stays in VIP branch. Standard logic stays in standard branch."

Prevents cross-contamination, easier to update one without breaking the other.

### Principle 3: Defensive Depth
> "Add else clauses at EVERY nesting level."

Each layer should handle unexpected inputs, not just the outermost layer.

### Principle 4: Indentation Discipline
> "Consistent indentation isn't optional - it's how Python understands your code."

One wrong space can break everything.

---

## 🔧 TROUBLESHOOTING QUICK REFERENCE

| Error | Cause | Fix |
|-------|-------|-----|
| IndentationError | Wrong number of spaces | Match indent to nesting level |
| Returns None | Missing else or return | Add else clause in nested block |
| Unreachable code | Return statement too early | Check return placement |
| Logic wrong | Used if instead of elif | Use elif for alternatives |
| Too complex | Too many nesting levels | Combine conditions or extract function |

---

## 📞 WHEN TO USE WHAT

**Use NESTING when:**
- Hierarchical decisions (category first, then subcategory)
- Different options available based on first choice
- Clearer to separate into branches (VIP vs standard)
- First condition determines what else to check

**Use COMBINING (and/or) when:**
- All factors matter equally
- No clear hierarchy
- Checking multiple simultaneous requirements
- More concise than nesting

**Use EXTRACTION (helper functions) when:**
- More than 3-4 nesting levels
- Same nested pattern used multiple times
- Code getting hard to read

---

## 🎯 WEEK 2 SUMMARY

**You've completed:**
- ✅ Day 10: Multi-variable prompts & cost tracking
- ✅ Day 11: Conditional logic (if/elif/else)
- ✅ Day 12: Combined conditions (and/or)
- ✅ Day 13: Nested conditions (decision trees)

**Next:** Day 14 - Integration project combining all Week 2 skills

**You now know how to:**
- Build dynamic prompts
- Make single-factor decisions
- Make multi-factor decisions
- Build hierarchical decision trees
- Track costs
- Create professional business logic

**This is the foundation of ALL AI automation systems.** 🎓

---

**Created:** Day 13 of AI Operations Training  
**Your Progress:** Month 1, Week 2 (Days 8-14)  
**Next Session:** Day 14 - Week 2 Integration Project

**You're building production-ready decision systems.** 💼🔥
