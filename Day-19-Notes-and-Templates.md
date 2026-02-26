# DAY 19: LOGGING - PROFESSIONAL ERROR TRACKING
## AI Operations Training - Week 3, Day 5

---

## what you learned today

### core skills:
- logging configuration and setup
- 5 log levels (debug, info, warning, error, critical)
- saving logs to permanent files
- real-world application to email systems
- production-ready logging patterns
- audit trail creation

### the architecture "why":
**days 15-18 taught you:** how to handle errors when they happen  
**day 19 teaches you:** how to track what's happening in your system

**the problem day 19 solves:**
- systems run 24/7 for clients
- things break at 3am when you're asleep
- client calls: "it stopped working!"
- without logs: spend 4 hours guessing what happened
- with logs: check file, see exact error, fix in 10 minutes

**real business impact:**
- permanent record of all system activity
- complete audit trail for compliance
- faster debugging (minutes vs hours)
- legal protection (prove what happened when)
- professional monitoring and alerting
- charge 50-100 euro/month extra for "professional monitoring"

---

## the key concept: permanent records

### what is logging?

**logging = creating permanent records of what your code does**

**print() statements (amateur):**
```python
print("processing email...")
print("email sent!")
# disappears when program ends
# can't review later
# no timestamps
# unprofessional
```

**logging (professional):**
```python
logging.info("processing email for customer@email.com")
logging.info("email sent successfully at 14:35:22")
# saved to file permanently
# includes timestamps
# can review days/weeks later
# filterable by importance
# industry standard
```

---

### real-world examples:

| scenario | without logging | with logging |
|----------|----------------|--------------|
| **system fails at 3am** | no idea what happened | check log: "error at 03:14:23 - database timeout" |
| **customer dispute** | "i think we sent it?" | "log shows email sent 2026-02-15 18:45:12" |
| **compliance audit** | search email archives (2 hours) | export app.log (2 minutes) |
| **debugging** | reproduce bug (4 hours) | read log file (10 minutes) |

**the principle:** if it's not logged, it didn't happen (legally)

---

## core concepts

### the 5 log levels

**python has 5 log levels from least to most severe:**

#### 1. debug - detailed information for diagnosing
```python
logging.debug("function called with parameters: a=10, b=5")
logging.debug("converted string to int: '123' -> 123")
```
**use for:** tracking code flow, variable values, detailed diagnostics  
**production:** usually turned off (too much detail)

#### 2. info - general information about execution
```python
logging.info("user logged in: john@email.com")
logging.info("email sent successfully")
logging.info("daily backup completed")
```
**use for:** tracking normal operations, audit trail  
**production:** always on

#### 3. warning - something unexpected but not broken
```python
logging.warning("disk space low: 15% remaining")
logging.warning("retry attempt 3 of 5")
logging.warning("deprecated feature used")
```
**use for:** potential problems, things to investigate  
**production:** always on, may trigger alerts

#### 4. error - serious problem, function failed
```python
logging.error("failed to send email: smtp timeout")
logging.error("database connection failed")
logging.error("invalid input: expected int, got str")
```
**use for:** failures that need attention  
**production:** always on, should trigger alerts

#### 5. critical - very serious, program may crash
```python
logging.critical("out of memory - shutting down")
logging.critical("security breach detected")
logging.critical("database corrupted")
```
**use for:** system-level failures  
**production:** always on, immediate alerts to phone

---

### visual comparison:

```python
# all log levels in action
logging.debug("function started")           # detailed tracking
logging.info("processing 100 records")      # what's happening
logging.warning("10 records skipped")       # potential issue
logging.error("5 records failed")           # definite problem
logging.critical("system shutting down")    # emergency
```

**key insight:** choose the right level for the right situation

---

## code templates

### template 1: basic logging setup

```python
import logging

# configure logging (do this once at top of file)
logging.basicConfig(
    level=logging.DEBUG,  # show all levels
    format='%(levelname)s: %(message)s'
)

# use logging throughout your code
logging.debug("this is debug info")
logging.info("this is general info")
logging.warning("this is a warning")
logging.error("this is an error")
logging.critical("this is critical")
```

**what this does:**
- `level=logging.DEBUG` → show all messages (debug and above)
- `format=` → how messages appear
- simple, console-only logging

**when to use:** quick testing, learning, simple scripts

---

### template 2: logging to files (professional)

```python
import logging

# configure logging to save to file
logging.basicConfig(
    level=logging.INFO,  # info and above
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),  # save to file
        logging.StreamHandler()           # also print to console
    ]
)

def process_data(data):
    """process data with logging."""
    logging.info(f"processing {len(data)} items")
    
    try:
        result = do_something(data)
        logging.info("processing successful")
        return result
    except Exception as e:
        logging.error(f"processing failed: {e}")
        return None
```

**what's new:**
- `%(asctime)s` → adds timestamp to each log
- `FileHandler('app.log')` → saves to file
- `StreamHandler()` → still prints to console

**when to use:** production systems, client projects, anything that runs unattended

---

### template 3: logging in real functions

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s - %(message)s'
)

def divide_numbers(a, b):
    """
    divides two numbers with comprehensive logging.
    
    real-world use: any calculation in client systems
    task: track all operations for debugging
    value: know exactly what happened when
    """
    # track function call
    logging.debug(f"divide_numbers called with a={a}, b={b}")
    
    # validate inputs
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        logging.error(f"invalid input types: a={type(a)}, b={type(b)}")
        return None
    
    # check for division by zero
    if b == 0:
        logging.warning("attempted division by zero!")
        return None
    
    # perform division
    result = a / b
    logging.info(f"successfully divided {a} by {b} = {result}")
    return result

# usage examples:
divide_numbers(10, 2)   # info: success
divide_numbers(10, 0)   # warning: division by zero
divide_numbers("10", 2) # error: wrong type
```

**what this demonstrates:**
- debug → track function calls
- info → track successful operations
- warning → track problems that don't break function
- error → track failures

**when to use:** any function that processes data or performs operations

---

### template 4: email system with logging (luigi's pizzeria)

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('luigis_email_system.log'),
        logging.StreamHandler()
    ]
)

def process_customer_email(customer_tier, email_type, tokens_used):
    """
    email automation with professional logging.
    
    real-world use: luigi's pizzeria email system
    task: track all email processing for audit trail
    value: legal compliance + debugging + dispute resolution
    """
    logging.info(f"starting email processing: tier={customer_tier}, type={email_type}")
    
    # validate customer tier
    valid_tiers = ["vip", "standard"]
    if customer_tier not in valid_tiers:
        logging.error(f"invalid customer tier: '{customer_tier}' (expected {valid_tiers})")
        return None
    
    # validate email type
    if not isinstance(email_type, str):
        logging.error(f"email type must be string, got {type(email_type)}")
        return None
    
    # process tokens
    if isinstance(tokens_used, str):
        if not tokens_used.isdigit():
            logging.error(f"invalid token count: '{tokens_used}' (must be numeric)")
            return None
        tokens_used = int(tokens_used)
        logging.debug(f"converted string tokens to int: {tokens_used}")
    
    # calculate cost
    cost = (tokens_used / 1000) * 0.003
    logging.info(f"email processed successfully: {customer_tier} {email_type}, cost=${cost:.4f}")
    
    return {
        "tier": customer_tier,
        "type": email_type,
        "tokens": tokens_used,
        "cost": cost
    }

# usage examples:
process_customer_email("vip", "complaint", 250)      # success
process_customer_email("viip", "complaint", 250)     # error: typo in tier
process_customer_email("standard", "reservation", "180")  # success: converts string
```

**log file will contain:**
```
2026-02-17 21:36:13 - INFO - starting email processing: tier=vip, type=complaint
2026-02-17 21:36:13 - INFO - email processed successfully: vip complaint, cost=$0.0008
2026-02-17 21:36:13 - INFO - starting email processing: tier=viip, type=complaint
2026-02-17 21:36:13 - ERROR - invalid customer tier: 'viip' (expected ['vip', 'standard'])
2026-02-17 21:36:13 - INFO - starting email processing: tier=standard, type=reservation
2026-02-17 21:36:13 - DEBUG - converted string tokens to int: 180
2026-02-17 21:36:13 - INFO - email processed successfully: standard reservation, cost=$0.0005
```

**business value:**
- audit trail for compliance
- customer dispute resolution
- debugging failed emails
- performance tracking
- legal protection

---

### template 5: production logging (clean logs)

```python
import logging

logging.basicConfig(
    level=logging.INFO,  # skip debug in production
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('production.log'),
        logging.StreamHandler()
    ]
)

def production_email_system(customer_tier, email_type, tokens_used):
    """
    production version - only logs important events.
    
    real-world use: luigi's live system (not testing)
    task: track successes and errors, skip debug details
    value: clean logs for production monitoring
    """
    logging.info(f"email request: {customer_tier} - {email_type}")
    
    try:
        # validate
        if customer_tier not in ["vip", "standard"]:
            raise ValueError(f"invalid tier: {customer_tier}")
        
        if isinstance(tokens_used, str):
            tokens_used = int(tokens_used)
        
        # process
        cost = (tokens_used / 1000) * 0.003
        
        # success - log for audit trail
        logging.info(f"success: email sent: {email_type}, cost=${cost:.4f}")
        return cost
        
    except ValueError as e:
        # business logic error - log as error
        logging.error(f"failed: validation error: {e}")
        return None
    except Exception as e:
        # unexpected error - log as critical
        logging.critical(f"critical: system error: {e}")
        return None

# usage:
production_email_system("vip", "complaint", 250)       # success
production_email_system("invalid", "test", 100)        # error
production_email_system("standard", "reservation", "180")  # success
```

**production log output:**
```
2026-02-17 21:40:07 - INFO - email request: vip - complaint
2026-02-17 21:40:07 - INFO - success: email sent: complaint, cost=$0.0008
2026-02-17 21:40:07 - INFO - email request: invalid - test
2026-02-17 21:40:07 - ERROR - failed: validation error: invalid tier: invalid
2026-02-17 21:40:07 - INFO - email request: standard - reservation
2026-02-17 21:40:07 - INFO - success: email sent: reservation, cost=$0.0005
```

**why clean logs matter:**
- easier to read in production
- faster to find problems
- less disk space
- better performance
- professional appearance

---

### template 6: daily operations summary

```python
def track_daily_operations():
    """
    demonstrates all log levels in one function.
    
    real-world use: end-of-day summary for luigi
    task: review what happened during business hours
    value: audit trail and performance tracking
    """
    logging.debug("starting daily operations review")
    
    # simulate processing emails
    emails_sent = 45
    emails_failed = 3
    total_revenue = 125.50
    
    logging.info(f"daily summary: {emails_sent} emails sent")
    
    if emails_failed > 0:
        logging.warning(f"{emails_failed} emails failed - review needed")
    
    if total_revenue < 100:
        logging.error("revenue below target - check pricing")
    else:
        logging.info(f"revenue target met: ${total_revenue}")
    
    logging.debug("daily operations review complete")
```

**log output:**
```
2026-02-17 21:43:00 - DEBUG - starting daily operations review
2026-02-17 21:43:00 - INFO - daily summary: 45 emails sent
2026-02-17 21:43:00 - WARNING - 3 emails failed - review needed
2026-02-17 21:43:00 - INFO - revenue target met: $125.5
2026-02-17 21:43:00 - DEBUG - daily operations review complete
```

**use case:** automated daily reports, performance monitoring, alerting

---

## key concepts

### when to use each log level

**use debug when:**
- tracking code flow for development
- inspecting variable values
- understanding complex logic
- diagnosing tricky bugs
- development and testing only

**use info when:**
- tracking normal operations
- audit trail of successful actions
- user activity logging
- business intelligence
- production monitoring

**use warning when:**
- recoverable errors
- deprecated features used
- resource limits approaching
- retry attempts
- things to investigate

**use error when:**
- operation failed
- data validation errors
- connection failures
- processing errors
- needs attention

**use critical when:**
- system-level failures
- security breaches
- data corruption
- service outage
- immediate action required

---

### logging configuration patterns

**development configuration:**
```python
logging.basicConfig(
    level=logging.DEBUG,  # show everything
    format='%(levelname)s - %(message)s'
)
```
- see all details
- simple format
- console only
- for testing

**production configuration:**
```python
logging.basicConfig(
    level=logging.INFO,  # skip debug
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```
- skip debug noise
- include timestamps
- save to file
- also show on console

**high-volume production:**
```python
logging.basicConfig(
    level=logging.WARNING,  # only warnings and above
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log')
    ]
)
```
- minimal logging
- file only (no console)
- reduce disk usage
- for stable systems

---

## common errors and fixes

### error 1: logs not appearing
**symptom:** logging calls don't show anything
```python
import logging
logging.info("this doesn't appear")  # nothing shows
```

**cause:** default level is warning, so info/debug don't show

**fix:** configure basicConfig with level
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logging.info("now it appears!")
```

---

### error 2: unicode encoding errors (windows)
**symptom:** unicode characters crash on windows
```python
logging.info("success")  # fails on windows
```

**cause:** windows console can't handle unicode

**fix:** use simple ascii text
```python
logging.info("success: email sent")  # works everywhere
```

---

### error 3: logs not saving to file
**symptom:** file created but empty
```python
logging.basicConfig(filename='app.log')
logging.info("message")
# file exists but empty
```

**cause:** forgot handlers or wrong configuration

**fix:** use filehandler properly
```python
logging.basicConfig(
    handlers=[logging.FileHandler('app.log')]
)
logging.info("message")  # now saves
```

---

### error 4: duplicate log messages
**symptom:** each message appears twice
```python
logging.basicConfig(...)
logging.basicConfig(...)  # called twice
logging.info("test")  # appears twice
```

**cause:** basicConfig called multiple times

**fix:** only call once at top of file
```python
import logging
logging.basicConfig(...)  # once only
```

---

## business value and roi

### scenario: luigi's pizzeria email automation

**client:** italian restaurant in dublin  
**system:** ai email automation (your day 14 project)  
**monthly fee:** 1200 euro

**without logging:**
```
3:00 am - system fails silently
9:00 am - customer calls angry: "no confirmation!"
9:05 am - luigi calls you: "system broken!"
9:10 am - you spend 2 hours debugging
11:00 am - still guessing what happened
result: 2 hours × 75 euro/hour = 150 euro lost
        + angry customer
        + bad review
        + lost trust
```

**with logging:**
```
3:00 am - system fails
3:01 am - error logged: "invalid email: customergmail.com"
9:00 am - customer calls
9:01 am - you check log file
9:02 am - "customer typed customergmail.com instead of customer@gmail.com"
9:03 am - problem solved
result: 2 minutes to resolve
        + professional service
        + client impressed
        + trust increased
```

**roi calculation:**
- logging implementation: 1 hour (75 euro)
- monthly value saved: 150 euro/incident × 3 incidents = 450 euro
- additional charge: 50 euro/month "professional monitoring"
- net gain: 450 saved + 50 charged = 500 euro/month

**return:** 567% monthly roi

---

### scenario: legal compliance - health department audit

**client:** restaurant with email order confirmations  
**audit requirement:** prove order confirmations were sent

**without logging:**
```
auditor: "prove you sent these confirmations"
luigi: "i think we sent them?"
auditor: searches email server logs (30 minutes)
auditor: some emails found, some missing
auditor: "insufficient documentation"
result: 500 euro fine
```

**with logging:**
```
auditor: "prove you sent these confirmations"
luigi: "here's our complete log file"
log shows:
  2026-02-15 18:45:12 - info - order confirmation sent to customer@email.com
  2026-02-15 18:50:33 - info - order confirmation sent to another@email.com
  ...complete record of all emails...
auditor: "perfect documentation"
result: audit passes in 5 minutes
        no fine
        professional appearance
```

**value:**
- avoided fine: 500 euro
- saved time: 2 hours (150 euro)
- total value: 650 euro
- cost: 0 euro (already implemented)

---

### scenario: customer dispute resolution

**client:** catering business  
**dispute:** customer claims quote never received

**without logging:**
```
customer: "you never sent my quote!"
luigi: "i'm sure we did..."
customer: "prove it"
luigi: searches email archives (20 minutes)
luigi: can't find definitive proof
result: give customer discount to keep happy (100 euro lost)
```

**with logging:**
```
customer: "you never sent my quote!"
luigi: checks log file (30 seconds)
luigi: "our system shows quote sent feb 15 at 18:45:12"
luigi: "you clicked the quote link at 19:15:33"
luigi: "you confirmed booking at 19:22:45"
customer: "oh... let me check my spam folder"
customer: "found it! sorry!"
result: dispute resolved in 2 minutes
        no discount needed
        customer embarrassed, luigi vindicated
```

**value:**
- saved discount: 100 euro
- saved time: 20 minutes (25 euro)
- preserved reputation
- total value: 125 euro per incident

---

## real-world logging patterns

### pattern 1: request/response logging

```python
def handle_customer_request(customer_id, request_type):
    """track complete request lifecycle."""
    logging.info(f"request received: customer={customer_id}, type={request_type}")
    
    try:
        result = process_request(request_type)
        logging.info(f"request completed: customer={customer_id}, result={result}")
        return result
    except Exception as e:
        logging.error(f"request failed: customer={customer_id}, error={e}")
        return None
```

**log output:**
```
2026-02-17 10:15:22 - INFO - request received: customer=12345, type=quote
2026-02-17 10:15:23 - INFO - request completed: customer=12345, result=quote_sent
```

**use case:** track every customer interaction

---

### pattern 2: performance logging

```python
import time

def process_large_batch(items):
    """track processing performance."""
    start_time = time.time()
    logging.info(f"starting batch: {len(items)} items")
    
    processed = 0
    for item in items:
        process_item(item)
        processed += 1
    
    duration = time.time() - start_time
    logging.info(f"batch complete: {processed} items in {duration:.2f}s")
    
    if duration > 60:
        logging.warning(f"batch processing slow: {duration:.2f}s")
```

**use case:** monitor system performance, identify slowdowns

---

### pattern 3: error context logging

```python
def send_email(to_address, subject, body):
    """log with context for debugging."""
    logging.debug(f"attempting email: to={to_address}, subject={subject[:30]}")
    
    try:
        email_client.send(to_address, subject, body)
        logging.info(f"email sent: {to_address}")
    except SMTPError as e:
        logging.error(f"smtp failed: {to_address}, error: {e}")
    except NetworkError as e:
        logging.error(f"network failed: {to_address}, error: {e}")
    except Exception as e:
        logging.critical(f"unexpected error: {to_address}, error: {e}")
```

**use case:** understand exactly what went wrong and where

---

## practical exercises

### exercise 1: add logging to day 14 system
```python
"""
take your day 14 email automation system
add comprehensive logging:
- info level for successful emails
- warning for validation issues
- error for failures
- debug for detailed tracking
"""
# your code here
```

---

### exercise 2: create audit logger
```python
"""
create a function that logs all user actions:
- login/logout
- data changes
- file uploads
- permission changes
suitable for compliance requirements
"""
# your code here
```

---

### exercise 3: performance monitor
```python
"""
create a decorator that logs:
- function name
- execution time
- parameters
- return value
use for identifying slow functions
"""
# your code here
```

---

## day 20 preview: debugging techniques

**tomorrow you'll learn:**
- using vs code debugger
- setting breakpoints
- step-through debugging
- inspecting variables
- call stack navigation
- professional troubleshooting

**example:**
```python
# instead of adding print statements everywhere
def complex_function(data):
    print(f"data: {data}")  # amateur
    result = process(data)
    print(f"result: {result}")  # amateur
    return result

# use debugger:
# - set breakpoint on line 3
# - step through code
# - inspect all variables
# - see exactly what's happening
# - professional debugging
```

**why it matters:**
- find bugs 10x faster
- understand complex code flow
- debug production issues
- professional development workflow
- no more "print debugging"

---

## file organization

**your day 19 structure:**
```
ai-operations-training/
├── day-15/
│   ├── day15_error_handling.py
│   └── day-15-notes.md
├── day-16/
│   ├── day16_input_validation.py
│   └── day-16-notes.md
├── day-17/
│   ├── day17_advanced_validation.py
│   └── day-17-notes.md
├── day-18/
│   ├── day18_custom_exceptions.py
│   └── day-18-notes.md
├── day-19/
│   ├── day19_logging.py (all logging examples)
│   ├── app.log (your log file!)
│   └── day-19-notes.md (this file)
└── week-3-video/
    └── watch-after-day-21.txt
```

---

## achievements

- [x] configured logging system
- [x] used all 5 log levels correctly
- [x] saved logs to permanent files
- [x] applied logging to email system
- [x] built production-ready patterns
- [x] understood business value

**grade: a+**

---

## key takeaways

1. **logging creates permanent records** - survives program restarts
2. **use appropriate log levels** - debug for detail, critical for emergencies
3. **always log to files in production** - console logs disappear
4. **include timestamps** - know when things happened
5. **log business-critical events** - audit trail for compliance
6. **descriptive messages** - include context and details
7. **professional debugging** - logs save hours of work

---

## the simple summary

### **without logging:**
```python
# something breaks
# no idea what happened
# spend hours debugging
# can't prove what you did
# unprofessional
```

### **with logging:**
```python
# something breaks
# check log file
# see exactly what happened and when
# fix in minutes
# complete audit trail
# professional service
```

**logging is the difference between amateur and professional code.**

---

## troubleshooting quick reference

| problem | cause | fix |
|---------|-------|-----|
| logs not appearing | level too high | set level=logging.debug |
| no timestamps | format missing asctime | add %(asctime)s to format |
| not saving to file | missing filehandler | add logging.filehandler('app.log') |
| unicode errors (windows) | fancy characters | use simple ascii text |
| duplicate messages | basicconfig called twice | configure only once at top |

---

## when to use what

**use debug:**
- development and testing
- detailed code flow tracking
- variable inspection
- turn off in production

**use info:**
- normal operations
- audit trail
- business intelligence
- always on in production

**use warning:**
- potential problems
- resource limits
- recoverable errors
- investigate later

**use error:**
- operation failures
- needs attention
- something is broken
- alert on-call person

**use critical:**
- system failures
- security issues
- immediate action
- wake up everyone

---

## week 3 progress

**completed:**
- day 15 (error handling)
- day 16 (input validation)
- day 17 (data sanitization)
- day 18 (custom exceptions)
- day 19 (logging)

**remaining in week 3:**
- day 20: debugging techniques
- day 21: week 3 integration

**after day 21:** watch corey schafer error handling video

---

**created:** day 19 of ai operations training  
**your progress:** week 3, day 5 (day 19/168 total)  
**next session:** day 20 - debugging techniques

**you're building production-ready, professional systems now.** 
**every day 14 system you sell will have logging = extra 50 euro/month.**
