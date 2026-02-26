import requests
print("making api request...")
url = "https://api.github.com/users/github"
response = requests.get(url)
print(f"status code: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"\nuser found: {data['login']}")
    print(f"name: {data['name']}")
    print(f"public repos: {data['public_repos']}")
    print(f"followers: {data['followers']}")
else:
    print(f"error: request failed with status {response.status_code}")
# ========================================
# example 2: working with json data
# ========================================

print("\n" + "=" * 60)
print("working with json data")
print("=" * 60)

# make another request
url = "https://api.github.com/users/github/repos"
response = requests.get(url)

if response.status_code == 200:
    repos = response.json()
    
    print(f"\ntotal repositories returned: {len(repos)}")
    print("\nfirst 3 repositories:")
    
    # loop through first 3 repos
    for i in range(min(3, len(repos))):
        repo = repos[i]
        print(f"\n{i+1}. {repo['name']}")
        print(f"   description: {repo['description']}")
        print(f"   stars: {repo['stargazers_count']}")
        print(f"   language: {repo['language']}")
else:
    print(f"error: {response.status_code}")

print("\n" + "=" * 60)
print("api error handling")
print("=" * 60)

def get_user_data(username):
    url = f"https://api.github.com/users/{username}"
    try:
        print(f"\nfetching data for user: {username}")
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"success: user found")
            return response.json()
        elif response.status_code == 404:
            print(f"error: user '{username}' not found")
            return None
        else:
            print(f"error: api returned status {response.status_code}")
            return None
    except requests.Exceptions.timeout:
        print(f"error: request timed out after 5 seconds")
        return None
    except requests.exceptions.ConnectionError:
        print(f"error: could not connect to api (check internet)")
        return None
    except Exception as e:
        print(f"error: unexpected problem = {e}")
        return None
    
user_data = get_user_data("github")
if user_data:
    print(f"  followers: {user_data['followers']}")

# test with invalid user
user_data = get_user_data("this_user_definitely_does_not_exist_12345")

# test with empty username
user_data = get_user_data("")

# ========================================
# example 4: query parameters
# ========================================

print("\n" + "=" * 60)
print("using query parameters to filter data")
print("=" * 60)

def search_github_repos(query, language=None, sort="stars"):
    """
    search github repositories with filters.
    
    args:
        query: search term
        language: filter by programming language (optional)
        sort: sort results by stars, forks, or updated
    
    returns: list of repositories or empty list on failure
    """
    url = "https://api.github.com/search/repositories"
    
    # build parameters dictionary
    params = {
        "q": query,
        "sort": sort,
        "order": "desc",
        "per_page": 5
    }
    
    # add language filter if provided
    if language:
        params["q"] = f"{query} language:{language}"
    
    try:
        print(f"\nsearching for: {query}")
        if language:
            print(f"filtered by language: {language}")
        print(f"sorted by: {sort}")
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            total_count = data["total_count"]
            repos = data["items"]
            
            print(f"\nfound {total_count} repositories")
            print(f"showing top {len(repos)}:")
            
            for i, repo in enumerate(repos, 1):
                print(f"\n{i}. {repo['full_name']}")
                print(f"   description: {repo['description'][:80] if repo['description'] else 'no description'}...")
                print(f"   stars: {repo['stargazers_count']}")
                print(f"   language: {repo['language']}")
                print(f"   url: {repo['html_url']}")
            
            return repos
        else:
            print(f"error: api returned status {response.status_code}")
            return []
    
    except Exception as e:
        print(f"error: {e}")
        return []


# test 1: search for python machine learning repos
print("\n" + "=" * 60)
print("test 1: python machine learning repositories")
search_github_repos("machine learning", language="python")

# test 2: search for javascript frameworks sorted by stars
print("\n" + "=" * 60)
print("test 2: javascript frameworks")
search_github_repos("framework", language="javascript")

# test 3: search for api documentation
print("\n" + "=" * 60)
print("test 3: api documentation repositories")
search_github_repos("api documentation", sort="stars")

# ========================================
# example 5: request headers
# ========================================

print("\n" + "=" * 60)
print("using request headers")
print("=" * 60)

def get_user_with_headers(username):
    """
    get github user data with custom headers.
    demonstrates how headers work.
    """
    url = f"https://api.github.com/users/{username}"
    
    # custom headers
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Luigi-Pizzeria-Bot/1.0"
    }
    
    try:
        print(f"\nfetching {username} with custom headers")
        print(f"headers sent: {headers}")
        
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"\nsuccess!")
            print(f"rate limit remaining: {response.headers.get('X-RateLimit-Remaining')}")
            print(f"rate limit resets at: {response.headers.get('X-RateLimit-Reset')}")
            
            return data
        else:
            print(f"error: status {response.status_code}")
            return None
    
    except Exception as e:
        print(f"error: {e}")
        return None


# test with headers
user = get_user_with_headers("github")
if user:
    print(f"\nuser info:")
    print(f"  name: {user['name']}")
    print(f"  location: {user.get('location', 'not specified')}")
    print(f"  bio: {user.get('bio', 'no bio')}")

    # ========================================
# example 6: response object details
# ========================================

print("\n" + "=" * 60)
print("understanding response objects")
print("=" * 60)

def analyze_response(url):
    """show all parts of an api response."""
    print(f"\nanalyzing response from: {url}")
    
    try:
        response = requests.get(url, timeout=5)
        
        print("\n--- response details ---")
        print(f"status code: {response.status_code}")
        print(f"reason: {response.reason}")
        print(f"encoding: {response.encoding}")
        print(f"response time: {response.elapsed.total_seconds()} seconds")
        
        print("\n--- response headers (first 5) ---")
        for i, (key, value) in enumerate(response.headers.items()):
            if i >= 5:
                break
            print(f"{key}: {value}")
        
        print("\n--- response body preview ---")
        if response.status_code == 200:
            data = response.json()
            print(f"data type: {type(data)}")
            if isinstance(data, dict):
                print(f"keys: {list(data.keys())[:5]}")
            elif isinstance(data, list):
                print(f"list length: {len(data)}")
                if len(data) > 0:
                    print(f"first item type: {type(data[0])}")
        
        return response
    
    except Exception as e:
        print(f"error: {e}")
        return None


# analyze different endpoints
analyze_response("https://api.github.com/users/github")
analyze_response("https://api.github.com/users/github/repos")

# ========================================
# example 7: real-world weather api
# ========================================

print("\n" + "=" * 60)
print("practical example: weather api for luigi's outdoor seating")
print("=" * 60)

def get_weather_forecast(city):
    """
    get weather forecast for a city.
    uses wttr.in free api (no key required).
    
    business context: luigi checks weather to plan outdoor seating
    """
    url = f"https://wttr.in/{city}?format=j1"
    
    try:
        print(f"\nfetching weather for: {city}")
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # extract current conditions
            current = data["current_condition"][0]
            
            print(f"\ncurrent weather in {city}:")
            print(f"  temperature: {current['temp_C']}°C / {current['temp_F']}°F")
            print(f"  feels like: {current['FeelsLikeC']}°C / {current['FeelsLikeF']}°F")
            print(f"  conditions: {current['weatherDesc'][0]['value']}")
            print(f"  humidity: {current['humidity']}%")
            print(f"  wind: {current['windspeedKmph']} km/h")
            
            # decision for outdoor seating
            temp = int(current['temp_C'])
            conditions = current['weatherDesc'][0]['value'].lower()
            
            print(f"\noutdoor seating recommendation:")
            if temp >= 15 and 'rain' not in conditions:
                print("  ✓ good conditions for outdoor seating")
                print("  → prepare 8 outdoor tables")
            elif temp >= 10 and 'rain' not in conditions:
                print("  ⚠ moderate conditions")
                print("  → prepare 4 outdoor tables with heaters")
            else:
                print("  ✗ poor conditions for outdoor seating")
                print("  → keep outdoor area closed")
            
            return data
        else:
            print(f"error: status {response.status_code}")
            return None
    
    except Exception as e:
        print(f"error: {e}")
        return None


# get weather for dublin (luigi's location)
weather = get_weather_forecast("dublin")

# also check cork for potential new location
print("\n" + "=" * 60)
weather = get_weather_forecast("cork")

