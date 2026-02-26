import requests
import json

print("=" * 60)
print("understanding api authentication")
print("=" * 60)

def demo_authentication_method():
    print("\nmethod 1: api key in header")
    url = "https://httpbin.org/headers"
    headers = {
        "authorization": "bearer sk_test_fake_key_12345",
        "X-API-KEY": "my-secret-key"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
       data = response.json()
       print("headers sent:")
       print(json.dumps(data["headers"], indent=2))
    print("\n" + "-" * 60)
    print("method 2: api key in query parameter")
    url = "https://httpbin.org/get"

    params = {
        "api_key": "my-secret-key",
        "user_id": "luigi123"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        print(f"url called: {data['url']}")
        print(f"parameters sent: {data['args']}")

demo_authentication_method()  

print("\n" + "=" * 60)
print("post requests - sending data to apis")
print("=" * 60)

def demo_post_request():
    url = "https://httpbin.org/post"
    reservation_data = {
        "customer_name": "john smith",
        "email": "john@email.com",
        "date": "2026-03-15",
        "party_size": 4,
        "special_requests": "window seat please"
    }

    print("\nsending reservation data via post request:")
    print(json.dumps(reservation_data, indent=2))

    response = requests.post(url, json=reservation_data)

    if response.status_code == 200:
        result = response.json()

        print("\nserver received:")
        print(f"data sent: {result['json']}")
        print(f"content-type: {result['headers']['Content-Type']}")
        
        print("\npost request successful!")
        return result
    else:
        print(f"error: status {response.status_code}")
        return None
   
demo_post_request()

print("\n" + "=" * 60)
print("authenticated post - real client scenario")
print("=" * 60)

def send_email_simulation(to_email, subject, body):
    url = "https://httpbin.org/post"
    headers = {
        "authorization": "bearer sg.fake_sendgrid_key_1234",
        "content-type": "application/json"
    }

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
                "tpe": "text/plain",
                "value": body
            }
        ]
    }

    print(f"\nsending email to: {to_email}")
    print(f"subject: {subject}")
    print(f"authentication with apu key...")

    try:
        response = requests.post(url, json=email_data, headers=headers)
        if response.status_code == 200:
            print(f"\nemail sent successfully!")
            print(f"response time: {response.elapsed.total_seconds():.2f}seconds")

            result = response.json()
            print(f"\nserver confirmed receipt")
            return True
        else:
            print(f"failed to send email: status {response.status_code}")
            return False
    except Exception as e:
        print(f"error sending email: {e}")
        return False
    except Exception as e:
        print(f"error sending email: {e}")
        return False
    
print("\ntest 1: reservation confirmation")
send_email_simulation(
    to_email="customer@email.com",
    subject="Reservation Confirmed - Luigi's Pizzeria",
    body="Your table for 4 on 2026-03-15 at 7:00 PM is confirmed."
)

# test: reminder email
print("\n" + "=" * 60)
print("test 2: reservation reminder")
send_email_simulation(
    to_email="customer@email.com",
    subject="Reminder: Reservation Tomorrow",
    body="Reminder: reservation tomorrow at 7:00 PM for 4 people.")

# ========================================
# example 4: complete workflow
# ========================================

print("\n" + "=" * 60)
print("complete workflow: reservation to email")
print("=" * 60)

def process_reservation_and_send_confirmation(customer_data):
    """
    complete workflow:
    1. validate reservation data (week 3 skills)
    2. send confirmation via api (week 4 skills)
    
    this is what you'll build for clients.
    """
    print("\nstep 1: validating reservation data...")
    
    # validate required fields
    required_fields = ["name", "email", "date", "party_size"]
    for field in required_fields:
        if field not in customer_data or not customer_data[field]:
            print(f"validation failed: missing {field}")
            return False
    
    print("validation passed")
    
    # step 2: prepare email content
    print("\nstep 2: preparing confirmation email...")
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
    
    # step 3: send via api
    print("\nstep 3: sending confirmation email...")
    success = send_email_simulation(
        to_email=customer_data['email'],
        subject=subject,
        body=body
    )
    
    if success:
        print("\nworkflow complete: reservation processed and confirmed")
        return True
    else:
        print("\nworkflow failed: email not sent")
        return False


# test complete workflow
print("\ntest: complete reservation workflow")
reservation = {
    "name": "john smith",
    "email": "john@email.com",
    "date": "2026-03-15",
    "party_size": 4
}

result = process_reservation_and_send_confirmation(reservation)
print(f"\nfinal result: {'success' if result else 'failed'}")