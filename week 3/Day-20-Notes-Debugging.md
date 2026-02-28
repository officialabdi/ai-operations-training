# DAY 20: DEBUGGING TECHNIQUES
## AI Operations Training - Week 3, Day 6

---

## what you learned today

### core skills:
- print statement debugging
- systematic debugging process (5 steps)
- finding bugs in code
- fixing indentation errors
- cleaning up debug code
- understanding code flow

### the architecture "why":
**days 15-19 taught you:** error handling and logging  
**day 20 teaches you:** how to find and fix bugs systematically

**the problem day 20 solves:**
```python
# amateur approach
# code doesn't work
# you stare at it for 2 hours
# randomly change things hoping it fixes
# give up

# professional approach
# code doesn't work
# add strategic debug statements
# find exact line where bug occurs
# fix it in 10 minutes
# remove debug statements
```

**real business impact:**
- fix client issues in minutes instead of hours
- save money (your time = money)
- look professional
- debug production systems confidently
- charge hourly for bug fixes (75 euro/hour in ireland)

---

## the key concept: systematic debugging

### what is debugging?

**debugging = finding and fixing errors in your code**

**two types of bugs:**
1. **syntax errors** - python can't run your code (typos, missing colons)
2. **logic errors** - code runs but gives wrong results (what we learned today)

**syntax errors are easy:**
```python
if x = 5  # syntax error - missing colon
    print("hello")
```
python tells you immediately: "syntaxerror: invalid syntax"

**logic errors are hard:**
```python
# code runs but calculates wrong discount
discount = price * discount_percent  # bug: should divide by 100 first
# no error message, just wrong results
```

---

## core concept 1: print statement debugging

### the method:

**add print statements to see what's happening inside your code**

```python
def calculate_discount(price, discount_percent):
    """calculate final price after discount."""
    # add debug prints to track values
    print(f"debug: price = {price}")
    print(f"debug: discount_percent = {discount_percent}")
    
    discount_amount = price * discount_percent
    print(f"debug: discount_amount = {discount_amount}")
    
    final_price = price - discount_amount
    print(f"debug: final_price = {final_price}")
    
    return final_price
```

### example from today:

**original buggy code:**
```python
def calculate_discount(price, discount_percent):
    discount_amount = price * discount_percent
    final_price = price - discount_amount
    return final_price

result = calculate_discount(100, 20)
# result: -1900 (WRONG - expected 80)
```

**added debug prints:**
```python
def calculate_discount(price, discount_percent):
    print(f"debug: price = {price}")
    print(f"debug: discount_percent = {discount_percent}")
    
    discount_amount = price * discount_percent
    print(f"debug: discount_amount = {discount_amount}")  # shows 2000!
    
    final_price = price - discount_amount
    print(f"debug: final_price = {final_price}")
    
    return final_price
```

**output revealed the bug:**
```
debug: price = 100
debug: discount_percent = 20
debug: discount_amount = 2000  ← THE BUG! should be 20
debug: final_price = -1900
```

**the fix:**
```python
def calculate_discount(price, discount_percent):
    discount_decimal = discount_percent / 100  # convert 20% to 0.20
    discount_amount = price * discount_decimal
    final_price = price - discount_amount
    return final_price

result = calculate_discount(100, 20)
# result: 80.0 (CORRECT)
```

### when to use print statement debugging:

**use print statements when:**
- quick debugging needed
- simple functions (under 50 lines)
- you have a guess where the bug is
- working with variables and calculations
- need to see value changes over time

**don't use print statements when:**
- debugging complex systems with many functions
- need to pause execution and inspect
- working with someone else's code
- need to step through code line by line

---

## core concept 2: the 5-step debugging process

**professional developers follow this systematic approach:**

### step 1: reproduce the bug

**make the bug happen consistently**

```python
# can you make it fail every time?
result = calculate_discount(100, 20)
# yes - always gives wrong answer

# or does it only fail sometimes?
result = process_order(data)
# sometimes works, sometimes fails (harder to debug)
```

**if you can't reproduce it consistently, it's much harder to fix**

### step 2: isolate the problem

**which function is broken?**

```python
# you have 3 functions:
def calculate_discount(price, discount):
    # ...

def calculate_tax(price):
    # ...

def calculate_total(price, discount):
    discounted = calculate_discount(price, discount)
    tax = calculate_tax(price)
    return discounted + tax

# result is wrong - which function has the bug?
# test each one individually
```

**isolate by testing functions independently:**
```python
# test function 1
print(calculate_discount(100, 20))  # returns 80 - correct

# test function 2
print(calculate_tax(100))  # returns 23 - correct

# test function 3
print(calculate_total(100, 20))  # returns 103 - WRONG
# bug must be in calculate_total
```

### step 3: add print statements

**add strategic prints to see what's happening**

```python
def calculate_total(price, discount_percent):
    print(f"debug: starting with price = {price}")
    
    discounted_price = calculate_discount(price, discount_percent)
    print(f"debug: after discount = {discounted_price}")
    
    tax = calculate_tax(price)  # bug is here
    print(f"debug: tax calculated on ${price} = ${tax}")
    
    total = discounted_price + tax
    print(f"debug: total = {discounted_price} + {tax} = {total}")
    
    return total
```

**output shows the bug:**
```
debug: starting with price = 100
debug: after discount = 80.0
debug: tax calculated on $100 = $23.0  ← BUG! should calculate tax on $80
debug: total = 80.0 + 23.0 = 103.0
```

### step 4: form a hypothesis

**based on debug output, guess what's wrong**

```python
# hypothesis: "tax is being calculated on original price instead of discounted price"

# the bug:
tax = calculate_tax(price)  # using original price

# the fix:
tax = calculate_tax(discounted_price)  # use discounted price
```

### step 5: test the fix

**apply the fix and verify it works**

```python
def calculate_total(price, discount_percent):
    discounted_price = calculate_discount(price, discount_percent)
    tax = calculate_tax(discounted_price)  # FIXED
    total = discounted_price + tax
    return total

# test
result = calculate_total(100, 20)
print(result)  # 98.4 - CORRECT!

# expected: 80 + (80 * 0.23) = 80 + 18.4 = 98.4 ✓
```

**if fix works, remove debug prints**

---

## common bugs and how to find them

### bug 1: wrong calculation (logic error)

**symptom:** code runs but gives wrong numbers

**example:**
```python
# bug
discount_amount = price * discount_percent
# 100 * 20 = 2000 (treating 20 as 2000%)

# fix
discount_decimal = discount_percent / 100
discount_amount = price * discount_decimal
# 100 * 0.20 = 20 (correct)
```

**how to find:** add print statements showing each calculation step

### bug 2: indentation error (python-specific)

**symptom:** loop doesn't run correctly, function exits early

**example from today:**
```python
# wrong indentation
def calculate_total(daily_sales):
    total = 0
    for sale in daily_sales:
        total = total + sale
        return total  # WRONG - returns after first item only!

# result: only processes first sale
```

**correct indentation:**
```python
def calculate_total(daily_sales):
    total = 0
    for sale in daily_sales:
        total = total + sale
    return total  # correct - returns after loop finishes
```

**how to find:** 
- add print statement inside loop
- if it only prints once, indentation is wrong
- return statement should be at same level as for statement

**visual guide:**
```python
def function():
    variable = 0
    for item in list:        # ← loop starts
        do_something()       # ← inside loop (indented)
        variable = variable + item  # ← inside loop (indented)
    return variable          # ← outside loop (same level as for)
```

### bug 3: using wrong variable

**symptom:** function uses original value instead of updated value

**example from today:**
```python
def calculate_total(price, discount_percent):
    discounted_price = calculate_discount(price, discount_percent)
    
    # bug: using original price for tax
    tax = calculate_tax(price)  # WRONG
    
    # fix: using discounted price for tax
    tax = calculate_tax(discounted_price)  # CORRECT
    
    total = discounted_price + tax
    return total
```

**how to find:** print both variables to see which one is being used

### bug 4: off-by-one error

**symptom:** loop runs too many or too few times

**example:**
```python
# wrong
for i in range(len(items) + 1):  # goes one past end
    process(items[i])  # crashes on last iteration

# correct
for i in range(len(items)):
    process(items[i])

# even better
for item in items:
    process(item)
```

---

## code templates

### template 1: basic debugging with prints

```python
def my_function(param1, param2):
    """function description."""
    # print inputs
    print(f"debug: param1 = {param1}")
    print(f"debug: param2 = {param2}")
    
    # calculate something
    result = param1 * param2
    print(f"debug: result = {result}")
    
    # do more calculations
    final = result / 100
    print(f"debug: final = {final}")
    
    return final
```

**when to use:** any time calculations aren't working as expected

---

### template 2: debugging loops

```python
def process_list(items):
    """process a list of items."""
    total = 0
    print(f"debug: processing {len(items)} items")
    
    for i, item in enumerate(items):
        print(f"debug: processing item {i+1}: {item}")
        total = total + item
        print(f"debug: total now = {total}")
    
    print(f"debug: loop finished, final total = {total}")
    return total
```

**what enumerate does:** gives you both the index and the item
```python
items = ["a", "b", "c"]
for i, item in enumerate(items):
    print(f"index {i}: {item}")

# output:
# index 0: a
# index 1: b
# index 2: c
```

**when to use:** when loop isn't processing all items or gives wrong results

---

### template 3: debugging multiple functions

```python
def function_a(x):
    """first function."""
    print(f"debug: function_a received x = {x}")
    result = x * 2
    print(f"debug: function_a returning {result}")
    return result

def function_b(y):
    """second function."""
    print(f"debug: function_b received y = {y}")
    result = y + 10
    print(f"debug: function_b returning {result}")
    return result

def main_function(value):
    """main function calling others."""
    print(f"debug: main_function starting with {value}")
    
    step1 = function_a(value)
    print(f"debug: step1 complete, result = {step1}")
    
    step2 = function_b(step1)
    print(f"debug: step2 complete, result = {step2}")
    
    return step2
```

**when to use:** when bug involves multiple functions calling each other

---

### template 4: clean version (after debugging)

```python
def calculate_discount(price, discount_percent):
    """
    calculate final price after discount.
    
    args:
        price: original price
        discount_percent: discount as percentage (20 for 20%)
    
    returns:
        final price after discount
    """
    discount_decimal = discount_percent / 100
    discount_amount = price * discount_decimal
    final_price = price - discount_amount
    return final_price
```

**important:** always remove debug prints from final code

---

## real business examples

### example 1: luigi's pizzeria email validation

**business problem:** customers sometimes type invalid emails, system crashes

**buggy code:**
```python
def validate_email(email):
    if "@" in email:
        return True
    return False

# problem: accepts "@@@@" as valid email
```

**debugging process:**
```python
def validate_email(email):
    print(f"debug: checking email: {email}")
    
    if "@" in email:
        print(f"debug: found @ symbol")
        parts = email.split("@")
        print(f"debug: parts after split: {parts}")
        
        if len(parts) == 2:
            print(f"debug: exactly 2 parts - good")
            return True
        else:
            print(f"debug: wrong number of parts")
            return False
    
    print(f"debug: no @ symbol found")
    return False

# test with bad email
validate_email("john@@gmail.com")
```

**debug output reveals:**
```
debug: checking email: john@@gmail.com
debug: found @ symbol
debug: parts after split: ['john', '', 'gmail.com']
debug: wrong number of parts  ← found the bug!
```

**fix:**
```python
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
```

**business value:**
- prevents system crashes from bad data
- improves user experience
- looks professional
- saves support time

---

### example 2: monthly revenue calculation bug

**business problem:** monthly report shows wrong total

**buggy code:**
```python
def calculate_monthly_revenue(daily_sales):
    total = 0
    for sale in daily_sales:
        total = total + sale
        return total  # BUG - returns after first sale only!

# test
sales = [500, 600, 550]
result = calculate_monthly_revenue(sales)
print(result)  # prints 500 instead of 1650
```

**debugging process:**
```python
def calculate_monthly_revenue(daily_sales):
    print(f"debug: processing {len(daily_sales)} sales")
    total = 0
    
    for sale in daily_sales:
        total = total + sale
        print(f"debug: added {sale}, total now = {total}")
        return total

# run and see output
```

**debug output:**
```
debug: processing 3 sales
debug: added 500, total now = 500
```

**only printed once! found the bug: return is inside the loop**

**fix:**
```python
def calculate_monthly_revenue(daily_sales):
    total = 0
    for sale in daily_sales:
        total = total + sale
    return total  # moved outside loop (same indentation as for)
```

**business value:**
- accurate financial reports
- correct revenue tracking
- trust from client
- avoid embarrassing mistakes

---

## key concepts

### concept 1: indentation matters in python

**python uses indentation to know what's inside what**

```python
# correct
def function():
    for item in list:
        do_something()  # inside loop
    return result       # outside loop

# wrong
def function():
    for item in list:
        do_something()  # inside loop
        return result   # inside loop - exits early!
```

**visual guide:**
```
def function():           ← function starts
    statement1           ← inside function
    statement2           ← inside function
    for item in list:    ← loop starts (inside function)
        statement3       ← inside loop (double indent)
        statement4       ← inside loop (double indent)
    statement5           ← outside loop but inside function
    return value         ← outside loop but inside function
```

### concept 2: debug then clean

**workflow:**
1. add debug prints
2. find the bug
3. fix the bug
4. test the fix
5. **remove debug prints**
6. test again without prints

**before (with debug):**
```python
def calculate_total(price, discount):
    print(f"debug: price = {price}")  # remove this
    print(f"debug: discount = {discount}")  # remove this
    
    result = price - (price * discount / 100)
    print(f"debug: result = {result}")  # remove this
    
    return result
```

**after (clean):**
```python
def calculate_total(price, discount):
    """calculate total after discount."""
    result = price - (price * discount / 100)
    return result
```

### concept 3: reproduce first, fix second

**always make sure you can reproduce the bug before trying to fix it**

```python
# can't reproduce = can't fix
# bug happens randomly? find pattern first

# can reproduce = can fix
# bug happens every time with same input? add debug prints and fix
```

---

## when to use what debugging method

### use print statements when:
- quick debugging needed
- simple calculations wrong
- need to see variable values
- learning/practicing
- function under 50 lines

### use python debugger (pdb) when:
- complex multi-function bug
- need to pause and inspect
- working with someone else's code
- production system debugging
- need to step through line by line

### use logging (day 19) when:
- production systems
- need permanent record
- debugging issues that happened in the past
- multiple users/clients
- need to track over time

**progression:**
- **learning (now):** print statements
- **small projects (days 30-84):** print statements + some logging
- **client work (days 85-168):** logging + occasional pdb
- **production systems:** primarily logging, pdb for complex bugs

---

## debugging mindset

### what professionals do:

**they don't:**
- randomly change code hoping it fixes
- give up after 5 minutes
- blame python/computer
- delete everything and start over

**they do:**
- follow systematic process (5 steps)
- add strategic debug statements
- test one fix at a time
- take breaks when stuck
- ask for help when needed

### debugging is a skill

**like any skill, you get better with practice:**

- **day 20 (now):** "i don't know where to start"
- **day 40:** "i can debug simple functions"
- **day 80:** "i can find bugs in multi-function systems"
- **day 168:** "i can debug production systems confidently"

**the more bugs you find and fix, the faster you get at it**

---

## common debugging mistakes

### mistake 1: not reproducing the bug first

**wrong approach:**
```python
# bug happens sometimes
# immediately start changing code
# don't know if fix works because can't reproduce bug
```

**right approach:**
```python
# bug happens sometimes
# find pattern: when does it fail?
# create test case that always fails
# now can debug systematically
```

### mistake 2: changing multiple things at once

**wrong approach:**
```python
# change line 5
# change line 10
# change line 15
# run code
# it works! but which change fixed it?
```

**right approach:**
```python
# change line 5
# run code
# still broken
# undo line 5
# change line 10
# run code
# it works! line 10 was the fix
```

### mistake 3: not removing debug prints

**wrong approach:**
```python
def calculate_discount(price, discount):
    print(f"debug: price = {price}")  # left in
    print(f"debug: discount = {discount}")  # left in
    result = price - (price * discount / 100)
    print(f"debug: result = {result}")  # left in
    return result

# client sees all these debug messages - looks unprofessional
```

**right approach:**
```python
def calculate_discount(price, discount):
    """calculate price after discount."""
    result = price - (price * discount / 100)
    return result

# clean code for client
```

### mistake 4: not testing the fix

**wrong approach:**
```python
# find bug
# fix bug
# assume it works
# deploy to client
# breaks in production
```

**right approach:**
```python
# find bug
# fix bug
# test with original failing case
# test with several other cases
# verify it works completely
# then deploy
```

---

## debugging checklist

**when your code doesn't work, check:**

- [ ] did i reproduce the bug consistently?
- [ ] which function has the bug?
- [ ] did i add debug prints to track values?
- [ ] did i check variable types (int vs string)?
- [ ] is my indentation correct?
- [ ] are variables named correctly (no typos)?
- [ ] did i test the fix?
- [ ] did i remove debug prints?

---

## business value and roi

### scenario: debugging client systems

**without debugging skills:**
```
client: "the discount calculation is wrong"
you: spend 3 hours randomly trying fixes
you: still can't find the problem
you: refund client
result: -3 hours, -money, -reputation
```

**with debugging skills:**
```
client: "the discount calculation is wrong"
you: add debug prints
you: find bug in 10 minutes (was missing / 100)
you: fix and test in 5 minutes
you: bill 1 hour (75 euro)
result: fixed in 15 min, charged 75 euro, happy client
```

### debugging is a billable skill

**freelance rates for debugging (ireland):**
- junior developer: 50-60 euro/hour
- mid developer: 60-80 euro/hour
- senior developer: 80-120 euro/hour

**most debugging tasks take 1-2 hours with proper skills**

**example:**
- client's system has bug
- you debug and fix in 1.5 hours
- charge 100 euro
- client happy (fast fix)
- you profitable (67 euro/hour effective rate)

---

## practical exercises

### exercise 1: find the bug

```python
def calculate_tip(bill, tip_percent):
    """calculate tip amount."""
    tip = bill * tip_percent
    return tip

# test
result = calculate_tip(100, 15)
print(f"tip: ${result}")
# expected: $15
# actual: $1500
```

**your task:**
1. add debug prints
2. find the bug
3. fix it
4. test it
5. remove debug prints

---

### exercise 2: indentation bug

```python
def sum_even_numbers(numbers):
    """sum all even numbers in list."""
    total = 0
    for num in numbers:
        if num % 2 == 0:
            total = total + num
            return total

# test
numbers = [1, 2, 3, 4, 5, 6]
result = sum_even_numbers(numbers)
print(result)
# expected: 12 (2 + 4 + 6)
# actual: 2 (only first even number)
```

**your task:** fix the indentation bug

---

### exercise 3: wrong variable used

```python
def apply_discount_and_tax(price, discount_percent):
    """apply discount then calculate tax."""
    discount_amount = price * (discount_percent / 100)
    discounted_price = price - discount_amount
    
    tax = price * 0.23  # bug is here
    
    final_price = discounted_price + tax
    return final_price

# test
result = apply_discount_and_tax(100, 20)
print(result)
# expected: 98.4 (80 after discount + 18.4 tax)
# actual: 103 (80 after discount + 23 tax on original price)
```

**your task:** find and fix the variable bug

---

## day 21 preview: week 3 integration

**tomorrow you'll:**
- combine all week 3 skills
- build a complete validation + logging + debugging system
- create professional error-handling code
- prepare for week 4 (api integration)

**what you'll build:**
```python
# complete system with:
- input validation (day 16-17)
- custom exceptions (day 18)
- logging (day 19)
- debugging-ready code (day 20)
```

---

## file organization

**your day 20 structure:**
```
ai-operations-training/
├── day-19/
│   ├── day19_logging.py
│   └── app.log
├── day-20/
│   ├── day20_debugging.py (all debugging examples)
│   └── day-20-notes.md (this file)
└── week-3-video/
    └── watch-after-day-21.txt
```

---

## achievements

- [x] used print statement debugging effectively
- [x] learned the 5-step debugging process
- [x] found and fixed calculation bugs
- [x] found and fixed indentation bugs
- [x] found and fixed variable bugs
- [x] cleaned up debug code professionally
- [x] understood when to use different debugging methods

**grade: a**

---

## key takeaways

1. **debugging is systematic** - follow the 5 steps every time
2. **print statements work great** - don't overcomplicate it
3. **indentation matters in python** - watch your spacing
4. **always test your fixes** - don't assume they work
5. **clean code is professional** - remove debug prints when done
6. **debugging is a billable skill** - clients pay for fast bug fixes

---

## the simple summary

### **debugging process:**
```python
# step 1: make bug happen every time
# step 2: find which function is broken
# step 3: add print statements to see values
# step 4: guess what's wrong
# step 5: fix it, test it, clean it up
```

### **most common bugs:**
```python
# wrong calculation
discount = price * percent  # should be: price * (percent / 100)

# wrong indentation
for item in list:
    process(item)
    return result  # should be outside loop

# wrong variable
tax = calculate_tax(price)  # should be: calculate_tax(discounted_price)
```

**debugging is how professionals fix problems fast**

---

## troubleshooting quick reference

| problem | likely cause | how to find | how to fix |
|---------|-------------|-------------|------------|
| wrong calculation | missing operation | add debug prints | add missing step |
| loop exits early | return inside loop | check indentation | move return outside |
| wrong value used | using wrong variable | print all variables | use correct variable |
| loop skips items | off-by-one error | print loop counter | fix range |
| function returns none | forgot return | check end of function | add return statement |

---

## week 3 progress

**completed:**
- day 15: error handling basics
- day 16: input validation
- day 17: data sanitization  
- day 18: custom exceptions
- day 19: logging
- day 20: debugging techniques

**remaining in week 3:**
- day 21: week 3 integration

**after day 21:** watch corey schafer error handling video

---

**created:** day 20 of ai operations training  
**your progress:** week 3, day 6 (day 20/168 total)  
**next session:** day 21 - week 3 integration

**you're building professional development skills.**  
**every day you're getting better at finding and fixing problems.**  
**this is what separates amateurs from professionals.**
