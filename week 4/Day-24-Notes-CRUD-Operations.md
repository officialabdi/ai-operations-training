# DAY 24: PUT/DELETE REQUESTS & CRUD OPERATIONS
## AI Operations Training - Week 4, Day 3

---

## what you learned today

### core skills:
- make put requests to update existing data
- make delete requests to remove data
- understand complete crud operations (create, read, update, delete)
- decide which http method to use for each scenario
- manage complete resource lifecycles via api

### the architecture "why":
**days 22-23 taught you:** reading and creating data (get, post)  
**day 24 teaches you:** updating and deleting data (put, delete)

**the problem day 24 solves:**
```python
# days 22-23 (incomplete control)
response = requests.get(url)    # can read ✓
response = requests.post(url, json=data)  # can create ✓
# but can't update or delete ✗

# day 24 (complete control)
response = requests.get(url)     # read ✓
response = requests.post(url, json=data)   # create ✓
response = requests.put(url, json=data)    # update ✓
response = requests.delete(url)  # delete ✓
# full resource management ✓
```

**real business impact:**
- without put/delete: can add menu items but can't change prices or remove items
- with complete crud: full control over all data
- this is how real businesses manage inventory, orders, customers

---

## the key concept: crud operations

### what is crud?

**crud = four basic operations on data**

| letter | operation | http method | purpose |
|--------|-----------|-------------|---------|
| c | create | post | add new resource |
| r | read | get | retrieve resource |
| u | update | put | modify resource |
| d | delete | delete | remove resource |

**together = complete data management**

---

## understanding http methods

### the four methods compared

**get (day 22):**
- retrieve/read data
- doesn't change anything
- no request body
- safe to repeat
- example: view menu, check order status

**post (day 23):**
- create new resource
- changes server state
- has request body
- not safe to repeat (creates duplicate)
- example: place order, add menu item

**put (day 24):**
- update existing resource
- changes server state
- has request body
- safe to repeat (same result)
- example: change price, update address

**delete (day 24):**
- remove resource
- changes server state
- usually no request body
- safe to repeat (already deleted)
- example: cancel order, remove item

---

## core concept 1: put requests

### what put does

**put = update existing resource by replacing it**

**characteristics:**
- requires resource id in url
- sends complete updated object
- replaces entire resource
- returns updated resource or confirmation

### put request structure

```python
# update existing menu item
url = f"https://api.luigis.com/menu/{item_id}"

updated_data = {
    "id": 1,
    "name": "margherita pizza",
    "description": "tomato, mozzarella, basil",
    "price": 14.00,  # updated from 12.00
    "category": "pizza",
    "available": True
}

response = requests.put(url, json=updated_data)
```

**key points:**
- url includes item id: `/menu/1`
- send entire object, not just changed field
- even if only price changed, send all fields

---

## core concept 2: delete requests

### what delete does

**delete = remove resource completely**

**characteristics:**
- requires resource id in url
- usually no request body
- permanent removal
- returns success or not found

### delete request structure

```python
# delete menu item
url = f"https://api.luigis.com/menu/{item_id}"

response = requests.delete(url)

if response.status_code == 200:
    print("deleted successfully")
elif response.status_code == 404:
    print("item not found (already deleted)")
```

**key points:**
- url includes item id: `/menu/5`
- no json body needed
- can't undo without recreating
- 404 means already gone

---

## the complete code examples

### example 1: put request (updating data)

```python
import requests
import json

def update_menu_item(item_id, updated_data):
    """
    update existing menu item using put request.
    
    business context: luigi updates pizza price or description
    """
    url = f"https://httpbin.org/put"
    
    # in real api:
    # url = f"https://api.luigis.com/menu/{item_id}"
    
    print(f"\nupdating item {item_id}")
    print("updated data:")
    print(json.dumps(updated_data, indent=2))
    
    try:
        response = requests.put(url, json=updated_data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\nitem updated successfully!")
            print(f"server received: {result['json']}")
            return True
        else:
            print(f"update failed: status {response.status_code}")
            return False
    
    except requests.exceptions.Timeout:
        print("update timeout")
        return False
    
    except Exception as e:
        print(f"error: {e}")
        return False


# test: update margherita pizza price
menu_item = {
    "id": 1,
    "name": "margherita pizza",
    "description": "tomato, mozzarella, basil",
    "price": 14.00,  # updated from 12.00
    "category": "pizza",
    "available": True
}

update_menu_item(item_id=1, updated_data=menu_item)
```

**your output:**
```
updating item 1
updated data:
{
  "id": 1,
  "name": "margherita pizza",
  "description": "tomato, mozzarella, basil",
  "price": 14.0,
  "category": "pizza",
  "available": true
}

item updated successfully
server received: {
  'id': 1,
  'name': 'margherita pizza',
  'description': 'tomato, mozzarella, basil',
  'price': 14.0,
  'category': 'pizza',
  'available': True
}
```

**what happened:**
- sent complete updated menu item
- only price changed (€12 → €14)
- but put requires sending entire object
- server confirmed update

---

### example 2: delete request (removing data)

```python
def delete_menu_item(item_id):
    """
    delete menu item using delete request.
    
    business context: luigi removes sold-out or discontinued items
    """
    url = f"https://httpbin.org/delete"
    
    # in real api:
    # url = f"https://api.luigis.com/menu/{item_id}"
    
    print(f"\ndeleting item {item_id}")
    
    try:
        response = requests.delete(url, timeout=10)
        
        if response.status_code == 200:
            print(f"\nitem {item_id} deleted successfully!")
            return True
        elif response.status_code == 404:
            print(f"item {item_id} not found (already deleted?)")
            return False
        else:
            print(f"delete failed: status {response.status_code}")
            return False
    
    except requests.exceptions.Timeout:
        print("delete timeout")
        return False
    
    except Exception as e:
        print(f"error: {e}")
        return False


# test: delete sold-out item
delete_menu_item(item_id=5)
```

**your output:**
```
deleting item 5

item 5 deleted successfully!
```

**what happened:**
- sent delete request for item 5
- no body needed (just url with id)
- item removed from system
- permanent deletion

---

### example 3: complete crud operations class

```python
class MenuAPI:
    """
    complete crud operations for luigi's menu.
    demonstrates all four http methods.
    """
    
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def create_item(self, item_data):
        """create new menu item (POST)"""
        url = f"{self.base_url}/post"
        
        print(f"\n[CREATE] adding new item: {item_data['name']}")
        
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=item_data,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✓ created: {item_data['name']}")
                return True
            else:
                print(f"✗ failed: status {response.status_code}")
                return False
        
        except Exception as e:
            print(f"✗ error: {e}")
            return False
    
    def read_item(self, item_id):
        """read menu item (GET)"""
        url = f"{self.base_url}/get"
        
        print(f"\n[READ] fetching item {item_id}")
        
        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✓ retrieved item data")
                return response.json()
            else:
                print(f"✗ failed: status {response.status_code}")
                return None
        
        except Exception as e:
            print(f"✗ error: {e}")
            return None
    
    def update_item(self, item_id, updated_data):
        """update menu item (PUT)"""
        url = f"{self.base_url}/put"
        
        print(f"\n[UPDATE] updating item {item_id}: {updated_data['name']}")
        print(f"  new price: €{updated_data['price']}")
        
        try:
            response = requests.put(
                url,
                headers=self.headers,
                json=updated_data,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✓ updated: {updated_data['name']}")
                return True
            else:
                print(f"✗ failed: status {response.status_code}")
                return False
        
        except Exception as e:
            print(f"✗ error: {e}")
            return False
    
    def delete_item(self, item_id, item_name):
        """delete menu item (DELETE)"""
        url = f"{self.base_url}/delete"
        
        print(f"\n[DELETE] removing item {item_id}: {item_name}")
        
        try:
            response = requests.delete(
                url,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✓ deleted: {item_name}")
                return True
            else:
                print(f"✗ failed: status {response.status_code}")
                return False
        
        except Exception as e:
            print(f"✗ error: {e}")
            return False


# demonstrate complete crud workflow
api = MenuAPI(
    base_url="https://httpbin.org",
    api_key="fake_luigis_api_key_12345"
)

# morning: add new seasonal pizza
new_pizza = {
    "id": 10,
    "name": "autumn truffle pizza",
    "description": "truffle oil, mushrooms, parmesan",
    "price": 18.00,
    "category": "pizza",
    "available": True
}
api.create_item(new_pizza)

# afternoon: check menu item details
api.read_item(item_id=10)

# evening: price increase due to truffle cost
updated_pizza = {
    "id": 10,
    "name": "autumn truffle pizza",
    "description": "truffle oil, mushrooms, parmesan",
    "price": 20.00,  # increased from 18.00
    "category": "pizza",
    "available": True
}
api.update_item(item_id=10, updated_data=updated_pizza)

# end of season: remove truffle pizza
api.delete_item(item_id=10, item_name="autumn truffle pizza")
```

**your output:**
```
[CREATE] adding new item: autumn truffle pizza
✓ created: autumn truffle pizza

[READ] fetching item 10
✓ retrieved item data

[UPDATE] updating item 10: autumn truffle pizza
  new price: €20.0
✓ updated: autumn truffle pizza

[DELETE] removing item 10: autumn truffle pizza
✓ deleted: autumn truffle pizza
```

**what this demonstrates:**
- complete lifecycle of a resource
- all four crud operations in order
- real business workflow (seasonal item)
- professional class structure

---

## crud decision framework

### when to use each method

**decision tree:**
```
question: does the resource exist yet?

├─ no → use POST (create)
│   example: new order, new customer, new menu item
│
└─ yes → what do you want to do?
    │
    ├─ just view it → use GET (read)
    │   example: check order status, view menu
    │
    ├─ change it → use PUT (update)
    │   example: update price, change address
    │
    └─ remove it → use DELETE (delete)
        example: cancel order, discontinue item
```

### business scenarios

**scenario 1: customer orders pizza**
- action: create new order
- method: **POST**
- why: order doesn't exist yet, creating new resource

**scenario 2: check order status**
- action: retrieve order details
- method: **GET**
- why: reading existing data, not changing anything

**scenario 3: customer changes delivery address**
- action: update order with new address
- method: **PUT**
- why: order exists, updating existing resource

**scenario 4: customer cancels order**
- action: remove order from system
- method: **DELETE**
- why: deleting resource completely

**scenario 5: luigi updates all menu prices +€1**
- action: update each menu item price
- method: **PUT** (for each item)
- why: items exist, updating existing resources

**scenario 6: view today's reservations**
- action: get list of reservations
- method: **GET**
- why: reading data only, no changes

---

## realistic business workflow

### luigi's daily operations

```python
def luigis_daily_workflow():
    """
    complete day using all crud operations.
    """
    
    # 8:00 AM - opening
    print("8:00 AM - opening preparation")
    
    # create today's special
    special = {
        "id": 99,
        "name": "sunday special - quattro formaggi",
        "price": 16.00,
        "available": True
    }
    # POST - create new item
    print(f"[POST] added: {special['name']} at €{special['price']}")
    
    # check menu
    # GET - verify menu complete
    print(f"[GET] retrieved menu items")
    
    # 12:00 PM - lunch rush
    print("\n12:00 PM - lunch rush")
    
    # high demand - increase price
    special['price'] = 18.00
    # PUT - update price
    print(f"[PUT] updated price: €{special['price']}")
    
    # customer checks menu
    # GET - customer views menu
    print(f"[GET] customer sees price: €{special['price']}")
    
    # customer orders
    order = {
        "id": 501,
        "items": ["sunday special"],
        "total": 18.00
    }
    # POST - create order
    print(f"[POST] order #{order['id']} created")
    
    # 3:00 PM - slow period
    print("\n3:00 PM - slow period")
    
    # reduce price
    special['price'] = 15.00
    # PUT - update price again
    print(f"[PUT] reduced price: €{special['price']}")
    
    # 8:00 PM - closing
    print("\n8:00 PM - closing time")
    
    # sold out
    special['available'] = False
    # PUT - update availability
    print(f"[PUT] marked unavailable")
    
    # 10:00 PM - cleanup
    print("\n10:00 PM - end of day")
    
    # remove special
    # DELETE - remove item
    print(f"[DELETE] removed: {special['name']}")
    
    # check tomorrow
    # GET - review menu
    print(f"[GET] menu ready for tomorrow")


luigis_daily_workflow()
```

**your output:**
```
8:00 AM - opening preparation
[POST] added: sunday special - quattro formaggi at €16.0
[GET] retrieved menu items

12:00 PM - lunch rush
[PUT] updated price: €18.0
[GET] customer sees price: €18.0
[POST] order #501 created

3:00 PM - slow period
[PUT] reduced price: €15.0

8:00 PM - closing time
[PUT] marked unavailable

10:00 PM - end of day
[DELETE] removed: sunday special - quattro formaggi
[GET] menu ready for tomorrow
```

**what this shows:**
- all four methods used in realistic sequence
- multiple updates to same resource (price changes)
- complete lifecycle from creation to deletion
- this is exactly how real businesses operate

---

## understanding put vs post

### key differences

**post (create):**
```python
# no id in url - server assigns id
url = "https://api.luigis.com/menu"

new_item = {
    # no id - will be assigned
    "name": "new pizza",
    "price": 12.00
}

response = requests.post(url, json=new_item)
# server returns: {"id": 15, "name": "new pizza", "price": 12.00}
```

**put (update):**
```python
# id in url - updating specific item
url = "https://api.luigis.com/menu/15"

updated_item = {
    "id": 15,  # must match url
    "name": "new pizza",
    "price": 14.00  # updated
}

response = requests.put(url, json=updated_item)
# server returns: {"id": 15, "name": "new pizza", "price": 14.00}
```

**summary:**
- post: url without id, creates new
- put: url with id, updates existing

---

## real api patterns

### pattern 1: menu management (stripe products)

```python
# create product
url = "https://api.stripe.com/v1/products"
product = {
    "name": "premium membership",
    "description": "monthly subscription"
}
response = requests.post(url, headers=headers, data=product)

# read product
product_id = "prod_abc123"
url = f"https://api.stripe.com/v1/products/{product_id}"
response = requests.get(url, headers=headers)

# update product
url = f"https://api.stripe.com/v1/products/{product_id}"
updates = {
    "name": "premium membership pro",
    "description": "monthly subscription with extras"
}
response = requests.post(url, headers=headers, data=updates)
# note: stripe uses POST for updates, not PUT (unusual)

# delete product
url = f"https://api.stripe.com/v1/products/{product_id}"
response = requests.delete(url, headers=headers)
```

---

### pattern 2: contact management (sendgrid)

```python
# create contact
url = "https://api.sendgrid.com/v3/marketing/contacts"
contact = {
    "email": "customer@email.com",
    "first_name": "john",
    "last_name": "smith"
}
response = requests.put(url, headers=headers, json={"contacts": [contact]})

# read contact
contact_id = "abc123"
url = f"https://api.sendgrid.com/v3/marketing/contacts/{contact_id}"
response = requests.get(url, headers=headers)

# update contact (upsert - creates if doesn't exist)
url = "https://api.sendgrid.com/v3/marketing/contacts"
updated_contact = {
    "email": "customer@email.com",
    "first_name": "john",
    "last_name": "smith-jones"  # updated
}
response = requests.put(url, headers=headers, json={"contacts": [updated_contact]})

# delete contact
contact_id = "abc123"
url = f"https://api.sendgrid.com/v3/marketing/contacts?ids={contact_id}"
response = requests.delete(url, headers=headers)
```

---

### pattern 3: data management (google sheets)

```python
# create row (append)
url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/Sheet1:append"
row_data = {
    "values": [["john smith", "john@email.com", "2026-03-15"]]
}
response = requests.post(url, headers=headers, json=row_data)

# read rows
url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/Sheet1!A1:C10"
response = requests.get(url, headers=headers)

# update row
url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/Sheet1!A2:C2"
updated_data = {
    "values": [["john smith", "newemail@email.com", "2026-03-15"]]
}
response = requests.put(url, headers=headers, json=updated_data)

# delete row (clear values)
url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/Sheet1!A2:C2:clear"
response = requests.post(url, headers=headers)
```

---

## error handling for crud operations

### common errors by method

**put errors:**
```python
response = requests.put(url, json=data)

if response.status_code == 200:
    # success
    pass
elif response.status_code == 404:
    # item doesn't exist - can't update
    print("item not found - use POST to create")
elif response.status_code == 400:
    # invalid data
    print("invalid update data")
elif response.status_code == 409:
    # conflict (version mismatch, concurrent edit)
    print("conflict - resource was modified by someone else")
```

**delete errors:**
```python
response = requests.delete(url)

if response.status_code == 200:
    # success
    pass
elif response.status_code == 204:
    # success, no content returned
    pass
elif response.status_code == 404:
    # already deleted or never existed
    print("item not found")
elif response.status_code == 409:
    # can't delete (dependencies exist)
    print("can't delete - other resources depend on this")
```

---

## professional crud implementation

### complete error handling

```python
class CRUDClient:
    """
    professional crud client with full error handling.
    """
    
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def create(self, resource, data):
        """create new resource"""
        url = f"{self.base_url}/{resource}"
        
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=data,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": f"status {response.status_code}"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def read(self, resource, resource_id=None):
        """read resource(s)"""
        url = f"{self.base_url}/{resource}"
        if resource_id:
            url = f"{url}/{resource_id}"
        
        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            elif response.status_code == 404:
                return {"success": False, "error": "not found"}
            else:
                return {"success": False, "error": f"status {response.status_code}"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def update(self, resource, resource_id, data):
        """update resource"""
        url = f"{self.base_url}/{resource}/{resource_id}"
        
        try:
            response = requests.put(
                url,
                headers=self.headers,
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            elif response.status_code == 404:
                return {"success": False, "error": "not found"}
            elif response.status_code == 409:
                return {"success": False, "error": "conflict"}
            else:
                return {"success": False, "error": f"status {response.status_code}"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def delete(self, resource, resource_id):
        """delete resource"""
        url = f"{self.base_url}/{resource}/{resource_id}"
        
        try:
            response = requests.delete(
                url,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code in [200, 204]:
                return {"success": True}
            elif response.status_code == 404:
                return {"success": False, "error": "not found"}
            elif response.status_code == 409:
                return {"success": False, "error": "can't delete - dependencies exist"}
            else:
                return {"success": False, "error": f"status {response.status_code}"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}


# usage
client = CRUDClient("https://api.example.com", "api_key_123")

# create
result = client.create("menu", {"name": "pizza", "price": 12})
if result["success"]:
    item_id = result["data"]["id"]

# read
result = client.read("menu", item_id)

# update
result = client.update("menu", item_id, {"name": "pizza", "price": 14})

# delete
result = client.delete("menu", item_id)
```

---

## key concepts

### concept 1: put replaces entire resource

**important distinction:**
- put sends complete object
- even if only one field changed
- server replaces entire resource

**example:**
```python
# original item
{
    "id": 1,
    "name": "pizza",
    "price": 12,
    "description": "delicious",
    "available": True
}

# want to change only price
# still must send everything
{
    "id": 1,
    "name": "pizza",
    "price": 14,  # only this changed
    "description": "delicious",
    "available": True
}
```

**why this matters:**
- if you only send {"price": 14}, other fields might be lost
- always send complete object with put

---

### concept 2: delete is permanent

**no undo button:**
- delete removes resource completely
- can't recover without backup
- must recreate from scratch if needed

**safe deletion pattern:**
```python
# option 1: soft delete (preferred)
# don't actually delete, just mark inactive
item["deleted"] = True
item["deleted_at"] = "2026-02-22"
requests.put(url, json=item)

# option 2: archive before delete
archive_response = requests.post(archive_url, json=item)
if archive_response.status_code == 200:
    requests.delete(url)
```

---

### concept 3: crud is universal

**every modern api follows crud:**
- stripe (payments)
- sendgrid (emails)
- google sheets (spreadsheets)
- github (repos)
- twitter (posts)
- slack (messages)

**same pattern everywhere:**
- create → post
- read → get
- update → put
- delete → delete

---

### concept 4: idempotency

**idempotent = safe to repeat**

**idempotent methods:**
- get - reading multiple times = same result
- put - updating multiple times = same result
- delete - deleting multiple times = same result (404 after first)

**not idempotent:**
- post - creating multiple times = multiple resources

**why this matters:**
```python
# if network fails after sending, is it safe to retry?

# post - NO (creates duplicates)
requests.post(url, json=order)  # created order #1
# network error, retry
requests.post(url, json=order)  # created order #2 (duplicate!)

# put - YES (same result)
requests.put(url, json=updated_item)  # updated to price 14
# network error, retry
requests.put(url, json=updated_item)  # still price 14 (safe)
```

---

## troubleshooting guide

### problem: 404 on put request
**cause:** resource doesn't exist  
**fix:** use post to create first, then put to update

```python
# wrong - trying to update non-existent resource
response = requests.put(f"{url}/999", json=data)  # 404

# correct - create first
response = requests.post(url, json=data)
item_id = response.json()["id"]

# then update
response = requests.put(f"{url}/{item_id}", json=updated_data)  # 200
```

---

### problem: 409 conflict on update
**cause:** resource was modified by someone else  
**fix:** get latest version, apply changes, retry

```python
# get latest version
response = requests.get(f"{url}/{item_id}")
current = response.json()

# apply your changes to latest version
current["price"] = 14.00

# update with latest version
response = requests.put(f"{url}/{item_id}", json=current)
```

---

### problem: delete returns 409
**cause:** other resources depend on this one  
**fix:** delete dependencies first, or use cascade delete

```python
# can't delete menu item (active orders reference it)
response = requests.delete(f"{url}/menu/5")  # 409

# option 1: delete dependencies first
requests.delete(f"{url}/orders/101")
requests.delete(f"{url}/orders/102")
requests.delete(f"{url}/menu/5")  # now works

# option 2: cascade delete (if api supports)
requests.delete(f"{url}/menu/5?cascade=true")
```

---

### problem: lost data after put
**cause:** didn't send complete object  
**fix:** always send all fields

```python
# wrong - only sending price
response = requests.put(url, json={"price": 14})
# result: name, description, etc deleted!

# correct - send everything
complete_item = {
    "id": 1,
    "name": "pizza",
    "description": "delicious",
    "price": 14,  # only this changed
    "category": "pizza",
    "available": True
}
response = requests.put(url, json=complete_item)
```

---

## practice exercises

### exercise 1: implement soft delete

```python
def soft_delete(item_id):
    """
    mark item as deleted instead of removing it.
    allows recovery.
    """
    # get current item
    response = requests.get(f"{url}/{item_id}")
    item = response.json()
    
    # mark as deleted
    item["deleted"] = True
    item["deleted_at"] = "2026-02-22"
    
    # update (not delete)
    response = requests.put(f"{url}/{item_id}", json=item)
    
    return response.status_code == 200


# later: restore item
def restore(item_id):
    response = requests.get(f"{url}/{item_id}")
    item = response.json()
    
    item["deleted"] = False
    item["deleted_at"] = None
    
    response = requests.put(f"{url}/{item_id}", json=item)
    return response.status_code == 200
```

---

### exercise 2: batch updates

```python
def batch_update_prices(item_ids, price_increase):
    """
    update multiple items at once.
    """
    results = []
    
    for item_id in item_ids:
        # get current item
        response = requests.get(f"{url}/{item_id}")
        
        if response.status_code == 200:
            item = response.json()
            
            # increase price
            item["price"] += price_increase
            
            # update
            update_response = requests.put(
                f"{url}/{item_id}",
                json=item
            )
            
            results.append({
                "id": item_id,
                "success": update_response.status_code == 200
            })
    
    return results


# usage: increase all pizza prices by €1
pizza_ids = [1, 2, 3, 4, 5]
results = batch_update_prices(pizza_ids, 1.00)
```

---

### exercise 3: versioned updates

```python
def versioned_update(item_id, changes):
    """
    prevent overwriting concurrent changes.
    """
    # get current version
    response = requests.get(f"{url}/{item_id}")
    item = response.json()
    current_version = item.get("version", 0)
    
    # apply changes
    item.update(changes)
    
    # increment version
    item["version"] = current_version + 1
    
    # update with version check
    response = requests.put(
        f"{url}/{item_id}",
        json=item,
        headers={"If-Match": str(current_version)}
    )
    
    if response.status_code == 409:
        print("conflict - item was updated by someone else")
        return False
    
    return response.status_code == 200
```

---

## code templates

### template 1: complete crud class

```python
class ResourceManager:
    """manage any resource via crud operations."""
    
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    def create(self, data):
        """create new resource"""
        response = requests.post(
            self.base_url,
            headers=self.headers,
            json=data,
            timeout=10
        )
        return self._handle_response(response)
    
    def read(self, resource_id=None):
        """read resource(s)"""
        url = self.base_url
        if resource_id:
            url = f"{url}/{resource_id}"
        
        response = requests.get(
            url,
            headers=self.headers,
            timeout=10
        )
        return self._handle_response(response)
    
    def update(self, resource_id, data):
        """update resource"""
        response = requests.put(
            f"{self.base_url}/{resource_id}",
            headers=self.headers,
            json=data,
            timeout=10
        )
        return self._handle_response(response)
    
    def delete(self, resource_id):
        """delete resource"""
        response = requests.delete(
            f"{self.base_url}/{resource_id}",
            headers=self.headers,
            timeout=10
        )
        return self._handle_response(response)
    
    def _handle_response(self, response):
        """standard response handling"""
        if response.status_code in [200, 201, 204]:
            try:
                return {"success": True, "data": response.json()}
            except:
                return {"success": True}
        else:
            return {"success": False, "status": response.status_code}
```

---

### template 2: safe deletion

```python
def safe_delete(url, resource_id, archive_url=None):
    """
    delete with optional archival.
    """
    # archive before delete (if specified)
    if archive_url:
        # get resource
        response = requests.get(f"{url}/{resource_id}")
        
        if response.status_code == 200:
            resource = response.json()
            
            # archive
            requests.post(archive_url, json=resource)
    
    # delete
    response = requests.delete(f"{url}/{resource_id}")
    
    return response.status_code in [200, 204]
```

---

### template 3: conditional update

```python
def conditional_update(url, resource_id, condition_fn, updates):
    """
    only update if condition is met.
    """
    # get current state
    response = requests.get(f"{url}/{resource_id}")
    
    if response.status_code == 200:
        resource = response.json()
        
        # check condition
        if condition_fn(resource):
            # apply updates
            resource.update(updates)
            
            # save
            response = requests.put(
                f"{url}/{resource_id}",
                json=resource
            )
            
            return response.status_code == 200
    
    return False


# usage
def is_available(item):
    return item.get("available", False)

# only update if item is available
conditional_update(
    url="/menu",
    resource_id=5,
    condition_fn=is_available,
    updates={"price": 15.00}
)
```

---

## day 25 preview: rate limiting & retry logic

**tomorrow you'll learn:**
- understand api rate limits
- implement retry logic with backoff
- handle 429 too many requests
- queue requests properly
- build resilient api clients

**by end of day 25:**
- professional error handling
- production-ready api integration
- handle failures gracefully

---

## achievements

- [x] understand put requests (updating data)
- [x] understand delete requests (removing data)
- [x] complete crud operations mastery
- [x] know when to use each http method
- [x] manage complete resource lifecycles
- [x] build professional crud clients

**day 24 complete: 5/5 skills mastered ✓**

---

## file organization

**your day 24 structure:**
```
ai-operations-training/
├── day-24/
│   ├── day24_crud_operations.py (all examples)
│   └── day-24-notes.md (this file)
└── previous days...
```

---

## the simple summary

### **day 24 in three sentences:**

1. **put updates existing resources (send complete object)**
2. **delete removes resources permanently (be careful)**
3. **get + post + put + delete = complete crud (full api control)**

### **the decision framework:**
```
new resource? → POST
view resource? → GET
change resource? → PUT
remove resource? → DELETE
```

**every api follows this pattern**

---

## honest self-assessment

**what you should understand (day 24):**
- [x] put updates existing resources
- [x] delete removes resources
- [x] complete crud operations
- [x] when to use each method
- [x] url structure for updates/deletes
- [x] put sends complete object

**what you don't understand yet (coming soon):**
- patch vs put (day 25)
- rate limiting (day 25)
- async requests (day 26)
- webhooks (week 5)
- optimistic locking (week 6)

---

## grade for day 24: a

**what went well:**
- all code working ✓
- understand all four http methods ✓
- built complete crud class ✓
- correct decision framework ✓
- applied to realistic scenarios ✓
- fixed indentation error independently ✓

**what to work on:**
- start thinking about error recovery strategies
- practice identifying which method to use
- consider edge cases (concurrent updates, dependencies)

---

**created:** day 24 of ai operations training  
**your progress:** week 4, day 3 (24/168 days total - 14.3%)  
**next session:** day 25 - rate limiting & retry logic

**you've mastered complete crud operations.**  
**tomorrow: professional error handling and resilience.**  
**by end of week 4: production-ready api integration.**
