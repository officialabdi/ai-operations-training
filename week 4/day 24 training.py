import requests
import json

print("=" * 60)
print("put requests - updating existing data")
print("=" * 60)

def update_menu_item(item_id, updated_data):
    url = f"https://httpbin.org/put"
    print(f"\nupdating item {item_id}")
    print("updating data:")
    print(json.dumps(updated_data, indent=2))

    try:
        response = requests.put(url, json=updated_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"\nitem updated successfully")
            print(f"server received: {result['json']}")
            return True
        else:
            print(f"update failed: status {response.status_code}")
            return False
        
    except requests.exceptions.timeout:
        print("update timeout")
        return False
    except Exception as e:
        print(f"error: {e}")
        return True
    
print("\ntest 1: update pizza price")
menu_item = {
    "id": 1,
    "name": "margherita pizza",
    "description": "tomato, mozzarella, basil",
    "price": 14.00,  # updated from 12.00
    "category": "pizza",
    "available": True
}

update_menu_item(item_id=1, updated_data=menu_item)

print("=" * 60)
print("put requests - updating existing data")
print("=" * 60)

def delete_menu_item(item_id):
    url = f"https://httpbin.org/delete"
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
    except requests.exceptions.timeout:
        print("delete timeout")
        return False
    except Exception as e:
        print(f"error: {e}")
        return False

print("\ntest 1: delete sold-out pizza")
delete_menu_item(item_id=5)

# test: delete already deleted item
print("\ntest 2: try to delete non-existent item")
# note: httpbin will return 200 for all deletes
# real apis return 404 for non-existent items
delete_menu_item(item_id=999)

print("\n" + "=" * 60)
print("complete crud - managing menu items")
print("=" * 60)

import requests
import json

class menuAPI:

    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.headers = {
            "authorization": f"bearer {api_key}",
            "content-type": "application/json"
        }
    def create_item(self, item_data):
        url = f"{self.base_url}/post"
        print(f"\n[create] adding new item: {item_data['name']}")
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=item_data,
                timeout=10
            )

            if response.status_code == 200:
               print(f"created: {item_data['name']}")
               return True
            else:
                print(f"failed: status {response.status_code}")
                return False
        except Exception as e:
            print(f"error: {e}")
            return False

    def read_item(self, item_id):
        url = f"{self.base_url}/get"
        print(f"\n[read] fetching item {item_id}")
        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
               print(f"retrieved item data")
               return response.json()
            else:
                print(f"failed: status {response.status_code}")
                return None
        except Exception as e:
            print(f"error: {e}")
            return None
        
    def update_item(self, item_id, updated_data):
        url = f"{self.base_url}/put"
        print(f"\n[update] updating item {item_id}: {updated_data['name']}")
        print(f"   new price: £{updated_data['price']}")

        try:
            response = requests.put(
                url,
                headers=self.headers,
                json=updated_data,
                timeout=10
            )
            if response.status_code == 200:
                print(f"updated: {updated_data['name']}")
                return True
            else:
                print(f"failed: status {response.status_code}")
                return False
        except Exception as e:
            print("error: {e}")
            return False

    def delete_item(self, item_id, item_name):
        url = f"{self.base_url}/delete"
        print(f"\n[delete] removing item {item_id}: {item_name}")

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
print("\ndemonstrating complete crud workflow:")
print("luigi manages his menu throughout the day")

# initialize api
api = menuAPI(
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

print("\n" + "=" * 60)
print("crud workflow complete")
print("=" * 60)

# ========================================
# example 4: crud decision guide
# ========================================

print("\n" + "=" * 60)
print("crud decision guide - when to use each method")
print("=" * 60)

def demonstrate_crud_decisions():
    """
    show when to use each http method.
    """
    
    print("\nscenario 1: customer orders new pizza")
    print("action: create new order")
    print("method: POST")
    print("why: creating new resource that didn't exist")
    
    print("\n" + "-" * 60)
    
    print("\nscenario 2: check order status")
    print("action: retrieve order details")
    print("method: GET")
    print("why: reading existing data, not changing anything")
    
    print("\n" + "-" * 60)
    
    print("\nscenario 3: customer changes delivery address")
    print("action: update order with new address")
    print("method: PUT")
    print("why: updating existing resource")
    
    print("\n" + "-" * 60)
    
    print("\nscenario 4: customer cancels order")
    print("action: remove order from system")
    print("method: DELETE")
    print("why: deleting resource completely")
    
    print("\n" + "-" * 60)
    
    print("\nscenario 5: luigi updates menu prices for inflation")
    print("action: update all pizza prices +€1")
    print("method: PUT (for each item)")
    print("why: updating existing resources")
    
    print("\n" + "-" * 60)
    
    print("\nscenario 6: view today's reservations")
    print("action: get list of reservations")
    print("method: GET")
    print("why: reading data only")


demonstrate_crud_decisions()

print("\n" + "=" * 60)
print("crud summary")
print("=" * 60)
print("""
create (post):   "add this new thing"
read (get):      "show me this thing"
update (put):    "change this existing thing"
delete (delete): "remove this thing"

every api you use follows this pattern.
""")

# ========================================
# example 5: realistic business workflow
# ========================================

print("\n" + "=" * 60)
print("realistic workflow: luigi's daily operations")
print("=" * 60)

def luigis_daily_workflow():
    """
    complete day in luigi's life using all crud operations.
    """
    
    print("\n8:00 AM - opening preparation")
    print("-" * 40)
    
    # create today's special
    print("\n[POST] create today's special")
    special = {
        "id": 99,
        "name": "sunday special - quattro formaggi",
        "price": 16.00,
        "available": True
    }
    print(f"✓ added: {special['name']} at €{special['price']}")
    
    # check current menu
    print("\n[GET] verify menu is complete")
    print("✓ retrieved 15 menu items")
    
    print("\n" + "=" * 60)
    print("\n12:00 PM - lunch rush")
    print("-" * 40)
    
    # high demand - increase price
    print("\n[PUT] update special price (high demand)")
    special['price'] = 18.00
    print(f"✓ updated price: €{special['price']}")
    
    # customer checks menu
    print("\n[GET] customer views menu")
    print(f"✓ shows special at €{special['price']}")
    
    # customer orders
    print("\n[POST] customer creates order")
    order = {
        "id": 501,
        "items": ["sunday special"],
        "total": 18.00,
        "status": "preparing"
    }
    print(f"✓ order #{order['id']} created")
    
    print("\n" + "=" * 60)
    print("\n3:00 PM - slow period")
    print("-" * 40)
    
    # reduce price to attract customers
    print("\n[PUT] update special price (slow period)")
    special['price'] = 15.00
    print(f"✓ reduced price: €{special['price']}")
    
    print("\n" + "=" * 60)
    print("\n8:00 PM - closing time")
    print("-" * 40)
    
    # sold out
    print("\n[PUT] mark special as unavailable")
    special['available'] = False
    print(f"✓ {special['name']} marked unavailable")
    
    print("\n" + "=" * 60)
    print("\n10:00 PM - end of day cleanup")
    print("-" * 40)
    
    # remove today's special
    print("\n[DELETE] remove today's special from menu")
    print(f"✓ deleted: {special['name']}")
    
    # check tomorrow's prep
    print("\n[GET] review menu for tomorrow")
    print("✓ menu ready for monday")
    
    print("\n" + "=" * 60)
    print("day complete - all operations successful")
    print("=" * 60)


luigis_daily_workflow()

print("\n\nwhat you learned today:")
print("=" * 60)
print("""
1. PUT updates existing resources (change price, description)
2. DELETE removes resources (discontinue items)
3. GET + POST + PUT + DELETE = complete control
4. each method has specific purpose
5. real businesses use all four methods daily

you can now manage any api resource completely.
""")