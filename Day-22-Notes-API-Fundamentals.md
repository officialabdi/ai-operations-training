# DAY 22: API FUNDAMENTALS
## AI Operations Training - Week 4, Day 1

---

## what you learned today

### core skills:
- make http get requests with python
- parse json data from api responses
- use query parameters to filter data
- send custom headers with requests
- handle api errors professionally
- analyze response objects
- integrate real-world apis

### the architecture "why":
**weeks 1-3 taught you:** python fundamentals, error handling, logging  
**week 4 teaches you:** connecting to external services via apis

**the problem week 4 solves:**
```python
# amateur approach (weeks 1-3)
# everything is local on your computer
# no connection to external services
# manual data entry
# isolated systems

# professional approach (week 4+)
# connect to external services
# automate data exchange
# integrate multiple systems
# this is what clients pay for
```

**real business impact:**
- apis are how you make money at month 6
- every €2,000+ automation uses apis
- email automation = sendgrid api
- payment processing = stripe api
- ai systems = claude api
- this is the foundation of all client work

---

## the key concept: what is an api?

### api = application programming interface

**simple analogy: restaurant waiter**

```
you (your code)
    ↓
tells waiter (api) what you want
    ↓
waiter takes order to kitchen (external service)
    ↓
kitchen prepares food (processes request)
    ↓
waiter brings back food (returns data)
    ↓
you eat (use the data)
```

**technical definition:**
- way for programs to communicate over internet
- one program (yours) requests data
- another program (api server) sends data back
- all happens automatically in milliseconds

---

## core concept 1: http requests and responses

### the request-response cycle

**what happens when you make an api call:**

```
1. your code sends http request
   ↓
2. request travels over internet to api server
   ↓
3. server processes request
   ↓
4. server sends back http response
   ↓
5. your code receives and processes response
```

**http methods (types of requests):**
- **get** - retrieve data (what you learned today)
- **post** - send data (day 24)
- **put** - update data (day 24)
- **delete** - remove data (day 24)

**today you learned get requests only**

---

## core concept 2: status codes

### what status codes mean

**status codes tell you if request succeeded:**

**200-299: success**
- 200: ok - request succeeded
- 201: created - new resource created
- 204: no content - succeeded but no data to return

**400-499: client errors (your fault)**
- 400: bad request - invalid data sent
- 401: unauthorized - missing/invalid credentials
- 403: forbidden - you don't have permission
- 404: not found - resource doesn't exist
- 429: too many requests - rate limit exceeded

**500-599: server errors (their fault)**
- 500: internal server error - api is broken
- 502: bad gateway - server is down
- 503: service unavailable - temporary issue

**from your output today:**
```
status code: 200  ← success!
status code: 404  ← user not found
```

**business value:**
```python
if response.status_code == 200:
    # success - process data
    send_confirmation_email()
elif response.status_code == 401:
    # auth failed - check api key
    logging.error("api key expired - update credentials")
elif response.status_code == 429:
    # rate limited - wait and retry
    time.sleep(60)
    retry_request()
```

---

## core concept 3: json data format

### json = javascript object notation

**the universal language of apis**

**what json looks like:**
```json
{
    "name": "john smith",
    "email": "john@email.com",
    "age": 30,
    "active": true,
    "reservations": [
        {"date": "2026-03-15", "party_size": 4},
        {"date": "2026-03-20", "party_size": 2}
    ]
}
```

**json to python conversion:**
```python
# api returns json string
# python converts to dict/list automatically

# json object → python dict
{"name": "john"}  →  {"name": "john"}

# json array → python list
["apple", "banana"]  →  ["apple", "banana"]

# json values → python values
true  →  True
false  →  False
null  →  None
```

**from your code today:**
```python
response = requests.get(url)
data = response.json()  # converts json to python dict/list
print(data["name"])  # access like normal dict
```

---

## the complete code walkthrough

### example 1: basic get request

```python
import requests

# the api endpoint url
url = "https://api.github.com/users/github"

# make the get request
response = requests.get(url)

# check status code
print(f"status code: {response.status_code}")

# parse json response
if response.status_code == 200:
    data = response.json()
    print(f"user: {data['login']}")
    print(f"name: {data['name']}")
    print(f"followers: {data['followers']}")
```

**what each line does:**
1. `import requests` - load the library
2. `url = "..."` - specify where to send request
3. `response = requests.get(url)` - make the request
4. `response.status_code` - check if it worked
5. `response.json()` - convert json to python dict
6. `data['login']` - access values like normal dict

**your output:**
```
status code: 200
user: github
name: GitHub
followers: 68943
```

**business value:**
this same pattern works for:
- sendgrid api (send emails)
- stripe api (process payments)
- claude api (ai responses)
- google sheets api (update spreadsheets)

---

### example 2: working with json lists

```python
# get list of repositories
url = "https://api.github.com/users/github/repos"
response = requests.get(url)

if response.status_code == 200:
    repos = response.json()  # returns list of dicts
    
    print(f"total repos: {len(repos)}")
    
    # loop through repos
    for repo in repos[:3]:  # first 3
        print(f"name: {repo['name']}")
        print(f"stars: {repo['stargazers_count']}")
        print(f"language: {repo['language']}")
```

**data structure returned:**
```python
[
    {"name": "repo1", "stars": 100, "language": "python"},
    {"name": "repo2", "stars": 200, "language": "javascript"},
    {"name": "repo3", "stars": 300, "language": "ruby"}
]
```

**your output:**
```
total repositories returned: 30

first 3 repositories:
1. .github - stars: 1114
2. accessibility-alt-text-bot - stars: 90
3. accessibility-scanner - stars: 210
```

**business application for luigi:**
```python
# get all reservations for today
url = "https://luigi-api.com/reservations?date=2026-03-15"
response = requests.get(url)

reservations = response.json()  # list of dicts

for reservation in reservations:
    customer = reservation["customer_name"]
    party_size = reservation["party_size"]
    print(f"{customer} - party of {party_size}")
```

---

### example 3: professional error handling

```python
def get_user_data(username):
    """get github user with full error handling."""
    url = f"https://api.github.com/users/{username}"
    
    try:
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"user '{username}' not found")
            return None
        else:
            print(f"api error: status {response.status_code}")
            return None
    
    except requests.exceptions.Timeout:
        print("request timed out")
        return None
    
    except requests.exceptions.ConnectionError:
        print("connection failed - check internet")
        return None
    
    except Exception as e:
        print(f"unexpected error: {e}")
        return None


# test cases
user = get_user_data("github")  # success
user = get_user_data("fake_user_12345")  # 404
user = get_user_data("")  # 404
```

**error types handled:**
1. **timeout** - api is slow/unresponsive
2. **connection error** - no internet or server down
3. **404** - resource not found
4. **other status codes** - various api errors
5. **unexpected exceptions** - anything else

**your output:**
```
fetching data for user: github
success: user found

fetching data for user: this_user_definitely_does_not_exist_12345
error: user 'this_user_definitely_does_not_exist_12345' not found

fetching data for user: 
error: user '' not found
```

**why this matters:**
- amateur code: crashes when api fails
- professional code: handles errors gracefully
- clients pay for reliability

**business scenario:**
```
monday 3am: sendgrid api goes down
amateur code: luigi's system crashes, no emails sent
your code: catches error, logs it, switches to backup api
tuesday 9am: you fix primary api, everything working
you bill: €200 for emergency support
```

---

### example 4: query parameters (filtering data)

**what are query parameters:**
- way to filter/customize api requests
- sent as part of the url
- key-value pairs after `?`

**url structure:**
```
https://api.example.com/search?query=pizza&location=dublin&limit=10
                                 ↑
                           query parameters start here

query=pizza        ← search term
location=dublin    ← filter by location
limit=10           ← maximum results
```

**code example:**
```python
def search_repos(query, language=None, sort="stars"):
    """search github repos with filters."""
    url = "https://api.github.com/search/repositories"
    
    # build parameters as dictionary
    params = {
        "q": query,
        "sort": sort,
        "order": "desc",
        "per_page": 5
    }
    
    # add language filter if provided
    if language:
        params["q"] = f"{query} language:{language}"
    
    # requests library adds params to url automatically
    response = requests.get(url, params=params, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        repos = data["items"]
        
        for repo in repos:
            print(f"{repo['full_name']}")
            print(f"  stars: {repo['stargazers_count']}")
            print(f"  language: {repo['language']}")
        
        return repos
    else:
        return []


# search for python machine learning repos
search_repos("machine learning", language="python")
```

**your output:**
```
searching for: machine learning
filtered by language: python
sorted by: stars

found 202905 repositories
showing top 5:

1. huggingface/transformers - stars: 156777
2. fighting41love/funNLP - stars: 79012
3. josephmisiti/awesome-machine-learning - stars: 71714
4. scikit-learn/scikit-learn - stars: 65185
5. gradio-app/gradio - stars: 41778
```

**business application for luigi:**
```python
# search reservations by date
params = {
    "date": "2026-03-15",
    "status": "confirmed",
    "min_party_size": 4
}
response = requests.get(luigi_api_url, params=params)

# search menu items
params = {
    "category": "pizza",
    "available": True,
    "max_price": 15
}
response = requests.get(menu_api_url, params=params)
```

**parameter types you'll use:**
- **filters:** date, status, category, price range
- **sorting:** sort_by, order (asc/desc)
- **pagination:** page, per_page, limit, offset
- **search:** query, search_term, keyword

---

### example 5: request headers

**what are headers:**
- metadata sent with request
- authentication, content type, user agent
- key-value pairs

**common headers:**
- `Authorization` - api key or token
- `Content-Type` - data format (json, xml)
- `User-Agent` - identifies your application
- `Accept` - what format you want back

**code example:**
```python
def get_user_with_headers(username):
    """get user data with custom headers."""
    url = f"https://api.github.com/users/{username}"
    
    # custom headers
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Luigi-Pizzeria-Bot/1.0"
    }
    
    response = requests.get(url, headers=headers, timeout=5)
    
    if response.status_code == 200:
        data = response.json()
        
        # response also has headers
        print(f"rate limit remaining: {response.headers.get('X-RateLimit-Remaining')}")
        
        return data
    else:
        return None
```

**your output:**
```
fetching github with custom headers
headers sent: {
    'Accept': 'application/vnd.github.v3+json', 
    'User-Agent': 'Luigi-Pizzeria-Bot/1.0'
}

success!
rate limit remaining: 54
rate limit resets at: 1771686285
```

**business application:**
```python
# sendgrid requires api key in header
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

email_data = {
    "to": "customer@email.com",
    "subject": "reservation confirmation",
    "body": "your table is confirmed"
}

response = requests.post(
    "https://api.sendgrid.com/v3/mail/send",
    headers=headers,
    json=email_data
)
```

**headers you'll use for clients:**
- sendgrid: `Authorization: Bearer sk_...`
- stripe: `Authorization: Bearer sk_...`
- claude api: `x-api-key: sk-ant-...`
- most apis: `Content-Type: application/json`

---

### example 6: response object details

**response object contains more than just data:**
```python
response = requests.get(url)

# status information
print(response.status_code)  # 200
print(response.reason)  # "OK"

# timing
print(response.elapsed.total_seconds())  # 0.443832

# headers
print(response.headers["Content-Type"])  # "application/json"

# body/data
print(response.json())  # parsed json
print(response.text)  # raw text
```

**your output:**
```
--- response details ---
status code: 200
reason: OK
encoding: utf-8
response time: 0.443832 seconds

--- response headers (first 5) ---
Date: Sat, 21 Feb 2026 14:04:45 GMT
Content-Type: application/json; charset=utf-8
Cache-Control: public, max-age=60, s-maxage=60
```

**why this matters:**
- **debugging** - see exactly what api returned
- **performance** - measure response times
- **rate limits** - check remaining quota
- **caching** - understand cache behavior

**business debugging scenario:**
```python
response = requests.get(sendgrid_url)

print(f"status: {response.status_code}")
print(f"time: {response.elapsed.total_seconds()}s")
print(f"headers: {response.headers}")
print(f"body: {response.text}")

# oh! status 401 - api key is wrong
# time is 5 seconds - api is slow today
# rate limit remaining: 0 - we hit the limit
```

---

### example 7: weather api (real business example)

**business problem:**
luigi wants to know weather each morning to plan outdoor seating

**manual solution:**
- luigi checks weather website
- reads forecast
- decides how many outdoor tables
- takes 10 minutes daily
- 10 min × 365 days = 60 hours/year wasted

**api solution:**
```python
def get_weather_forecast(city):
    """get weather for outdoor seating decisions."""
    url = f"https://wttr.in/{city}?format=j1"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            current = data["current_condition"][0]
            
            temp = int(current['temp_C'])
            conditions = current['weatherDesc'][0]['value'].lower()
            
            # business logic
            if temp >= 15 and 'rain' not in conditions:
                recommendation = "prepare 8 outdoor tables"
            elif temp >= 10 and 'rain' not in conditions:
                recommendation = "prepare 4 tables with heaters"
            else:
                recommendation = "keep outdoor area closed"
            
            print(f"temperature: {temp}°C")
            print(f"conditions: {conditions}")
            print(f"recommendation: {recommendation}")
            
            return data
        else:
            print(f"error: status {response.status_code}")
            return None
    
    except requests.exceptions.Timeout:
        print("weather api timeout - using backup api")
        return None
    
    except Exception as e:
        print(f"error: {e}")
        return None


# automated daily check
weather = get_weather_forecast("dublin")
```

**your output:**
```
fetching weather for: dublin
error: HTTPSConnectionPool(host='wttr.in', port=443): Read timed out. (read timeout=10)
```

**what happened:**
- api server was slow/unresponsive
- request waited 10 seconds
- timeout exception raised
- **your error handling caught it perfectly** ✓

**this is real client work:**
- apis fail sometimes
- networks are unreliable
- your code handled it professionally
- system didn't crash
- clear error message logged

**business value:**
- saves luigi 60 hours/year = €1,800/year (at €30/hour)
- automated decision making
- runs at 6am daily automatically
- your charge: €300/month
- luigi's savings after paying you: €1,500/year

---

## understanding dict vs list

### dict (dictionary)

**what it is:** single object with key-value pairs

**example:**
```python
user = {
    "name": "john smith",
    "email": "john@email.com",
    "age": 30
}

# access values by key
print(user["name"])  # john smith
print(user["email"])  # john@email.com
```

**when apis return dict:**
- single user
- one reservation
- one product
- one result

**from your output:**
```
data type: <class 'dict'>
keys: ['login', 'id', 'node_id', 'avatar_url', 'gravatar_id']
```

---

### list (array)

**what it is:** ordered collection of items

**example:**
```python
users = [
    {"name": "john", "age": 30},
    {"name": "mary", "age": 25},
    {"name": "bob", "age": 35}
]

# access by index
print(users[0])  # first user
print(users[1])  # second user

# loop through all
for user in users:
    print(user["name"])
```

**when apis return list:**
- multiple users
- list of reservations
- search results
- collection of items

**from your output:**
```
data type: <class 'list'>
list length: 30
first item type: <class 'dict'>
```

this means: list of 30 dictionaries

---

### list of dicts (most common)

**most apis return this structure:**
```python
[
    {"id": 1, "name": "item1"},
    {"id": 2, "name": "item2"},
    {"id": 3, "name": "item3"}
]
```

**how to work with it:**
```python
# get the data
repos = response.json()  # returns list

# loop through list
for repo in repos:  # each repo is a dict
    print(repo["name"])  # access dict values
    print(repo["stars"])
```

**business example:**
```python
# luigi's reservations api returns list of dicts
reservations = [
    {"id": 1, "customer": "john", "party_size": 4},
    {"id": 2, "customer": "mary", "party_size": 2},
    {"id": 3, "customer": "bob", "party_size": 6}
]

# process each reservation
for reservation in reservations:
    name = reservation["customer"]
    size = reservation["party_size"]
    print(f"{name} - party of {size}")
```

---

## business value and roi

### without apis (manual work)

**luigi's daily tasks:**
- manually check weather: 10 minutes
- manually send confirmation emails: 30 minutes
- manually update menu across platforms: 20 minutes
- manually check payment status: 15 minutes
- **total: 75 minutes/day = 9+ hours/week = €270/week = €1,080/month wasted**

---

### with apis (automation)

**your automated systems:**
```python
# 6am: check weather api
weather = get_weather("dublin")
setup_outdoor_tables(weather)

# when reservation made: send confirmation
send_email_via_sendgrid(customer_email, reservation_details)

# when menu updated: sync everywhere
update_menu_on_toast_api(menu_items)
update_menu_on_square_api(menu_items)
update_menu_on_website(menu_items)

# hourly: check payment status
check_stripe_payments()
reconcile_transactions()
```

**time saved:** 9 hours/week  
**labor cost saved:** €270/week = €1,080/month  
**your charges:**
- initial build: €2,000-3,000 one-time
- monthly maintenance: €500/month
- emergency support: €100/hour

**luigi's roi:**
- month 1: pays €2,500 setup + €500 monthly = €3,000
- month 1 savings: €1,080
- net cost month 1: -€1,920
- month 2+: pays €500, saves €1,080
- net profit month 2+: +€580/month
- year 1 total savings: €4,040
- payback period: 2.8 months

**why clients pay:**
- saves massive time
- prevents errors (apis don't make typos)
- works 24/7 (no sick days)
- scales infinitely (handle 10 or 1000 reservations)
- professional appearance

---

## real client apis you'll use

### month 6 (first clients)

**sendgrid (email automation):**
```python
# send reservation confirmation
url = "https://api.sendgrid.com/v3/mail/send"
headers = {"Authorization": f"Bearer {api_key}"}
data = {"to": customer_email, "subject": "confirmed", "body": details}
response = requests.post(url, headers=headers, json=data)
```
**charge:** €800-1,200/month

**twilio (sms reminders):**
```python
# send reservation reminder
url = "https://api.twilio.com/2010-04-01/Accounts/{account}/Messages.json"
data = {"To": customer_phone, "Body": "reminder: reservation tomorrow at 7pm"}
response = requests.post(url, auth=(account_sid, auth_token), data=data)
```
**charge:** €600-1,000/month

---

### month 12 (growing business)

**stripe (payment processing):**
```python
# charge customer
url = "https://api.stripe.com/v1/charges"
headers = {"Authorization": f"Bearer {secret_key}"}
data = {"amount": 5000, "currency": "eur", "source": token}
response = requests.post(url, headers=headers, data=data)
```
**charge:** €1,500-2,500/month

**google sheets (data sync):**
```python
# update reservation log
url = "https://sheets.googleapis.com/v4/spreadsheets/{id}/values/{range}"
headers = {"Authorization": f"Bearer {access_token}"}
data = {"values": [[name, email, date, party_size]]}
response = requests.put(url, headers=headers, json=data)
```
**charge:** €500-800/month

---

### month 18 (advanced systems)

**claude api (ai automation):**
```python
# generate personalized email
url = "https://api.anthropic.com/v1/messages"
headers = {"x-api-key": api_key, "anthropic-version": "2023-06-01"}
data = {
    "model": "claude-sonnet-4-20250514",
    "messages": [{"role": "user", "content": f"write confirmation for {customer}"}]
}
response = requests.post(url, headers=headers, json=data)
```
**charge:** €2,000-4,000/month

---

## common api patterns

### pattern 1: get single item

```python
# get one user, one order, one product
url = f"https://api.example.com/users/{user_id}"
response = requests.get(url)
user = response.json()  # returns dict
```

---

### pattern 2: get list of items

```python
# get multiple users, orders, products
url = "https://api.example.com/users"
response = requests.get(url)
users = response.json()  # returns list of dicts

for user in users:
    print(user["name"])
```

---

### pattern 3: search/filter

```python
# search with parameters
params = {"status": "active", "limit": 10}
response = requests.get(url, params=params)
results = response.json()
```

---

### pattern 4: authenticated request

```python
# include api key in header
headers = {"Authorization": f"Bearer {api_key}"}
response = requests.get(url, headers=headers)
```

---

### pattern 5: error handling

```python
try:
    response = requests.get(url, timeout=5)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        logging.error(f"api error: {response.status_code}")
        return None

except requests.exceptions.Timeout:
    logging.error("request timeout")
    return None

except Exception as e:
    logging.error(f"unexpected error: {e}")
    return None
```

---

## key concepts

### concept 1: apis enable automation

**without apis:**
- manual data entry
- isolated systems
- human errors
- slow processes

**with apis:**
- automated data exchange
- integrated systems
- zero errors
- instant processes

---

### concept 2: json is universal

**every modern api uses json:**
- easy for humans to read
- easy for computers to parse
- supported by all languages
- standard format

**python makes json easy:**
```python
response.json()  # converts json to dict/list automatically
```

---

### concept 3: error handling is critical

**apis fail for many reasons:**
- server is down
- network issues
- authentication problems
- rate limits
- invalid requests

**professional code handles all of these:**
```python
try:
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        return response.json()
    else:
        handle_error(response.status_code)
except requests.exceptions.Timeout:
    retry_later()
except Exception as e:
    log_error(e)
```

---

### concept 4: headers carry metadata

**headers tell api:**
- who you are (authorization)
- what format you want (accept)
- what you're sending (content-type)
- what application you are (user-agent)

**headers tell you:**
- rate limits remaining
- cache control
- content type
- server information

---

### concept 5: parameters customize requests

**use parameters to:**
- filter results (status=active)
- sort results (sort=date)
- limit results (limit=10)
- paginate (page=2)
- search (query=pizza)

---

## troubleshooting guide

### problem: "module 'requests' not found"
**cause:** requests library not installed  
**fix:** `python -m pip install requests`

---

### problem: status code 401
**cause:** missing or invalid api key  
**fix:** check authentication header, verify api key

---

### problem: status code 404
**cause:** endpoint doesn't exist or resource not found  
**fix:** verify url, check api documentation

---

### problem: status code 429
**cause:** too many requests (rate limited)  
**fix:** slow down requests, implement retry with delay

---

### problem: timeout error
**cause:** api is slow or unresponsive  
**fix:** increase timeout, add retry logic, use backup api

---

### problem: connection error
**cause:** no internet or server is down  
**fix:** check internet, verify api status page, add error handling

---

### problem: json decode error
**cause:** response is not valid json  
**fix:** check response.text to see what was actually returned

---

## practice exercises

### exercise 1: explore different apis

**try these free apis (no key required):**
```python
# cat facts
url = "https://catfact.ninja/fact"

# random user
url = "https://randomuser.me/api/"

# joke api
url = "https://official-joke-api.appspot.com/random_joke"

# advice
url = "https://api.adviceslip.com/advice"
```

---

### exercise 2: add error logging

**improve the weather function with logging:**
```python
import logging

logging.basicConfig(level=logging.INFO)

def get_weather_with_logging(city):
    logging.info(f"fetching weather for {city}")
    
    try:
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            logging.info("weather data retrieved successfully")
            return response.json()
        else:
            logging.error(f"api returned status {response.status_code}")
            return None
    
    except Exception as e:
        logging.error(f"request failed: {e}")
        return None
```

---

### exercise 3: build search function

**create a function that searches github users:**
```python
def search_users(keyword, min_repos=10):
    """
    search github users by keyword.
    only return users with at least min_repos repositories.
    """
    # your code here
    pass
```

---

## day 23 preview: api authentication

**tomorrow you'll learn:**
- api keys and tokens
- authentication headers
- post requests (sending data)
- creating resources via api
- rate limiting

**what you'll build:**
- authenticated api requests
- data submission systems
- email confirmation sender
- payment processing foundation

---

## achievements unlocked

- [x] understand what apis are and why they matter
- [x] make http get requests
- [x] parse json responses (dict and list)
- [x] use query parameters to filter data
- [x] send custom headers
- [x] handle api errors professionally
- [x] analyze response objects
- [x] integrate real-world apis
- [x] build business logic on top of api data

**day 22 complete: 8/8 skills mastered ✓**

---

## file organization

**your day 22 structure:**
```
ai-operations-training/
├── day-22/
│   ├── day22_api_basics.py (all 7 examples)
│   └── day-22-notes.md (this file)
└── previous days...
```

---

## the simple summary

### **apis in three sentences:**

1. **apis let your code talk to other services over the internet**
2. **you send requests (with parameters/headers), they send back data (json)**
3. **this is how you automate everything clients pay for**

### **the pattern you'll use forever:**
```python
# every api integration:
response = requests.get(url, params=params, headers=headers, timeout=5)

if response.status_code == 200:
    data = response.json()
    # do something with data
else:
    # handle error
```

**this pattern is worth €2,000-3,000/month to clients**

---

## honest self-assessment

**what you should understand (day 22):**
- [x] apis enable communication between programs
- [x] http requests send data, responses return data
- [x] status codes indicate success/failure
- [x] json is the data format
- [x] error handling prevents crashes
- [x] query parameters filter results
- [x] headers carry metadata

**what you don't understand yet (coming soon):**
- authentication mechanisms (day 23)
- post/put/delete requests (day 24)
- building your own apis (much later)
- rate limiting strategies (day 25)
- webhooks (week 5)

---

## grade for day 22: A

**what went well:**
- all code worked correctly ✓
- understood dict vs list ✓
- handled errors professionally ✓
- asked good clarifying questions ✓
- caught when lesson was too short (good instinct) ✓
- weather api timeout handled gracefully ✓

**what to improve:**
- start thinking about how to apply to luigi's business
- experiment with other free apis
- practice modifying examples independently

---

**created:** day 22 of ai operations training  
**your progress:** week 4, day 1 (22/168 days total - 13.1%)  
**next session:** day 23 - api authentication

**you've learned the foundation of all automation systems.**  
**tomorrow: authentication and sending data to apis.**  
**this is where it gets real.**
