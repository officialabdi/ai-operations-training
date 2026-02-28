import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
def divide_numbers(a, b):
    logging.debug(f"divide_numbers called with a={a}, b={b}")
    if not isinstance(a, (int, float)) or not isinstance (b, (int, float)):
        logging.error(f"invalid input types: a={type(a)}, b={type,(b)}")
        return None
    if b == 0:
        logging.warning("attempted division by zero")
        return None
    result = a / b
    logging.info(f"successfully divided {a} by {b} = {result}")
    return result


# ========================================
# REAL-WORLD EXAMPLE: Email System Logging
# ========================================

def process_customer_email(customer_tier, customer_email_type, tokens_used):
    logging.info(f"starting email proccessing: tier={customer_tier}, type={customer_email_type}")
    valid_tiers = ["vip", "standard"]
    if customer_tier not in valid_tiers:
        logging.error(f"invalid customer tier: '{customer_tier}' (expected {valid_tiers})")
        return None
    if not isinstance(customer_email_type, str):
        logging.error(f"email type must be string, got {type(customer_email_type)}")
        return None
    if isinstance(tokens_used, str):
        if not tokens_used.isdigit():
            logging.error(f"invalid token count: '{tokens_used}' (must be numeric)")
            return None
        tokens_used = int(tokens_used)
        logging.debug(f"Converted string tokens to int: {tokens_used}")
    
    # Calculate cost
    cost = (tokens_used / 1000) * 0.003
    logging.info(f"Email processed successfully: {customer_tier} {customer_email_type}, cost=${cost:.4f}")
    
    return {
        "tier": customer_tier,
        "type": customer_email_type,
        "tokens": tokens_used,
        "cost": cost
    }
# ========================================
# PRODUCTION LOGGING EXAMPLE
# ========================================

def production_email_system(customer_tier, email_type, tokens_used):
    """
    Production version - only logs important events.
    
    REAL-WORLD USE: Luigi's live system (not testing)
    TASK: Track successes and errors, skip debug details
    VALUE: Clean logs for production monitoring
    """
    # In production, we might only want INFO and above
    # (skip DEBUG messages to keep logs clean)
    
    logging.info(f"Email request: {customer_tier} - {email_type}")
    
    try:
        # Validate
        if customer_tier not in ["vip", "standard"]:
            raise ValueError(f"Invalid tier: {customer_tier}")
        
        if isinstance(tokens_used, str):
            tokens_used = int(tokens_used)
        
        # Process
        cost = (tokens_used / 1000) * 0.003
        
        # Success - log for audit trail
        logging.info(f" Email sent: {email_type}, cost=${cost:.4f}")
        return cost
        
    except ValueError as e:
        # Business logic error - log as ERROR
        logging.error(f" Validation failed: {e}")
        return None
    except Exception as e:
        # Unexpected error - log as CRITICAL
        logging.critical(f" System error: {e}")
        return None


# final example: complete logging system
def track_daily_operations():
    """
    demonstrates all log levels in one function.
    
    real-world use: end-of-day summary for luigi
    task: review what happened during business hours
    value: audit trail and performance tracking
    """
    logging.debug("starting daily operations review")
    
    # simulate processing emails
    emails_sent = 45
    emails_failed = 3
    total_revenue = 125.50
    
    logging.info(f"daily summary: {emails_sent} emails sent")
    
    if emails_failed > 0:
        logging.warning(f"{emails_failed} emails failed - review needed")
    
    if total_revenue < 100:
        logging.error("revenue below target - check pricing")
    else:
        logging.info(f"revenue target met: ${total_revenue}")
    
    logging.debug("daily operations review complete")

print("\n=== daily operations summary ===")
track_daily_operations()