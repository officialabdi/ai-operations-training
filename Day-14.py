def route_email_request(customer_tier , email_type , urgency):
    if customer_tier == "VIP":
        return "vip complaint team - immediate response"
    elif customer_tier == "VIP" and email_type == "support" and urgency == "high":
        return "vip support team - 15 min response"
    elif customer_tier == "VIP" and email_type == "sales" and urgency == "high":
            return "vip sales team - priority follow-up"
    elif customer_tier == "VIP":
        return "vip general team - same day response"
    else:
        if email_type == "complaint":
            return "standard complaint team - 2 hour response"
        elif email_type == "support":
            return "standard support team - 4 hour response"
        elif email_type == "sales":
            return "standard sales team - 24 hour response"
        else:
            return "standard general team - 48 hour response"
def generate_email_prompt(customer_tier , email_type , urgency,customer_name, issue):
    routing = route_email_request(customer_tier, email_type,urgency)       
    if urgency == "high":
        urgency_text = "urgent - respond immediately"
    else:#
        urgency_text = "standard priority"
    prompt = f"""generate an {email_type} email for {customer_name}.
        customer tier: {customer_tier}
        routing: {routing}
        priority: {urgency_text}
        issue: {issue}
        write a professional response addressing their concern."""
    return prompt
email_log = []
def track_email_generation(customer_tier, email_type, tokens_used):
    cost_per_1k_tokens = 0.003
    calculated_cost = (tokens_used / 1000) * cost_per_1k_tokens
    log_entry = {
        "tier": customer_tier,
        "type": email_type,
        "tokens": tokens_used,
        "cost": calculated_cost
    }
    email_log.append(log_entry) # type: ignore
def generate_monthly_report():
    total_cost = 0
    total_emails = len(email_log) # type: ignore

    vip_count = 0
    standard_count = 0
    for entry in email_log: # type: ignore
        total_cost += entry["cost"]
        if entry["tier"] == "VIP":
            vip_count += 1
        else:
            standard_count += 1
    print("\n=== MONTHLY EMAIL AUTOMATION REPORT ===")
    print(f"Total Emails Generated: {total_emails}")
    print(f"VIP Emails: {vip_count}")
    print(f"Standard Emails: {standard_count}")
    print(f"Total Cost: ${total_cost:.4f}")
    print(f"Average Cost per Email: ${total_cost/total_emails:.4f}")
    print("=" * 40)


print("Test 1: VIP Complaint")
routing1 = route_email_request("VIP", "complaint", "high")
print(f"Routing: {routing1}")

prompt1 = generate_email_prompt("VIP", "complaint", "high", "Sarah Johnson", "Product arrived damaged")
print(prompt1)

track_email_generation("VIP", "complaint", 250)
print("-" * 40)


print("\nTest 2: Standard Support")
routing2 = route_email_request("standard", "support", "low")
print(f"Routing: {routing2}")

prompt2 = generate_email_prompt("standard", "support", "low", "John Smith", "How do I reset my password?")
print(prompt2)

track_email_generation("standard", "support", 180)
print("-" * 40)


print("\nTest 3: VIP Sales")
prompt3 = generate_email_prompt("VIP", "sales", "high", "Lisa Chen", "Interested in enterprise plan")
print(prompt3)

track_email_generation("VIP", "sales", 200)
print("-" * 40)


print("\nTest 4: Standard Complaint")
prompt4 = generate_email_prompt("standard", "complaint", "high", "Mike Brown", "Billing error on invoice")
print(prompt4)

track_email_generation("standard", "complaint", 220)
print("-" * 40)


print("\n")
generate_monthly_report()

