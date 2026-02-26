# DAY 23: API AUTHENTICATION & POST REQUESTS
## AI Operations Training - Week 4, Day 2

---

## what you learned today

### core skills:
- authenticate with apis using api keys
- make post requests to send/create data
- combine authentication + post requests
- build complete validation → api workflows
- structure request bodies correctly

### the architecture "why":
**day 22 taught you:** reading data from apis (get requests)  
**day 23 teaches you:** writing data to apis (post requests) + authentication

**the problem day 23 solves:**
```python
# day 22 (read only)
response = requests.get(url)
# you can see data but can't do anything

# day 23 (read + write)
response = requests.post(url, headers=auth, json=data)
# you can create, send, automate actions
# this is what clients actually pay for
```

**real business impact:**
- day 22: read weather, read user data (informational)
- day 23: send emails, charge cards, create reservations (actionable)
- clients don't pay to read data, they pay to automate actions

---

## the key concept: authentication

### why apis need authentication

**public apis (no auth):**
- free weather data
- public github repos
- anyone can access
- no billing, no rate limits per user

**private apis (require auth):**
- sendgrid (email)
- stripe (payments)
- claude (ai)
- need to identify you for billing and rate limits

### how authentication works

**the basic flow:**
```
1. you sign up for service (sendgrid, stripe, etc)
2. service gives you api key: "sk_abc123..."
3. you include key in every request
4. service knows it's you
5. service bills you, tracks usage, applies rate limits
```

---

## core concept 1: authentication methods

### method 1: api key in headers (90% of apis)

**most common and secure method**

```python
headers = {
    "Authorization": "Bearer sk_test_fake_key_12345",
    # or
    "X-API-Key": "my-secret-key"
}

response = requests.get(url, headers=headers)
```

**your output today:**
```json
{
  "Authorization": "bearer sk_test_fake_key_12345",
  "X-Api-Key": "my-secret-key"
}
```

**why headers are better:**
- api key not visible in url
- not logged in browser history
- can't be accidentally shared
- professional standard

**real examples:**
```python
# sendgrid
headers = {"Authorization": "Bearer SG.xxxxxxxxxxxxx"}

# stripe
headers = {"Authorization": "Bearer sk_live_xxxxxxxxxxxxx"}

# claude api
headers = {"x-api-key": "sk-ant-xxxxxxxxxxxxx"}
```

---

### method 2: api key in query parameter (10% of apis)

**less common, less secure**

```python
params = {
    "api_key": "my-secret-key",
    "user_id": "luigi123"
}

response = requests.get(url, params=params)
```

**your output today:**
```
url called: https://httpbin.org/get?api_key=my-secret-key&user_id=luigi123
```

**why this is less secure:**
- api key visible in url
- shows in browser history
- logged in server access logs
- can be accidentally shared when copying url

**when it's used:**
- some weather apis
- public data apis
- quick testing/demos

---

## core concept 2: get vs post requests

### understanding the difference

**get requests (day 22):**
- retrieve/read data
- don't change anything on server
- like viewing a book

**post requests (day 23):**
- send/create data
- change things on server
- like writing in a book

### http methods comparison

| method | purpose | changes data? | has body? |
|--------|---------|---------------|-----------|
| get | retrieve data | no | no |
| post | create data | yes | yes |
| put | update data | yes | yes |
| delete | remove data | yes | no |

**today you learned get and post. put/delete come on day 24.**

---

## core concept 3: post request structure

### anatomy of a post request

```python
response = requests.post(
    url="https://api.example.com/endpoint",  # where to send
    headers={"Authorization": "Bearer key"},  # who you are
    json={"name": "value"},                   # data to send
    timeout=10                                 # max wait time
)
```

**four key parts:**
1. **url** - where to send the request
2. **headers** - authentication and metadata
3. **json** - the actual data being sent
4. **timeout** - how long to wait

---

## the complete code examples

### example 1: understanding authentication

```python
import requests
import json

# method 1: api key in header (most common)
url = "https://httpbin.org/headers"

headers = {
    "Authorization": "Bearer sk_test_fake_key_12345",
    "X-API-Key": "my-secret-key"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print("headers sent:")
    print(json.dumps(data["headers"], indent=2))
```

**what happened:**
- sent api key in headers
- server received and echoed back
- this proves authentication worked

**your output:**
```json
{
  "Authorization": "bearer sk_test_fake_key_12345",
  "X-Api-Key": "my-secret-key"
}
```

---

### example 2: basic post request

```python
# data to send (like creating a new reservation)
reservation_data = {
    "customer_name": "john smith",
    "email": "john@email.com",
    "date": "2026-03-15",
    "party_size": 4,
    "special_requests": "window seat please"
}

# make post request with json data
url = "https://httpbin.org/post"
response = requests.post(url, json=reservation_data)

if response.status_code == 200:
    result = response.json()
    print(f"server received: {result['json']}")
    print(f"content-type: {result['headers']['Content-Type']}")
```

**what the json= parameter does:**
1. converts python dict to json string automatically
2. sets `Content-Type: application/json` header
3. sends data in request body

**your output:**
```
server received: {
  'customer_name': 'john smith',
  'date': '2026-03-15',
  'email': 'john@email.com',
  'party_size': 4,
  'special_requests': 'window seat please'
}
content-type: application/json
```

---

### example 3: authenticated post request

```python
def send_email_simulation(to_email, subject, body):
    """
    simulate sending email via sendgrid api.
    demonstrates auth + post together.
    """
    url = "https://httpbin.org/post"
    
    # authentication
    headers = {
        "Authorization": "Bearer SG.fake_sendgrid_key_12345",
        "Content-Type": "application/json"
    }
    
    # data to send
    email_data = {
        "personalizations": [
            {
                "to": [{"email": to_email}],
                "subject": subject
            }
        ],
        "from": {"email": "noreply@luigispizzeria.com"},
        "content": [
            {
                "type": "text/plain",
                "value": body
            }
        ]
    }
    
    try:
        # post with auth + data
        response = requests.post(
            url,
            headers=headers,
            json=email_data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("email sent successfully!")
            print(f"response time: {response.elapsed.total_seconds():.2f} seconds")
            return True
        else:
            print(f"failed: status {response.status_code}")
            return False
    
    except requests.exceptions.Timeout:
        print("timeout - will retry later")
        return False
    
    except Exception as e:
        print(f"error: {e}")
        return False


# send confirmation email
send_email_simulation(
    to_email="customer@email.com",
    subject="Reservation Confirmed - Luigi's Pizzeria",
    body="Your table for 4 on 2026-03-15 at 7:00 PM is confirmed."
)
```

**what this demonstrates:**
- authentication via header
- data sent via json body
- error handling (timeout, exceptions)
- professional structure

**your output:**
```
sending email to: customer@email.com
subject: Reservation Confirmed - Luigi's Pizzeria
authentication with api key...

email sent successfully!
response time: 1.15seconds

server confirmed receipt
```

---

### example 4: complete workflow integration

```python
def process_reservation_and_send_confirmation(customer_data):
    """
    complete workflow combining week 3 + week 4 skills:
    1. validate data (week 3)
    2. send via api (week 4)
    """
    # step 1: validation (week 3 skills)
    print("step 1: validating reservation data...")
    
    required_fields = ["name", "email", "date", "party_size"]
    for field in required_fields:
        if field not in customer_data or not customer_data[field]:
            print(f"validation failed: missing {field}")
            return False
    
    print("validation passed")
    
    # step 2: prepare email content
    print("step 2: preparing confirmation email...")
    subject = f"Reservation Confirmed - {customer_data['name']}"
    body = f"""
Dear {customer_data['name']},

Your reservation is confirmed!

Details:
- Date: {customer_data['date']}
- Party Size: {customer_data['party_size']} people
- Time: 7:00 PM

We look forward to serving you at Luigi's Pizzeria.

Thank you,
Luigi's Team
    """
    
    print("email content prepared")
    
    # step 3: send via api (week 4 skills)
    print("step 3: sending confirmation email...")
    success = send_email_simulation(
        to_email=customer_data['email'],
        subject=subject,
        body=body
    )
    
    if success:
        print("workflow complete: reservation processed and confirmed")
        return True
    else:
        print("workflow failed: email not sent")
        return False


# test complete workflow
reservation = {
    "name": "john smith",
    "email": "john@email.com",
    "date": "2026-03-15",
    "party_size": 4
}

result = process_reservation_and_send_confirmation(reservation)
print(f"final result: {'success' if result else 'failed'}")
```

**what this demonstrates:**
- week 3 skills (validation, error handling)
- week 4 skills (api integration)
- complete business workflow
- this is what you'll build for clients

**your output:**
```
step 1: validating reservation data...
validation passed

step 2: preparing confirmation email...
email content prepared

step 3: sending confirmation email...

sending email to: john@email.com
subject: Reservation Confirmed - john smith
authentication with api key...

email sent successfully!
response time: 0.82seconds

server confirmed receipt

workflow complete: reservation processed and confirmed

final result: success
```

---

## understanding request headers

### what headers are

**headers = metadata about the request**

**common headers you'll use:**
- `Authorization` - api key or token
- `Content-Type` - format of data you're sending
- `Accept` - format you want back
- `User-Agent` - identifies your application

### content-type header

**when sending json:**
```python
headers = {
    "Content-Type": "application/json"
}
```

**the json= parameter sets this automatically:**
```python
# these are equivalent:
response = requests.post(url, json=data)

# same as:
response = requests.post(
    url,
    headers={"Content-Type": "application/json"},
    data=json.dumps(data)
)
```

**use json= parameter - it's simpler and safer**

---

## understanding request body

### what goes in the body

**get requests:** no body (data in url parameters)  
**post requests:** body contains the data

### body formats

**json (most common):**
```python
data = {"name": "john", "age": 30}
response = requests.post(url, json=data)
```

**form data (less common):**
```python
data = {"name": "john", "age": "30"}
response = requests.post(url, data=data)
```

**for apis, always use json**

---

## real api patterns

### pattern 1: sendgrid (email)

```python
url = "https://api.sendgrid.com/v3/mail/send"

headers = {
    "Authorization": "Bearer SG.your_actual_key_here",
    "Content-Type": "application/json"
}

email_data = {
    "personalizations": [
        {"to": [{"email": "customer@email.com"}]}
    ],
    "from": {"email": "you@yourcompany.com"},
    "subject": "test email",
    "content": [
        {"type": "text/plain", "value": "hello world"}
    ]
}

response = requests.post(url, headers=headers, json=email_data)
```

**this is the real sendgrid api structure**

---

### pattern 2: stripe (payments)

```python
url = "https://api.stripe.com/v1/charges"

headers = {
    "Authorization": "Bearer sk_live_your_key_here"
}

charge_data = {
    "amount": 2000,  # €20.00 in cents
    "currency": "eur",
    "source": "tok_visa",  # token from stripe.js
    "description": "pizza order"
}

response = requests.post(url, headers=headers, data=charge_data)
```

**note: stripe uses data= not json=**

---

### pattern 3: claude api (ai)

```python
url = "https://api.anthropic.com/v1/messages"

headers = {
    "x-api-key": "sk-ant-your_key_here",
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
}

message_data = {
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 1024,
    "messages": [
        {"role": "user", "content": "hello claude"}
    ]
}

response = requests.post(url, headers=headers, json=message_data)
```

**this is what you'll use in week 5**

---

## error handling for apis

### common errors and how to handle them

**timeout errors:**
```python
try:
    response = requests.post(url, json=data, timeout=10)
except requests.exceptions.Timeout:
    print("request timed out after 10 seconds")
    # retry logic here
```

**connection errors:**
```python
try:
    response = requests.post(url, json=data)
except requests.exceptions.ConnectionError:
    print("could not connect to api")
    # check internet, verify url
```

**http errors (400, 401, 500, etc):**
```python
response = requests.post(url, json=data)

if response.status_code == 200:
    # success
    data = response.json()
elif response.status_code == 401:
    # authentication failed
    print("invalid api key")
elif response.status_code == 400:
    # bad request
    print("invalid data format")
else:
    print(f"error: status {response.status_code}")
```

---

## professional error handling pattern

```python
def make_api_request(url, headers, data):
    """
    professional api request with full error handling.
    """
    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        elif response.status_code == 401:
            return {"success": False, "error": "authentication failed"}
        elif response.status_code == 400:
            return {"success": False, "error": "invalid data"}
        elif response.status_code == 429:
            return {"success": False, "error": "rate limit exceeded"}
        else:
            return {"success": False, "error": f"status {response.status_code}"}
    
    except requests.exceptions.Timeout:
        return {"success": False, "error": "request timeout"}
    
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "connection failed"}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


# use it
result = make_api_request(url, headers, data)

if result["success"]:
    print(f"success: {result['data']}")
else:
    print(f"failed: {result['error']}")
```

---

## key concepts

### concept 1: authentication identifies you

**why apis need to know who you are:**
- billing (charge you for usage)
- rate limiting (prevent abuse)
- access control (what you can access)
- usage tracking (how much you use)

**without authentication:**
- anyone could use service free
- no way to bill users
- can't prevent abuse
- no usage limits

---

### concept 2: post creates, get reads

**when to use get:**
- retrieving user data
- fetching weather
- reading reservations
- searching repositories
- getting current state

**when to use post:**
- creating new user
- sending email
- making reservation
- processing payment
- generating ai content

---

### concept 3: headers carry authentication

**api keys go in headers because:**
- not visible in url
- not logged by default
- can't be accidentally shared
- industry standard
- more secure

**never put api keys in:**
- url parameters (visible)
- code comments (visible on github)
- console.log statements (visible in logs)
- client-side code (visible to users)

---

### concept 4: json is the data format

**why apis use json:**
- easy for humans to read
- easy for computers to parse
- supported by all languages
- nested data structures
- industry standard

**json structure:**
```json
{
  "string": "text value",
  "number": 123,
  "boolean": true,
  "null": null,
  "array": [1, 2, 3],
  "object": {
    "nested": "value"
  }
}
```

---

## real business application

### luigi's reservation confirmation system

**manual process (before):**
1. customer makes reservation online
2. luigi gets notification
3. luigi manually writes email
4. luigi manually sends email
5. time: 5 minutes per reservation

**automated process (after - what you built today):**
1. customer makes reservation online
2. system validates data
3. system sends confirmation automatically
4. customer gets email instantly
5. time: 0.5 seconds, zero manual work

**time saved:**
- 5 minutes × 50 reservations/week = 250 minutes/week
- 250 minutes = 4+ hours/week
- at €30/hour labor = €120/week = €480/month saved

**what you don't know:**
- what you could charge to build this
- what clients would actually pay
- monthly retainer vs one-time fee
- success rate of getting clients

**what we do know from fiverr search (feb 2026):**
- simple api integration: €100-300 (one-time)
- complex integration: €300-800+ (one-time)
- automation workflows: starting at €15-20

---

## troubleshooting guide

### problem: 401 unauthorized
**cause:** invalid or missing api key  
**fix:** verify api key, check header format

```python
# wrong
headers = {"Authorization": "sk_abc123"}

# correct
headers = {"Authorization": "Bearer sk_abc123"}
```

---

### problem: 400 bad request
**cause:** invalid data format  
**fix:** check json structure, verify required fields

```python
# check what you're sending
print(json.dumps(data, indent=2))

# verify it matches api docs
```

---

### problem: 429 too many requests
**cause:** exceeded rate limit  
**fix:** slow down requests, implement retry logic

```python
import time

response = requests.post(url, json=data)

if response.status_code == 429:
    print("rate limited, waiting 60 seconds...")
    time.sleep(60)
    response = requests.post(url, json=data)
```

---

### problem: timeout
**cause:** api is slow or unresponsive  
**fix:** increase timeout, add retry logic

```python
# increase timeout
response = requests.post(url, json=data, timeout=30)

# or retry
for attempt in range(3):
    try:
        response = requests.post(url, json=data, timeout=10)
        break
    except requests.exceptions.Timeout:
        if attempt == 2:
            raise
        print(f"timeout, retrying ({attempt + 1}/3)...")
```

---

### problem: connection error
**cause:** no internet or wrong url  
**fix:** check internet, verify url

```python
# verify url format
print(f"connecting to: {url}")

# test basic connectivity
response = requests.get("https://httpbin.org/get")
if response.status_code == 200:
    print("internet works, api url might be wrong")
```

---

## practice exercises

### exercise 1: add logging

**improve the email function with logging:**
```python
import logging

logging.basicConfig(level=logging.INFO)

def send_email_with_logging(to_email, subject, body):
    logging.info(f"attempting to send email to {to_email}")
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            logging.info("email sent successfully")
            return True
        else:
            logging.error(f"email failed: status {response.status_code}")
            return False
    
    except Exception as e:
        logging.error(f"email error: {e}")
        return False
```

---

### exercise 2: add retry logic

**retry failed requests automatically:**
```python
def send_email_with_retry(to_email, subject, body, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            
            if response.status_code == 200:
                return True
            
            if response.status_code == 429:
                # rate limited, wait before retry
                wait_time = 60 * (attempt + 1)
                print(f"rate limited, waiting {wait_time} seconds...")
                time.sleep(wait_time)
                continue
            
            # other error, don't retry
            return False
        
        except requests.exceptions.Timeout:
            if attempt == max_retries - 1:
                return False
            print(f"timeout, retrying ({attempt + 1}/{max_retries})...")
    
    return False
```

---

### exercise 3: validate before sending

**combine validation + api call:**
```python
def validate_and_send_email(email_data):
    # validate email format
    if "@" not in email_data["to_email"]:
        print("invalid email format")
        return False
    
    # validate subject not empty
    if not email_data["subject"] or len(email_data["subject"]) == 0:
        print("subject cannot be empty")
        return False
    
    # send if validation passes
    return send_email_simulation(
        to_email=email_data["to_email"],
        subject=email_data["subject"],
        body=email_data["body"]
    )
```

---

## code templates

### template 1: authenticated get request

```python
def get_with_auth(url, api_key):
    """get request with authentication."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"error: status {response.status_code}")
            return None
    
    except Exception as e:
        print(f"error: {e}")
        return None
```

---

### template 2: authenticated post request

```python
def post_with_auth(url, api_key, data):
    """post request with authentication."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": response.status_code}
    
    except Exception as e:
        return {"success": False, "error": str(e)}
```

---

### template 3: complete workflow

```python
def complete_workflow(input_data):
    """validate → process → send → log."""
    # step 1: validate
    if not validate_input(input_data):
        logging.error("validation failed")
        return False
    
    # step 2: process
    processed_data = process_data(input_data)
    
    # step 3: send via api
    result = send_via_api(processed_data)
    
    # step 4: log result
    if result["success"]:
        logging.info("workflow complete")
        return True
    else:
        logging.error(f"workflow failed: {result['error']}")
        return False
```

---

## day 24 preview: crud operations

**tomorrow you'll learn:**
- put requests (updating data)
- delete requests (removing data)
- complete crud (create, read, update, delete)
- managing resources via api
- building complete data management systems

**by end of day 24:**
- full api mastery (get, post, put, delete)
- can manage any api resource
- ready for rate limiting (day 25)

---

## achievements

- [x] understand api authentication
- [x] use api keys in headers
- [x] make post requests to create data
- [x] combine auth + post
- [x] build complete validation → api workflows
- [x] handle timeouts and errors
- [x] integrate week 3 + week 4 skills

**day 23 complete: 5/5 skills mastered ✓**

---

## file organization

**your day 23 structure:**
```
ai-operations-training/
├── day-23/
│   ├── day23_authentication.py (all examples)
│   └── day-23-notes.md (this file)
└── previous days...
```

---

## the simple summary

### **day 23 in three sentences:**

1. **authentication tells apis who you are (api key in headers)**
2. **post requests send data to create/update resources (vs get which just reads)**
3. **auth + post = real automation (emails, payments, ai)**

### **the pattern you'll use forever:**
```python
# every authenticated api call:
headers = {"Authorization": f"Bearer {api_key}"}
response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    # success
else:
    # handle error
```

**this pattern works for sendgrid, stripe, claude api, every api**

---

## honest self-assessment

**what you should understand (day 23):**
- [x] apis need authentication to identify users
- [x] api keys go in headers (not url)
- [x] post sends data, get reads data
- [x] json= parameter for sending data
- [x] error handling prevents crashes
- [x] combining validation + api = complete workflow

**what you don't understand yet (coming soon):**
- put/delete requests (day 24)
- rate limiting strategies (day 25)
- async requests (day 26)
- webhooks (week 5)
- building your own apis (much later)

---

## what we don't know

**pricing reality check:**

**we found (from fiverr search feb 21 2026):**
- simple api integration: €100-300
- complex integration: €300-800+
- basic automation: €15-20 starting

**we don't know:**
- what you could actually charge in dublin
- what irish small businesses pay
- monthly retainer feasibility
- your specific success rate
- client acquisition difficulty

**to find out:**
- test the market at day 56
- reach out to dublin businesses
- see what they're willing to pay
- adjust based on real feedback

---

## grade for day 23: a

**what went well:**
- all code working perfectly ✓
- understand auth + post ✓
- built complete workflow ✓
- caught fake statistics ✓
- demanded honesty ✓
- ready for crud operations ✓

**what to work on:**
- start thinking about client outreach
- practice explaining value to non-technical people
- consider how to package your skills

---

**created:** day 23 of ai operations training  
**your progress:** week 4, day 2 (23/168 days total - 13.7%)  
**next session:** day 24 - put/delete requests (crud operations)

**you've learned how to write data to apis.**  
**tomorrow: updating and deleting data.**  
**by end of week 4: complete api mastery.**
