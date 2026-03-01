import csv
import asyncio
import time
import random
import logging
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

CONFIG = {
    "input_file":  r"c:\Users\abdi0\OneDrive\ai road 2026\day 28\customers.csv",
    "output_file": r"c:\Users\abdi0\OneDrive\ai road 2026\day 28\results.csv",
    "max_retries":  3,
    "concurrency":  10,
    "api_delay":    0.1,
    "failure_rate": 0.1
}

# ── READ CSV ──────────────────────────────────────────────────────────────────
def read_customers(filepath):
    customers = []
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            customers.append(row)
    logger.info(f"Loaded {len(customers)} customers from {filepath}")
    return customers


# ── GENERATE PROMPT ───────────────────────────────────────────────────────────
def generate_prompt(customer):
    name          = customer['name'].strip()
    customer_type = customer['customer_type'].strip()
    visit_count   = customer['visit_count'].strip()
    last_visit    = customer['last_visit'].strip()

    if customer_type == 'VIP':
        return (
            f"Write a warm, exclusive message to {name}, a VIP customer "
            f"who has visited {visit_count} times. Last visit: {last_visit}. "
            f"Thank them for their loyalty and offer a complimentary dessert. "
            f"Keep it personal and under 50 words."
        )
    elif customer_type == 'new':
        return (
            f"Write a welcoming message to {name}, a first-time customer "
            f"who visited on {last_visit}. "
            f"Invite them back and offer 10% off their next booking. "
            f"Keep it friendly and under 50 words."
        )
    elif customer_type == 'no_show':
        return (
            f"Write a polite re-engagement message to {name}, who missed "
            f"their reservation on {last_visit}. "
            f"No guilt — just invite them to rebook easily. "
            f"Keep it brief and under 40 words."
        )
    else:
        return (
            f"Write a friendly check-in message to {name}, a regular customer "
            f"with {visit_count} visits. Last visit: {last_visit}. "
            f"Let them know about Luigi's new weekend menu. "
            f"Keep it casual and under 50 words."
        )


# ── SIMULATE API CALL ─────────────────────────────────────────────────────────
async def simulate_api_call(prompt):
    await asyncio.sleep(CONFIG['api_delay'])
    if random.random() < CONFIG['failure_rate']:
        raise Exception("API timeout - rate limited")
    return f"AI_RESPONSE: {prompt[:40]}..."


# ── PROCESS ONE CUSTOMER ──────────────────────────────────────────────────────
async def process_customer(customer, semaphore):
    async with semaphore:
        name          = customer['name'].strip()
        customer_type = customer['customer_type'].strip()
        prompt        = generate_prompt(customer)

        for attempt in range(CONFIG['max_retries']):
            try:
                response = await simulate_api_call(prompt)
                if attempt > 0:
                    logger.warning(f"Recovered after {attempt + 1} attempts: {name}")
                return {
                    'customer_id':   customer['customer_id'].strip(),
                    'name':          name,
                    'customer_type': customer_type,
                    'prompt':        prompt,
                    'status':        'success',
                    'attempts':      attempt + 1
                }
            except Exception as e:
                if attempt < CONFIG['max_retries'] - 1:
                    wait_time = 2 ** attempt
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"Failed permanently: {name} | {e}")
                    return {
                        'customer_id':   customer['customer_id'].strip(),
                        'name':          name,
                        'customer_type': customer_type,
                        'prompt':        prompt,
                        'status':        'failed',
                        'attempts':      CONFIG['max_retries']
                    }


# ── RUN PIPELINE ──────────────────────────────────────────────────────────────
async def run_pipeline(customers):
    semaphore = asyncio.Semaphore(CONFIG['concurrency'])
    tasks     = [process_customer(c, semaphore) for c in customers]
    results   = await asyncio.gather(*tasks)
    return results


# ── WRITE RESULTS ─────────────────────────────────────────────────────────────
def write_results(results, filepath):
    fieldnames = ['customer_id', 'name', 'customer_type',
                  'prompt', 'status', 'attempts']
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    logger.info(f"Results saved to {filepath}")


# ── SUMMARY REPORT ────────────────────────────────────────────────────────────
def print_summary(results, elapsed):
    successful = [r for r in results if r['status'] == 'success']
    failed     = [r for r in results if r['status'] == 'failed']
    retried    = [r for r in results if r['attempts'] > 1]

    logger.info("-" * 50)
    logger.info("PIPELINE SUMMARY")
    logger.info("─" * 50)
    logger.info(f"Total processed : {len(results)}")
    logger.info(f"Successful       : {len(successful)}")
    logger.info(f"Failed           : {len(failed)}")
    logger.info(f"Retried          : {len(retried)}")
    logger.info(f"Time elapsed     : {elapsed:.2f} seconds")
    logger.info(f"Success rate     : {len(successful)/len(results)*100:.1f}%")
    logger.info("─" * 50)

    if failed:
        logger.warning("Failed customers:")
        for r in failed:
            logger.warning(f"  - {r['name']} (ID: {r['customer_id']})")

            # ── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    logger.info("Pipeline started")
    logger.info(f"Config: {CONFIG}")

    # load customers
    customers = read_customers(CONFIG["input_file"])

    # simulate 1000 rows
    customers_1000 = customers * 100
    for i, c in enumerate(customers_1000):
        c = dict(c)
        c['customer_id'] = str(i + 1)
        customers_1000[i] = c

    # run pipeline
    start   = time.time()
    results = asyncio.run(run_pipeline(customers_1000))
    elapsed = time.time() - start

    # output
    write_results(results, CONFIG['output_file'])
    print_summary(results, elapsed)

    logger.info("Pipeline complete")
