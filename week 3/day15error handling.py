from datetime import date


def divide_numbers(a, b):
    result = a / b
    return result
answer1 = divide_numbers(10, 2)
print(f"10 / 2 = {answer1}")

answer2 = divide_numbers(10, 0)
print(f"10 / 0 = {answer2}")

def safe_divide(a , b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("Error: Cannot divide by zero")
        return None
answer3 = safe_divide(10, 0)
print(f"result: {answer3}")
answer4 = safe_divide(10, 2)
print(f"result: {answer4}")

def safe_calculate(a, b, operation):
    try:
        if operation == "divide":
            result = a / b
        elif operation == "add":
            result = a + b 
        else: 
            result = "unknown operation"
        return result
    except ZeroDivisionError:
        return "error: cannot divide by zero"
    except TypeError:
        return "error: invalid data type"
     

print(safe_calculate(10, 2, "divide"))


print(safe_calculate(10, 0, "divide"))


print(safe_calculate("ten", 2, "add"))


print(safe_calculate(10, 5, "add"))

def super_safe_function(data):
    try:
        result = int(data) * 2
        return result
    except ValueError:
        return "error: not a valid number"
    except TypeError:
        return "error: wrong data type"
    except:
        return "error: something unexpected happened" 
    
def divide_with_else(a, b):
    try:
        result = a / b 
    except ZeroDivisionError:
        print("error caught: division by zero")
        return None
    else: 
        print("succes! no errors occurred")
        return result
    
    

print(super_safe_function("10"))      
print(super_safe_function("abc"))     
print(super_safe_function(None))      


print(divide_with_else(10, 2))
print(divide_with_else(10, 0))

def open_and_process(filename):
    try:
        print("opening file...")
        result = 10 / 0
        print("processing result...")
        return result
    except ZeroDivisionError:
        print("error during processing")
        return None
    finally: 
        print("cleanup complete (finally always runs)")


print("=== Test with error ===")
result1 = open_and_process("test.txt")
print(f"Result: {result1}\n")


def open_and_process_success(filename):
    try:
        print("Opening file...")
        result = 10 / 2  
        print("Processing file...")
        return result
    except ZeroDivisionError:
        print("Error during processing")
        return None
    finally:
        print("Cleanup complete (finally always runs)")

print("=== Test without error ===")
result2 = open_and_process_success("test.txt")
print(f"Result: {result2}")

def safe_track_email_generation(customer_tier, email_type, tokens_used):
    """
    Tracks email generation with error handling.
    Handles bad input gracefully.
    """
    try:
        
        tokens = int(tokens_used)
        
       
        cost = (tokens / 1000) * 0.003
        
        log_entry = {
            "tier": customer_tier,
            "type": email_type,
            "tokens": tokens,
            "cost": cost
        }
        
        
        print(f"Logged: {customer_tier} {email_type} - ${cost:.4f}")
        return True
        
    except ValueError:
        print(f"Error: tokens_used must be a number, got '{tokens_used}'")
        return False
        
    except ZeroDivisionError:
        print("Error: Cannot calculate cost")
        return False
        
    except:
        print("Error: Something unexpected happened")
        return False
    
    
safe_track_email_generation("VIP", "complaint", 250)


safe_track_email_generation("standard", "support", "250 tokens")


safe_track_email_generation("VIP", "sales", 180)