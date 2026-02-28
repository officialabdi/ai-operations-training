def route_support_ticket(is_vip, issue_type, urgency):
    if is_vip:
        if issue_type == "billing":
            response = "vip billing team - 10 min response"
        elif issue_type == "technical":
            response = "vip technical team - 15 min response"
        elif issue_type == "account":
            response = "vip account team - 20 min response"
        else: 
            response = "vip general support - 30 min response"
    else:
        if issue_type == "billing":
            response = "standard billing - 2 hour response"
        elif issue_type == "technical":
            response = "standard technical - 4 hour response"
        elif issue_type == "account":
            response = "standard account - 6 hour response"
        else: 
            response = "general support - 24 hour response"
    return response
    
    
test1 = route_support_ticket(True, "billing", "high")
print(f"VIP + Billing: {test1}")


test2 = route_support_ticket(True, "technical", "low")
print(f"VIP + Technical: {test2}")


test3 = route_support_ticket(False, "billing", "high")
print(f"Regular + Billing: {test3}")


test4 = route_support_ticket(False, "shipping", "low")
print(f"Regular + Shipping: {test4}")               

def route_order(is_dining, food_type):

    if is_dining:
        if food_type == "pizza":
            return "dine-in pizza station - priority" 
        elif food_type == "pasta":
            return "dine-in pasta station - priority"
        elif food_type == "salad":
            return "dine-in salad station - priority"
        else:
            return "dine-in general station - priority"
    else: 
        if food_type == "pizza":
            return "takeout pizza station - standard"
        elif food_type == "pasta":
            return "takeout pasta station - standard"
        elif food_type == "salad":
            return "takeout salad station - standard"
        else: 
            return "takeout general station - standard"
        return route_order
test1 = route_order(True, "pizza")    
print(route_order(True, "pizza"))
test2 = route_order(True, "pasta")    
print(route_order(True, "pasta"))
test3 = route_order(False, "salad") 
print(route_order(False, "salad"))
test4 = route_order(False, "burger") 
print(route_order(False, "burger"))   
        
