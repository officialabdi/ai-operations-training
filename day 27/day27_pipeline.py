import csv
def read_customers(filepath):
    customers = []
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            customers.append(row)

    return customers    

def generate_prompt(customer):
    name = customer['name']
    customer_type = customer['customer_type'].strip()
    visit_count = customer['visit_count']
    last_visit = customer['last_visit']

    if customer_type == 'VIP':
        prompt= (
            f"Write a warm, exclusive message to {name}, a VIP customer "
            f"who has visited {visit_count} times. Last visit: {last_visit}. "
            f"Thank them for their loyalty and offer a complimentary dessert "
            f"on their next visit. Keep it personal and under 50 words."
        )
    elif customer_type == 'new':
        prompt = (
            f"Write a welcoming message to {name}, a first-time customer "
            f"who visited on {last_visit}. "
            f"Invite them back and offer 10% off their next booking. "
            f"Keep it friendly and under 50 words."
        )
    elif customer_type == 'no_show':
        prompt = (
            f"Write a polite re-engagement message to {name}, who missed "
            f"their reservation on {last_visit}. "
            f"No guilt — just invite them to rebook easily. "
            f"Keep it brief and under 40 words."
        )
    else:  # regular
        prompt = (
            f"Write a friendly check-in message to {name}, a regular customer "
            f"with {visit_count} visits. Last visit: {last_visit}. "
            f"Let them know about Luigi's new weekend menu. "
            f"Keep it casual and under 50 words."
        ) 
    return prompt 

import asyncio
import time

import random
async def simulate_api_call(prompt):
    await asyncio.sleep(0.1)
    if random.random() < 0.1:
        raise Exception("api timeout - rate limited")
    return f"ai_response-for {prompt[:40]}..."

async def process_customer(customer, semaphore):
    """
    Processes one customer with retry logic on failure.
    """
    async with semaphore:
        name = customer['name'].strip()
        customer_type = customer['customer_type'].strip()
        prompt = generate_prompt(customer)

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = await simulate_api_call(prompt)
                return {
                    'customer_id': customer['customer_id'].strip(),
                    'name': name,
                    'customer_type': customer_type,
                    'prompt': prompt,
                    'status': 'success',
                    'attempts': attempt + 1
                }
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    await asyncio.sleep(wait_time)
                else:
                    return {
                        'customer_id': customer['customer_id'].strip(),
                        'name': name,
                        'customer_type': customer_type,
                        'prompt': prompt,
                        'status': 'failed',
                        'attempts': max_retries
                    }
                
    
async def run_pipeline(customers):
    semaphore = asyncio.Semaphore(10)
    tasks = [process_customer(c, semaphore) for c in customers ]
    results = await asyncio.gather(*tasks)
    return results

def write_results(results, output_filepath):
    fieldnames = ['customer_id', 'name', 'customer_type', 'prompt', 'status', 'attempts']
    with open(output_filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"💾 Results saved to {output_filepath}")
                  
# --- run it ---
customers = read_customers("customers.csv")

# simulate 1000 rows by repeating our 10 customers 100 times
customers_1000 = customers * 100
# fix customer IDs so they're unique
for i, c in enumerate(customers_1000):
    c = dict(c)
    c['customer_id'] = str(i + 1)
    customers_1000[i] = c

print(f"Total customers to process: {len(customers_1000)}\n")

start = time.time()
results = asyncio.run(run_pipeline(customers_1000))
end = time.time()

# summary
successful = [r for r in results if r['status'] == 'success']
failed = [r for r in results if r['status'] == 'failed']
retried = [r for r in results if r['attempts'] > 1]

print(f"✅ Successful: {len(successful)}")
print(f"❌ Failed:     {len(failed)}")
print(f"🔁 Retried:    {len(retried)}")
print(f"⏱  Time:       {end - start:.2f} seconds")
print(f"📊 Sequential would have taken: {len(customers_1000) * 0.1:.0f} seconds")

write_results(results, "results.csv")