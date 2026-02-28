def build_priority_email(recipient_role, urgency, topic):
    if recipient_role == "ceo" and urgency == "high":
        tone = "urgent and executive-level"
    elif recipient_role == "ceo" and urgency == "low":
        tone = "formal and data driven"
    elif recipient_role == "colleague" and urgency == "high":
        tone = "quick and collaborative"
    elif recipient_role == "colleague" and urgency == "low":
        tone = "friendly and casual"
    else:
        tone = "professional"
    prompt = f"write a {tone} email to a {recipient_role} about {topic}."
    return prompt

def check_support_priority(customer_tier, years_active):
    if customer_tier == "premium" or years_active >= 5:
        priority = "vip"
    else:
        priority = "standard support"
    return priority


    result1 = build_priority_email("ceo", "high", "server outage")
    print(result1)
    result2 = build_priority_email("ceo", "low", "quarterly planning")
    print(result2)
    result3 = build_priority_email("colleague", "high", "deadline today")
    print(result3)
    result4 = build_priority_email("colleague", "low", "lunch tomorrow")
    print(result4)
    result5 = build_priority_email("customer", "high", "order issue")
    print(result5)

   
    test1 = check_support_priority("premium", 2)
    print(f"premium + 2 years: {test1}")
    test2 = check_support_priority("standard", 7)
    print(f"standard + 7 years: {test2}")
    test3 = check_support_priority("premium", 8)
    print(f"Premium + 8 years: {test3}")
    test4 = check_support_priority("standard", 3)
    print(f"Standard + 3 years: {test4}:")

def check_content_urgency(content_type, word_count):
    if content_type == "tweet" or word_count <50:
        return "quick post" 
    elif content_type == "blog" and word_count >= 1000:
        return "long-form article" 
    elif content_type == "email" and word_count <200:
        return "brief message"
    else:
        return "standard content"
    
print(check_content_urgency("tweet", 25))       
print(check_content_urgency("social", 30))        
print(check_content_urgency("blog", 1500))       
print(check_content_urgency("email", 150))       
print(check_content_urgency("report", 500))