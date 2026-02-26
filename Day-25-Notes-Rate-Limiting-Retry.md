# DAY 25: RATE LIMITING & RETRY LOGIC
## AI Operations Training - Week 4, Day 4

---

## what you learned today

### core skills:
- understand api rate limits and why they exist
- detect rate limit errors (429 status code)
- implement retry logic with exponential backoff
- build production-ready resilient api clients
- handle failures gracefully without crashing

### the architecture "why":
**days 22-24 taught you:** making api calls (get, post, put, delete)  
**day 25 teaches you:** making api calls that don't break in production

**the problem day 25 solves:**
```python
# days 22-24 (fragile)
response = requests.post(url, json=data)
# if api fails, code crashes
# if rate limited, request lost
# customer doesn't get email

# day 25 (resilient)
response = make_request_with_retry(url, json=data)
# if api fails, automatically retries
# if rate limited, waits and retries
# customer eventually gets email
```

**real business impact:**
- without retry: system breaks on first failure, manual cleanup required
- with retry: system handles failures automatically, professional reliability
- clients pay for systems that don't break

---

## the key concept: rate limiting

### what are rate limits?

**rate limit = maximum requests allowed in a time period**

**common limits (real data from api documentation):**
- sendgrid free: 100 emails/day
- sendgrid paid: 40,000 emails/day  
- stripe: 100 requests/second
- twitter: 300 tweets/3 hours
- github authenticated: 5,000 requests/hour

**when you exceed limits:**
1. api returns status code 429 (too many requests)
2. response includes retry-after header (seconds to wait)
3. your request is rejected (not processed)
4. if you keep trying, api might temporarily block you

### why apis have rate limits

**reasons:**
1. prevent server overload
2. ensure fair usage for all users
3. prevent abuse and spam
4. encourage paid plans for high volume

**business model:**
- free tier: low limits (100/day)
- paid tier: higher limits (40,000/day)
- enterprise: custom limits

---

## understanding status code 429

### what 429 means

**429 = too many requests**
- you've exceeded the rate limit
- slow down
- try again later

**response headers:**
```python
response.status_code == 429

# often includes retry-after header
retry_after = response.headers.get('Retry-After')
# returns seconds to wait before retrying
```

### detecting rate limits

```python
response = requests.post(url, json=data)

if response.status_code == 200:
    # success
    pass
elif response.status_code == 429:
    # rate limited
    retry_after = response.headers.get('Retry-After')
    if retry_after:
        wait_time = int(retry_after)
        print(f"wait {wait_time} seconds")
```

---

## the problem: code without retry logic

### fragile code example

```python
def send_email_basic(email):
    """
    no retry logic - breaks on first failure.
    """
    url = "https://api.sendgrid.com/v3/mail/send"
    
    response = requests.post(url, headers=headers, json=email_data)
    
    if response.status_code == 200:
        return True
    elif response.status_code == 429:
        print("rate limited!")
        return False  # just gives up
    else:
        return False
```

**what happens in production:**
```python
# send 100 confirmation emails
for customer in customers:
    success = send_email_basic(customer.email)
    # if api fails at customer #50:
    # - remaining 50 emails never sent
    # - no retry, just fails
    # - manual cleanup required
```

**business impact:**
- 50 customers don't get confirmations
- angry phone calls to luigi
- unprofessional
- you lose client

---

## solution 1: fixed delay retry

### basic retry with fixed wait

```python
def send_email_with_retry(email, max_retries=3):
    """
    retry with fixed 2 second delay.
    better than nothing, but not optimal.
    """
    url = "https://httpbin.org/status/429"
    
    for attempt in range(max_retries):
        response = requests.post(url, timeout=10)
        
        if response.status_code == 200:
            return True
        
        elif response.status_code == 429:
            if attempt < max_retries - 1:
                wait_time = 2  # fixed delay
                print(f"rate limited - waiting {wait_time}s")
                time.sleep(wait_time)
            else:
                print("max retries reached")
                return False
    
    return False
```

**your output:**
```
rate limited (attempt 1/3) - waiting 2s
rate limited (attempt 2/3) - waiting 2s
rate limited - max retries reached
failed after 3 attempts
```

**problem with fixed delays:**
- api might need 10 seconds to recover
- but you only wait 2 seconds each time
- keep hitting same limit
- never recovers
- wastes retries

---

## solution 2: exponential backoff (professional)

### what is exponential backoff?

**exponential backoff = wait progressively longer between retries**

**wait pattern:**
```python
wait_time = 2 ** attempt

attempt 0: 2^0 = 1 second
attempt 1: 2^1 = 2 seconds
attempt 2: 2^2 = 4 seconds
attempt 3: 2^3 = 8 seconds
attempt 4: 2^4 = 16 seconds
```

**why this works:**
- short initial wait (1s) for temporary glitches
- progressively longer waits for rate limits
- gives api time to recover
- industry standard pattern
- used by google, aws, stripe, all major apis

### exponential backoff implementation

```python
def send_email_with_backoff(email, max_retries=5):
    """
    retry with exponential backoff.
    professional standard approach.
    """
    url = "https://api.sendgrid.com/v3/mail/send"
    
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            
            if response.status_code == 200:
                if attempt > 0:
                    print(f"succeeded after {attempt + 1} attempts")
                return True
            
            elif response.status_code == 429:
                if attempt < max_retries - 1:
                    # exponential backoff
                    wait_time = 2 ** attempt
                    print(f"rate limited - waiting {wait_time}s")
                    time.sleep(wait_time)
                else:
                    return False
        
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
            else:
                return False
    
    return False
```

**wait progression:**
```
attempt 1: wait 1 second  (2^0)
attempt 2: wait 2 seconds (2^1)
attempt 3: wait 4 seconds (2^2)
attempt 4: wait 8 seconds (2^3)
attempt 5: wait 16 seconds (2^4)
total: 31 seconds over 5 attempts
```

---

## production-ready retry logic

### complete implementation

```python
import requests
import time

def make_request_with_retry(
    method,
    url,
    max_retries=5,
    initial_delay=1,
    max_delay=60,
    **kwargs
):
    """
    production-ready api request with exponential backoff.
    
    handles:
    - rate limits (429)
    - server errors (500s)
    - timeouts
    - connection errors
    
    parameters:
    - method: 'get', 'post', 'put', 'delete'
    - url: api endpoint
    - max_retries: maximum retry attempts (default 5)
    - initial_delay: starting wait time in seconds (default 1)
    - max_delay: maximum wait time in seconds (default 60)
    - **kwargs: additional arguments (headers, json, etc)
    
    returns: response object or None
    """
    
    for attempt in range(max_retries):
        try:
            # make request
            if method.lower() == 'get':
                response = requests.get(url, timeout=10, **kwargs)
            elif method.lower() == 'post':
                response = requests.post(url, timeout=10, **kwargs)
            elif method.lower() == 'put':
                response = requests.put(url, timeout=10, **kwargs)
            elif method.lower() == 'delete':
                response = requests.delete(url, timeout=10, **kwargs)
            else:
                return None
            
            # success (200, 201, 204)
            if response.status_code in [200, 201, 204]:
                if attempt > 0:
                    print(f"succeeded after {attempt + 1} attempts")
                return response
            
            # rate limited (429)
            elif response.status_code == 429:
                if attempt < max_retries - 1:
                    # check retry-after header
                    retry_after = response.headers.get('Retry-After')
                    
                    if retry_after:
                        # api told us how long to wait
                        wait_time = int(retry_after)
                        print(f"rate limited - api says wait {wait_time}s")
                    else:
                        # use exponential backoff
                        wait_time = min(initial_delay * (2 ** attempt), max_delay)
                        print(f"rate limited - backoff {wait_time}s")
                    
                    time.sleep(wait_time)
                else:
                    print(f"rate limited - max retries reached")
                    return None
            
            # server error (500-599) - retry
            elif 500 <= response.status_code < 600:
                if attempt < max_retries - 1:
                    wait_time = min(initial_delay * (2 ** attempt), max_delay)
                    print(f"server error {response.status_code} - retry in {wait_time}s")
                    time.sleep(wait_time)
                else:
                    print(f"server error - max retries reached")
                    return None
            
            # client error (400-499) - don't retry
            elif 400 <= response.status_code < 500:
                print(f"client error {response.status_code} - not retrying")
                return None
            
            else:
                print(f"unexpected status {response.status_code}")
                return None
        
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                wait_time = min(initial_delay * (2 ** attempt), max_delay)
                print(f"timeout - retry in {wait_time}s")
                time.sleep(wait_time)
            else:
                print(f"timeout - max retries reached")
                return None
        
        except requests.exceptions.ConnectionError:
            if attempt < max_retries - 1:
                wait_time = min(initial_delay * (2 ** attempt), max_delay)
                print(f"connection error - retry in {wait_time}s")
                time.sleep(wait_time)
            else:
                print(f"connection error - max retries reached")
                return None
        
        except Exception as e:
            print(f"unexpected error: {e}")
            return None
    
    return None
```

**what this handles:**

**retry these errors:**
- 429 (rate limit)
- 500-599 (server errors)
- timeout exceptions
- connection errors

**don't retry these:**
- 400-499 (client errors - your fault)
- 200-299 (success)
- unexpected exceptions

**respects retry-after header:**
- if api says "wait 30 seconds" → waits 30 seconds
- otherwise uses exponential backoff

**caps maximum wait:**
- won't wait more than 60 seconds (max_delay)
- prevents infinite waits

---

## usage examples

### example 1: send email with retry

```python
def send_confirmation_email(customer_email, reservation):
    """
    send reservation confirmation with automatic retry.
    """
    url = "https://api.sendgrid.com/v3/mail/send"
    
    email_data = {
        "personalizations": [{
            "to": [{"email": customer_email}],
            "subject": "Reservation Confirmed"
        }],
        "from": {"email": "noreply@luigis.com"},
        "content": [{
            "type": "text/plain",
            "value": f"Table for {reservation['party_size']} confirmed."
        }]
    }
    
    headers = {
        "Authorization": "Bearer SG.real_api_key_here",
        "Content-Type": "application/json"
    }
    
    # use production-ready retry
    response = make_request_with_retry(
        method='post',
        url=url,
        headers=headers,
        json=email_data,
        max_retries=5
    )
    
    if response:
        print("confirmation sent successfully")
        return True
    else:
        print("failed to send confirmation after retries")
        return False
```

---

### example 2: batch processing with retry

```python
def send_daily_confirmations(reservations):
    """
    send confirmation emails to all reservations.
    handles failures gracefully.
    """
    successful = 0
    failed = 0
    failed_emails = []
    
    for i, reservation in enumerate(reservations, 1):
        print(f"\n[{i}/{len(reservations)}] processing {reservation['customer']}")
        
        response = make_request_with_retry(
            method='post',
            url="https://api.sendgrid.com/v3/mail/send",
            headers=headers,
            json=email_data,
            max_retries=5
        )
        
        if response:
            successful += 1
            print("confirmation sent")
        else:
            failed += 1
            failed_emails.append(reservation['email'])
            print("failed after retries")
    
    # summary
    print(f"\ntotal: {len(reservations)}")
    print(f"successful: {successful}")
    print(f"failed: {failed}")
    
    if failed_emails:
        print("\nfailed emails (manual follow-up required):")
        for email in failed_emails:
            print(f"  - {email}")
    
    return successful, failed
```

**business value:**
- processes all reservations even if some fail
- tracks successes and failures
- logs failed emails for manual follow-up
- professional reporting
- system doesn't crash

---

## key concepts

### concept 1: retry vs don't retry

**when to retry:**
- 429 (rate limit) → temporary, retry
- 500-599 (server error) → temporary, retry
- timeout → temporary, retry
- connection error → temporary, retry

**when not to retry:**
- 400 (bad request) → your data is wrong, fix it
- 401 (unauthorized) → wrong api key, fix it
- 403 (forbidden) → no permission, can't retry
- 404 (not found) → resource doesn't exist, can't retry

**rule:**
- temporary problems → retry
- permanent problems → don't retry

---

### concept 2: exponential backoff is industry standard

**why everyone uses it:**
- proven effective
- respects server resources
- balances speed vs politeness
- recommended by google, aws, stripe

**alternative approaches (not recommended):**
- linear backoff (1s, 2s, 3s, 4s) → too slow
- fixed delay (2s, 2s, 2s, 2s) → doesn't adapt
- no delay (retry immediately) → hammers server

**exponential backoff (1s, 2s, 4s, 8s) → just right**

---

### concept 3: max delay prevents infinite waits

**why cap the delay:**
```python
# without cap
wait_time = 2 ** attempt
attempt 10: 2^10 = 1024 seconds (17 minutes!)
attempt 20: 2^20 = 1,048,576 seconds (12 days!)

# with cap (max_delay=60)
wait_time = min(2 ** attempt, 60)
attempt 6+: always 60 seconds maximum
```

**prevents:**
- unreasonably long waits
- system appearing frozen
- resource waste

**typical caps:**
- 30 seconds for user-facing requests
- 60 seconds for background jobs
- 300 seconds (5 min) for batch processing

---

### concept 4: respect retry-after header

**when api tells you how long to wait:**
```python
response.status_code == 429
retry_after = response.headers.get('Retry-After')
# retry_after might be: "30" (seconds) or "Wed, 21 Oct 2026 07:28:00 GMT" (date)

if retry_after:
    # use what api says
    wait_time = int(retry_after)
else:
    # fallback to exponential backoff
    wait_time = 2 ** attempt
```

**why this matters:**
- api knows its own limits best
- respects api's preferences
- prevents unnecessary retries
- professional behavior

---

## real business workflow

### luigi's nightly email batch

```python
def nightly_confirmation_batch():
    """
    runs every night at 10pm.
    sends confirmations for tomorrow's reservations.
    """
    # get tomorrow's reservations from database
    reservations = get_tomorrows_reservations()
    
    print(f"processing {len(reservations)} reservations")
    
    successful = 0
    failed = 0
    failed_list = []
    
    for reservation in reservations:
        # prepare email
        email_data = {
            "to": reservation['email'],
            "subject": f"Reservation Confirmed - {reservation['date']}",
            "body": f"Table for {reservation['party_size']} at {reservation['time']}"
        }
        
        # send with retry logic
        response = make_request_with_retry(
            method='post',
            url=sendgrid_url,
            headers=headers,
            json=email_data,
            max_retries=5
        )
        
        if response:
            successful += 1
            log_success(reservation)
        else:
            failed += 1
            failed_list.append(reservation)
            log_failure(reservation)
    
    # send summary to luigi
    send_summary_email(luigi_email, successful, failed, failed_list)
    
    return successful, failed
```

**what this provides:**
- automated nightly processing
- handles temporary failures automatically
- logs all successes and failures
- alerts luigi to any permanent failures
- professional and reliable

---

## troubleshooting guide

### problem: still getting 429 after retries
**cause:** wait times too short for api's rate limit  
**fix:** increase max_delay or max_retries

```python
# if api needs longer recovery
response = make_request_with_retry(
    url=url,
    max_retries=10,  # more attempts
    max_delay=120    # wait up to 2 minutes
)
```

---

### problem: code waits too long
**cause:** max_delay too high  
**fix:** reduce max_delay for user-facing requests

```python
# for user-facing (quick response needed)
response = make_request_with_retry(
    url=url,
    max_delay=10  # maximum 10 second wait
)

# for background jobs (can wait longer)
response = make_request_with_retry(
    url=url,
    max_delay=60  # can wait up to 1 minute
)
```

---

### problem: retrying client errors (400s)
**cause:** code retries errors it shouldn't  
**fix:** check error type before retrying

```python
# correct - don't retry client errors
if 400 <= response.status_code < 500:
    print("client error - not retrying")
    return None  # don't retry, it's our fault
```

---

### problem: infinite retries
**cause:** no max_retries limit  
**fix:** always set max_retries

```python
# wrong - could retry forever
while True:
    response = requests.post(url)
    if response.status_code == 200:
        break
    time.sleep(2)

# correct - limited retries
for attempt in range(max_retries):
    response = requests.post(url)
    if response.status_code == 200:
        return response
```

---

## practice exercises

### exercise 1: add jitter to backoff

**add randomness to prevent thundering herd:**
```python
import random

def exponential_backoff_with_jitter(attempt, initial_delay=1, max_delay=60):
    """
    exponential backoff with jitter.
    prevents all clients retrying at exact same time.
    """
    base_wait = min(initial_delay * (2 ** attempt), max_delay)
    
    # add random jitter (±25%)
    jitter = random.uniform(0.75, 1.25)
    wait_time = base_wait * jitter
    
    return wait_time


# usage
wait_time = exponential_backoff_with_jitter(attempt)
time.sleep(wait_time)
```

**why jitter helps:**
- 1000 clients hit rate limit at same time
- without jitter: all retry at exact same moment → hit limit again
- with jitter: retries spread out over time → gradual recovery

---

### exercise 2: retry with callback

**track retry attempts for monitoring:**
```python
def make_request_with_callback(url, on_retry=None, **kwargs):
    """
    retry with callback function for monitoring.
    """
    for attempt in range(5):
        response = requests.post(url, **kwargs)
        
        if response.status_code == 200:
            return response
        
        elif response.status_code == 429:
            if attempt < 4:
                wait_time = 2 ** attempt
                
                # call callback
                if on_retry:
                    on_retry(attempt, wait_time, response.status_code)
                
                time.sleep(wait_time)
    
    return None


# usage with monitoring
def log_retry(attempt, wait_time, status):
    print(f"retry {attempt}: status {status}, waiting {wait_time}s")
    # could also log to database, send alert, etc

response = make_request_with_callback(
    url,
    on_retry=log_retry
)
```

---

### exercise 3: circuit breaker pattern

**stop trying if api is completely down:**
```python
class CircuitBreaker:
    """
    circuit breaker: stops retrying if too many failures.
    """
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
    
    def call(self, func, *args, **kwargs):
        # if circuit open, don't even try
        if self.state == "open":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "half-open"
            else:
                raise Exception("circuit breaker open - api down")
        
        try:
            result = func(*args, **kwargs)
            
            # success - reset
            self.failure_count = 0
            self.state = "closed"
            return result
        
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            # too many failures - open circuit
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
            
            raise


# usage
breaker = CircuitBreaker(failure_threshold=5, timeout=60)

try:
    response = breaker.call(send_email, customer_email)
except Exception as e:
    print(f"circuit breaker: {e}")
```

---

## code templates

### template 1: simple retry wrapper

```python
def retry(func, max_retries=3):
    """
    simple retry decorator.
    """
    def wrapper(*args, **kwargs):
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                wait_time = 2 ** attempt
                time.sleep(wait_time)
    return wrapper


# usage
@retry(max_retries=5)
def send_email(email):
    response = requests.post(url, json=email)
    if response.status_code != 200:
        raise Exception(f"failed: {response.status_code}")
    return response
```

---

### template 2: async retry (advanced preview)

```python
import asyncio

async def async_retry(func, max_retries=5):
    """
    async retry with exponential backoff.
    preview of week 7 content.
    """
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt
            await asyncio.sleep(wait_time)


# usage (week 7)
async def send_email_async(email):
    # async http request
    pass

result = await async_retry(send_email_async, max_retries=5)
```

---

## what we don't know

**honest limitations:**

**we know (facts):**
- sendgrid free tier: 100 emails/day (from their docs)
- stripe: 100 requests/second (from their docs)
- exponential backoff is industry standard (google cloud docs)
- 429 status code means rate limited (http spec)

**we don't know:**
- exact failure rate of apis in production
- success rate improvement with vs without retry
- average time to recover from rate limits
- cost of downtime for specific businesses

**to find out:**
- implement retry logic in real systems
- monitor success/failure rates
- measure time to recovery
- track business impact

---

## day 26 preview: async requests & concurrency

**tomorrow you'll learn:**
- make multiple api requests simultaneously
- async/await pattern
- concurrent processing
- parallel api calls
- speed up batch operations

**by end of day 26:**
- process 100 emails in seconds not minutes
- make parallel api calls
- understand concurrency

---

## achievements

- [x] understand api rate limits
- [x] detect 429 status codes
- [x] implement exponential backoff
- [x] build production-ready retry logic
- [x] handle failures gracefully
- [x] process batches with error tracking

**day 25 complete: 6/6 skills mastered ✓**

---

## file organization

**your day 25 structure:**
```
ai-operations-training/
├── day-25/
│   ├── day25_rate_limiting.py (all examples)
│   └── day-25-notes.md (this file)
└── previous days...
```

---

## the simple summary

### **day 25 in three sentences:**

1. **apis have rate limits (requests per time period)**
2. **retry with exponential backoff (wait 1s, 2s, 4s, 8s, 16s)**
3. **production code handles failures automatically (don't crash)**

### **the retry pattern:**
```python
for attempt in range(max_retries):
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        return response  # success
    
    elif response.status_code == 429:
        wait_time = 2 ** attempt  # exponential backoff
        time.sleep(wait_time)
        # retry
    
    else:
        return None  # permanent failure
```

**this pattern makes systems production-ready**

---

## honest self-assessment

**what you should understand (day 25):**
- [x] apis limit requests per time period
- [x] 429 means "too many requests"
- [x] exponential backoff increases wait time
- [x] retry temporary errors, not permanent ones
- [x] production code needs retry logic

**what you don't understand yet (coming soon):**
- async/await syntax (day 26)
- concurrent requests (day 26)
- distributed rate limiting (week 10)
- custom rate limiters (week 12)

---

## grade for day 25: a

**what went well:**
- all code working ✓
- understand rate limits ✓
- understand exponential backoff ✓
- production-ready retry logic ✓
- realistic business examples ✓

**what to work on:**
- practice implementing retry in real projects
- experiment with different backoff strategies
- monitor retry success rates

---

**created:** day 25 of ai operations training  
**your progress:** week 4, day 4 (25/168 days total - 14.9%)  
**next session:** day 26 - async requests & concurrency

**you've built production-ready api clients.**  
**tomorrow: making them fast with concurrency.**  
**by end of week 4: professional api integration complete.**
