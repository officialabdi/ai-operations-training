import requests
import time
import json

print("=" * 60)
print("understanding api rate limits")
print("=" * 60)

def demonstrate_rate_limits():
    print("\ncommon api rate limits:")
    print("-" * 60)

    limits = {
        "sendgrid free": "100 emails/day",
        "sendgrid": "40,000 emails/day",
        "stripe": "100 requests/second",
        "twitter": "300 tweets/3 hours",
        "github": "5,000 requests/hour (authenticated)"
    }
    for api, limit in limits.items():
        print(f"{api:20} {limit}")

    print("\n" + "=" * 60)
    print("\nwhat happens when you exceed limits:")
    print("-" * 60)
    
    print("\n1. api returns status code 429 (too many requests)")
    print("2. response includes retry-after header (seconds to wait)")
    print("3. your request is rejected (not processed)")
    print("4. if you keep trying, api might block you temporarily")
    
    print("\n" + "=" * 60)
    print("\nwhy apis have rate limits:")
    print("-" * 60)
    
    print("\n1. prevent server overload")
    print("2. fair usage for all users")
    print("3. prevent abuse/spam")
    print("4. encourage paid plans for high volume")

demonstrate_rate_limits()

print("\n" + "=" * 60)
print("detecting rate limit errors")
print("=" * 60)

def send_email_basic(email):
    url = "https://httpbin.org/status/429"
    print(f"\nattempting to send email to {email}")

    try:
        response = requests.post(url, timeout=10)
        if response.status_code == 200:
            print(f"✓ email sent successfully")
            return True
        
        elif response.status_code == 429:
            print(f"✗ rate limit exceeded!")
            retry_after = response.headers.get('retry-after')
            if retry_after:
                print(f"   api says: wait {retry_after} seconds")
            else:
                print(f"   api didnt specify wait time")
                return False
        else:
            print(f" failed: status {response.status_code}")
            return False
    except Exception as e:
        print(f"error: {e}")
        return False
    
    print("\ntest: sending emails without retry logic")
print("-" * 60)

emails = ["customer1@email.com", "customer2@email.com", "customer3@email.com"]

for email in emails:
    result = send_email_basic(email)
    if not result:
        print(f"  → failed to send to {email}")

print("\n" + "=" * 60)
print("without retry logic: all emails failed")
print("professional code needs to handle this")
print("=" * 60)


# ========================================
# example 3: basic retry logic
# ========================================

print("\n" + "=" * 60)
print("basic retry logic with fixed delay")
print("=" * 60)

def send_email_with_retry(email, max_retries=3):
    """
    send email with retry logic.
    waits 2 seconds between retries.
    
    business context: ensures email eventually gets sent
    """
    url = "https://httpbin.org/status/429"
    
    print(f"\nattempting to send email to {email}")
    
    for attempt in range(max_retries):
        try:
            response = requests.post(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✓ email sent successfully")
                return True
            
            elif response.status_code == 429:
                if attempt < max_retries - 1:
                    wait_time = 2  # fixed 2 second wait
                    print(f"✗ rate limited (attempt {attempt + 1}/{max_retries})")
                    print(f"  waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                else:
                    print(f"✗ rate limited - max retries reached")
                    return False
            
            else:
                print(f"✗ failed: status {response.status_code}")
                return False
        
        except Exception as e:
            print(f"✗ error: {e}")
            if attempt < max_retries - 1:
                print(f"  retrying...")
                time.sleep(2)
            else:
                return False
    
    return False


# test: retry logic in action
print("\ntest: sending emails with basic retry logic")
print("-" * 60)

emails = ["customer1@email.com", "customer2@email.com"]

for email in emails:
    result = send_email_with_retry(email)
    if result:
        print(f"  → successfully sent to {email}")
    else:
        print(f"  → failed to send to {email} after 3 attempts")


# ========================================
# example 4: exponential backoff (professional)
# ========================================

print("\n" + "=" * 60)
print("exponential backoff - professional retry logic")
print("=" * 60)

def send_email_with_backoff(email, max_retries=5):
    """
    send email with exponential backoff.
    
    wait pattern:
    - attempt 1: wait 1 second
    - attempt 2: wait 2 seconds
    - attempt 3: wait 4 seconds
    - attempt 4: wait 8 seconds
    - attempt 5: wait 16 seconds
    
    business context: gives api time to recover
    """
    # use success endpoint to simulate eventual success
    url = "https://httpbin.org/status/200"
    
    print(f"\nattempting to send email to {email}")
    
    for attempt in range(max_retries):
        try:
            response = requests.post(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✓ email sent successfully on attempt {attempt + 1}")
                return True
            
            elif response.status_code == 429:
                if attempt < max_retries - 1:
                    # exponential backoff: 1, 2, 4, 8, 16 seconds
                    wait_time = 2 ** attempt
                    print(f"✗ rate limited (attempt {attempt + 1}/{max_retries})")
                    print(f"  waiting {wait_time} seconds (exponential backoff)...")
                    time.sleep(wait_time)
                else:
                    print(f"✗ rate limited - max retries reached")
                    return False
            
            else:
                print(f"✗ failed: status {response.status_code}")
                return False
        
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"✗ timeout (attempt {attempt + 1}/{max_retries})")
                print(f"  waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                print(f"✗ timeout - max retries reached")
                return False
        
        except Exception as e:
            print(f"✗ error: {e}")
            return False
    
    return False


# demonstrate exponential backoff pattern
print("\nexponential backoff wait times:")
print("-" * 60)

for attempt in range(5):
    wait_time = 2 ** attempt
    print(f"attempt {attempt + 1}: wait {wait_time} seconds")

print("\n" + "=" * 60)

# test: exponential backoff in action
print("\ntest: sending emails with exponential backoff")
print("-" * 60)

emails = ["customer1@email.com", "customer2@email.com", "customer3@email.com"]

for email in emails:
    result = send_email_with_backoff(email)
    if result:
        print(f"  → successfully sent to {email}\n")
    else:
        print(f"  → failed to send to {email}\n")

# ========================================
# example 5: production-ready retry function
# ========================================

import requests
import time
import json

print("\n" + "=" * 60)
print("production-ready retry logic")
print("=" * 60)

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
    
    parameters:
    - method: 'get', 'post', 'put', 'delete'
    - url: api endpoint
    - max_retries: maximum retry attempts
    - initial_delay: starting wait time (seconds)
    - max_delay: maximum wait time (seconds)
    - **kwargs: additional arguments for requests (headers, json, etc)
    
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
                print(f"unsupported method: {method}")
                return None
            
            # success
            if response.status_code in [200, 201, 204]:
                if attempt > 0:
                    print(f"✓ succeeded after {attempt + 1} attempts")
                return response
            
            # rate limited
            elif response.status_code == 429:
                if attempt < max_retries - 1:
                    # check retry-after header
                    retry_after = response.headers.get('Retry-After')
                    
                    if retry_after:
                        wait_time = int(retry_after)
                        print(f"rate limited - api says wait {wait_time}s")
                    else:
                        # exponential backoff
                        wait_time = min(initial_delay * (2 ** attempt), max_delay)
                        print(f"rate limited - exponential backoff: {wait_time}s")
                    
                    time.sleep(wait_time)
                else:
                    print(f"✗ rate limited - max retries ({max_retries}) reached")
                    return None
            
            # server error (500s) - retry
            elif 500 <= response.status_code < 600:
                if attempt < max_retries - 1:
                    wait_time = min(initial_delay * (2 ** attempt), max_delay)
                    print(f"server error {response.status_code} - retry in {wait_time}s")
                    time.sleep(wait_time)
                else:
                    print(f"✗ server error - max retries reached")
                    return None
            
            # client error (400s) - don't retry
            elif 400 <= response.status_code < 500:
                print(f"✗ client error {response.status_code} - not retrying")
                return None
            
            else:
                print(f"✗ unexpected status {response.status_code}")
                return None
        
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                wait_time = min(initial_delay * (2 ** attempt), max_delay)
                print(f"timeout - retry in {wait_time}s")
                time.sleep(wait_time)
            else:
                print(f"✗ timeout - max retries reached")
                return None
        
        except requests.exceptions.ConnectionError:
            if attempt < max_retries - 1:
                wait_time = min(initial_delay * (2 ** attempt), max_delay)
                print(f"connection error - retry in {wait_time}s")
                time.sleep(wait_time)
            else:
                print(f"✗ connection error - max retries reached")
                return None
        
        except Exception as e:
            print(f"✗ unexpected error: {e}")
            return None
    
    return None


# test: production-ready retry
print("\ntest: production-ready retry logic")
print("-" * 60)

# test 1: successful request
print("\ntest 1: normal successful request")
response = make_request_with_retry('get', 'https://httpbin.org/get')
if response:
    print(f"✓ response received: status {response.status_code}")

# test 2: simulate what you'd do in real code
print("\n" + "=" * 60)
print("\nreal usage example:")
print("-" * 60)

def send_confirmation_email(customer_email, reservation_details):
    """
    real business function using retry logic.
    """
    url = "https://httpbin.org/post"  # simulates sendgrid
    
    email_data = {
        "to": customer_email,
        "subject": "Reservation Confirmed",
        "body": f"Your table for {reservation_details['party_size']} is confirmed."
    }
    
    headers = {
        "Authorization": "Bearer fake_sendgrid_key",
        "Content-Type": "application/json"
    }
    
    print(f"\nsending confirmation to {customer_email}")
    
    response = make_request_with_retry(
        method='post',
        url=url,
        headers=headers,
        json=email_data
    )
    
    if response:
        print(f"✓ confirmation sent successfully")
        return True
    else:
        print(f"✗ failed to send confirmation after retries")
        return False


# send confirmation for reservation
reservation = {
    "customer": "john smith",
    "email": "john@email.com",
    "party_size": 4,
    "date": "2026-03-15"
}

success = send_confirmation_email(
    reservation["email"],
    reservation
)

print("\n" + "=" * 60)
print("production-ready retry logic complete")
print("=" * 60)