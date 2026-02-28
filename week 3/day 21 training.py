import logging

class reservationerror(Exception):
    pass
class invalidnameerror(reservationerror):
    pass
class invalidemailerror(reservationerror):
    pass
class invalidphoneerror(reservationerror):
    pass
class invaliddateerror(reservationerror):
    pass
class invalidpasrtysizeerror(reservationerror):
    pass

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('luigis_reservation.log'),
        logging.StreamHandler()
        
    ] 
)

def validate_name(name):
    if not name or len(name) < 2:
        raise invalidnameerror(f"name must be at least 2 characters. got: '{name}'")
    return name.strip()
def validate_email(email):
    if "@" not in email:
        raise invalidemailerror(f"email must contain @. got: '{email}'")
    parts = email.split("@")
    if len(parts) != 2:
        raise invalidemailerror(f"email must have exactly one @. got: '{email}'")
    username, domain = parts
    if len(username) == 0 or len(domain) == 0:
        raise invalidemailerror(f"email must have usernmae and domain. got: '{email}'")
    return email.strip().lower()
def validate_phone(phone):
    cleaned = phone.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
    if not cleaned.isdigit():
        raise invalidphoneerror(f"phone must be only digits. got: '{phone}'")
    if len(cleaned) != 10:
        raise invalidphoneerror(f"phone must be 10 digits. got: '{phone}'")
    return cleaned
def validate_date(date):
    if not date or len(date) == 0:
        raise invaliddateerror(f"date cannot be empty. got: '{date}'")
    if len(date) != 10 or date[4] != "-" or date[7] != "-":
        raise invaliddateerror(f"date must be in format YYYY-MM-DD. got: '{date}'")
    return date
def validate_party_size(party_size):
    try:
        size = int(party_size)
    except ValueError:
        raise invalidpasrtysizeerror(f"party size must be a number. got: '{party_size}'")
    if size < 1:
        raise invalidpasrtysizeerror(f"party size must be at least 1. got: '{party_size}'")
    if size > 20:
        raise invalidpasrtysizeerror(f"party size cannot exceed 20. got: '{party_size}'")
    return size

def process_reservation(name, email, phone, date, party_size):
    try:
        
        validated_name = validate_name(name)
        validated_email = validate_email(email)
        validated_phone = validate_phone(phone)
        validated_date = validate_date(date)
        validated_party_size = validate_party_size(party_size)
        
       
        logging.info(f"reservation successful: {validated_name}, {validated_email}, {validated_phone}, {validated_date}, party of {validated_party_size}")
        return f"reservation confirmed for {validated_name} on {validated_date} for {validated_party_size}"
    except reservationerror as e:
        logging.error(f"reservation failed for {name}: {str(e)}")
        return f"reservation error: {str(e)}"
    except Exception as e:
        logging.critical(f"unexpected error processing reservation for {name}: {str(e)}")
        return "system errror: please contact luigi's directly at 555-1234"
    
    # ========================================
# test cases
# ========================================

print("=" * 60)
print("testing luigi's reservation system")
print("=" * 60)

# test 1: valid reservation
print("\ntest 1: valid reservation")
result = process_reservation("john smith", "john@email.com", "555-123-4567", "2026-03-15", "4")
print(result)

# test 2: invalid name
print("\ntest 2: invalid name (too short)")
result = process_reservation("j", "john@email.com", "555-123-4567", "2026-03-15", "4")
print(result)

# test 3: invalid email
print("\ntest 3: invalid email (no @)")
result = process_reservation("john smith", "johnemail.com", "555-123-4567", "2026-03-15", "4")
print(result)

# test 4: invalid phone
print("\ntest 4: invalid phone (wrong digits)")
result = process_reservation("john smith", "john@email.com", "555-123", "2026-03-15", "4")
print(result)

# test 5: invalid date
print("\ntest 5: invalid date (wrong format)")
result = process_reservation("john smith", "john@email.com", "555-123-4567", "15-03-2026", "4")
print(result)

# test 6: invalid party size
print("\ntest 6: invalid party size (too large)")
result = process_reservation("john smith", "john@email.com", "555-123-4567", "2026-03-15", "25")
print(result)

print("\n" + "=" * 60)
print("check luigis_reservations.log file for complete log")
print("=" * 60)
