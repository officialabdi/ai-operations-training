# DAY 27: THE 1000-ROW PROMPT BATCH PIPELINE
## AI Operations Training - Week 4, Day 6

---

## what you learned today

### core skills:
- read a CSV file and process every row into a structured dictionary
- generate personalised AI prompts using conditional logic on real data
- combine async concurrency + rate limiting + retry logic into one production pipeline
- write processed results back to a new CSV with status tracking

### the architecture "why":
**weeks 1-3 taught you:** python fundamentals, prompt logic, error handling  
**week 4 days 22-26 taught you:** CSV processing, HTTP, rate limiting, async  
**day 27 teaches you:** how all of those skills combine into one complete system

**the problem day 27 solves:**
```
luigi has 1000 customers and wants a personalised AI message for each one.

manual approach:    1000 × 3 minutes = 50 hours of work
your pipeline:      25 seconds
```

**real business value:**
- this is a billable deliverable: €2,000–3,000 to build
- client provides CSV → you return CSV with AI prompts ready to send
- scales to any size: 100 rows or 100,000 rows, same code

---

## the complete pipeline architecture

```
customers.csv (input)
      ↓
read_customers()        ← day 22-23: CSV reading
      ↓
generate_prompt()       ← day 8-13: f-strings + conditional logic
      ↓
simulate_api_call()     ← day 26: async + day 25: retry logic
      ↓
asyncio.Semaphore(10)   ← rate limiting: max 10 concurrent requests
      ↓
results.csv (output)    ← day 23: CSV writing with status tracking
```

every skill from week 4 in one system.

---

## the complete code

```python
import csv
import asyncio
import time
import random


# ── STEP 1: READ CSV ──────────────────────────────────────────────────────────

def read_customers(filepath):
    """
    Reads customers from CSV and returns a list of dictionaries.
    Each row becomes a dict: {"customer_id": "1", "name": "Marco", ...}
    """
    customers = []

    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            customers.append(row)

    return customers


# ── STEP 2: GENERATE PROMPTS ─────────────────────────────────────────────────

def generate_prompt(customer):
    """
    Generates a personalised AI prompt based on customer type.
    Returns a prompt string ready to send to an AI API.
    """
    name = customer['name'].strip()
    customer_type = customer['customer_type'].strip()   # .strip() always on CSV values
    visit_count = customer['visit_count'].strip()
    last_visit = customer['last_visit'].strip()

    if customer_type == 'VIP':
        prompt = (
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


# ── STEP 3: SIMULATE API CALL ────────────────────────────────────────────────

async def simulate_api_call(prompt):
    """
    Simulates a real API call with occasional failures.
    In week 8, replace this with your actual OpenAI/Claude API call.
    """
    await asyncio.sleep(0.1)

    # simulate 10% failure rate (real APIs fail sometimes)
    if random.random() < 0.1:
        raise Exception("API timeout - rate limited")

    return f"AI_RESPONSE_FOR: {prompt[:40]}..."


# ── STEP 4: PROCESS ONE CUSTOMER WITH RETRY ──────────────────────────────────

async def process_customer(customer, semaphore):
    """
    Processes one customer with retry logic on failure.
    Semaphore limits concurrent requests to prevent rate limiting.
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
                    wait_time = 2 ** attempt   # exponential backoff: 1s, 2s, 4s
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


# ── STEP 5: RUN FULL BATCH ───────────────────────────────────────────────────

async def run_pipeline(customers):
    """
    Processes all customers concurrently with a rate limit of 10 at a time.
    """
    semaphore = asyncio.Semaphore(10)   # max 10 concurrent requests

    tasks = [process_customer(c, semaphore) for c in customers]
    results = await asyncio.gather(*tasks)
    return results


# ── STEP 6: WRITE RESULTS ────────────────────────────────────────────────────

def write_results(results, output_filepath):
    """
    Writes processed results to a new CSV file.
    """
    fieldnames = ['customer_id', 'name', 'customer_type', 'prompt', 'status', 'attempts']

    with open(output_filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"💾 Results saved to {output_filepath}")


# ── RUN IT ───────────────────────────────────────────────────────────────────

customers = read_customers("customers.csv")

# simulate 1000 rows by repeating 10 customers 100 times
customers_1000 = customers * 100
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
failed     = [r for r in results if r['status'] == 'failed']
retried    = [r for r in results if r['attempts'] > 1]

print(f"✅ Successful: {len(successful)}")
print(f"❌ Failed:     {len(failed)}")
print(f"🔁 Retried:    {len(retried)}")
print(f"⏱  Time:       {end - start:.2f} seconds")
print(f"📊 Sequential would have taken: {len(customers_1000) * 0.1:.0f} seconds")

write_results(results, "results.csv")
```

---

## your actual output

```
Total customers to process: 1000

✅ Successful: 998
❌ Failed:     2
🔁 Retried:    87
⏱  Time:       25.66 seconds
📊 Sequential would have taken: 100 seconds
💾 Results saved to results.csv
```

---

## what those numbers mean

| metric | value | what it proves |
|--------|-------|---------------|
| 998 successful | 99.8% success rate | retry logic recovered most failures |
| 2 failed | 0.2% permanent failure | correct — some failures are unrecoverable |
| 87 retried | day 25 working inside day 27 | exponential backoff saved 87 customers |
| 25 seconds | async working | semaphore + gather processing in parallel |
| 100s sequential | 4x slower | async delivers real business value |

**the 2 failures are not a bug.** they are correct behaviour.
a production system logs them as `status: failed` in the CSV instead of crashing.
in a real client system you would extract failed rows and re-run them separately.

---

## key concepts explained

### why .strip() on every csv value
```python
# csv may contain hidden whitespace
customer_type = customer['customer_type']        # reads "VIP " (space after)
customer_type == 'VIP'                           # False — comparison fails

customer_type = customer['customer_type'].strip() # reads "VIP" (clean)
customer_type == 'VIP'                           # True — works correctly
```

**rule:** always `.strip()` values read from CSV, APIs, user input, or databases.
never `.strip()` values you wrote yourself inside your code.

### what asyncio.Semaphore does
```python
semaphore = asyncio.Semaphore(10)  # only 10 tasks run at the same time

async with semaphore:   # wait here if 10 already running
    await api_call()    # do the work
                        # release — next task enters
```

without semaphore: all 1000 requests fire simultaneously → 429 rate limit error → API key banned

with semaphore: max 10 at a time → stays within API limits → all 1000 processed safely

### what *tasks means (unpacking)
```python
tasks = [task1, task2, task3]

# these are identical:
asyncio.gather(*tasks)
asyncio.gather(task1, task2, task3)

# * unpacks the list into separate arguments
# use it whenever a function expects individual arguments but you have a list
```

### retry with exponential backoff inside async
```python
for attempt in range(max_retries):
    try:
        response = await simulate_api_call(prompt)
        return result   # success — exit immediately
    except Exception:
        if attempt < max_retries - 1:
            wait_time = 2 ** attempt   # 1s, 2s, 4s
            await asyncio.sleep(wait_time)
        else:
            return failed_result   # permanent failure after 3 attempts
```

day 25 (retry) + day 26 (async) working together in one function.

---

## bugs you hit today and what they taught you

### bug 1: wrong prompt for all customers
```
Marco Rossi (VIP) → got "regular" message   ❌
```
**cause:** hidden whitespace in CSV. python read `"VIP "` not `"VIP"`.
`"VIP " == "VIP"` is False → fell through to else (regular).
**fix:** `.strip()` on all CSV values before any comparison.

### bug 2: missing `customer` before dictionary access
```python
customer_type = ['customer_type'].strip()    # ❌ list, not dict lookup
customer_type = customer['customer_type'].strip()  # ✅ correct
```
**lesson:** always count your variable names. `customer['key']` not `['key']`.

### bug 3: FileNotFoundError
```
FileNotFoundError: No such file or directory: 'customers.csv'
```
**cause:** terminal was in wrong folder. python looks for files in current directory.
**fix:** always `cd` into your project folder before running a script.
```
cd "c:\Users\abdi0\OneDrive\ai road 2026\day 27"
python day27_pipeline.py
```

---

## week 4 skills — complete picture

| day | skill | used today |
|-----|-------|-----------|
| 22-23 | CSV read/write | ✅ read_customers() + write_results() |
| 24 | HTTP methods | ✅ simulate_api_call() (real call in week 8) |
| 25 | retry + backoff | ✅ 3-attempt retry in process_customer() |
| 26 | async + gather | ✅ asyncio.gather() + semaphore |
| 27 | full pipeline | ✅ all of the above in one system |

---

## what happens in week 8

```python
# today (simulation)
async def simulate_api_call(prompt):
    await asyncio.sleep(0.1)
    return f"AI_RESPONSE_FOR: {prompt[:40]}..."

# week 8 (real api - one line changes)
async def call_openai_api(prompt):
    response = await openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

the entire pipeline stays identical. you swap one function.
1000 real AI responses in ~1.5 seconds instead of 1500 seconds sequential.

---

## proof of work — answers

**q1: root cause of wrong prompts?**
hidden whitespace in CSV values. `"VIP "` does not equal `"VIP"`.
`.strip()` removes the whitespace so the comparison works.

**q2: what happens to the 2 failed customers?**
in production: extract rows where `status == failed` from results.csv
and re-run the pipeline on just those rows. never ask the client to find them manually.

**q3: real api timing at 1.5s per call?**
sequential: 1000 × 1.5s = 1500 seconds (25 minutes)
async: ~1.5 seconds (time of one call, all run simultaneously)
async is 1000x faster at this scale.

---

## achievements

- [x] read and process a CSV into dictionaries
- [x] generate 4 different prompt types using conditional logic
- [x] build async batch processor with semaphore rate limiting
- [x] integrate retry + exponential backoff inside async
- [x] write full results to CSV with status tracking
- [x] process 1000 rows with 99.8% success rate

**day 27 complete: 5/5 skills mastered ✓**

---

## day 28 preview: week 4 integration project

**tomorrow: the full week 4 system comes together as one polished deliverable**
- clean up and structure today's pipeline professionally
- add proper logging (day 19 skills)
- add a summary report
- push to github
- this is your first portfolio piece

---

## file organisation

```
ai-operations-training/
├── day-27/
│   ├── day27_pipeline.py    (complete pipeline)
│   ├── customers.csv        (input data)
│   ├── results.csv          (output - generated prompts)
│   └── day-27-notes.md      (this file)
└── previous days...
```

---

## the simple summary

### day 27 in three sentences:
1. **read customer data from csv, apply conditional logic to generate personalised prompts**
2. **process all rows concurrently with asyncio.gather() limited by a semaphore**
3. **retry failures with exponential backoff and write all results to a new csv**

### the reusable pattern:
```python
# read → process → write
customers = read_csv("input.csv")
results   = asyncio.run(run_pipeline(customers))
write_csv(results, "output.csv")
```

this pattern works for any batch processing job you will ever build.

---

## grade for day 27: b+

**what went well:**
- full pipeline built and working ✓
- all 3 bugs debugged ✓
- 1000 rows processed successfully ✓
- retry logic integrated correctly ✓

**what to work on:**
- answer technical questions with more precision
- name the specific cause of bugs, not just the fix

---

**created:** day 27 of ai operations training
**your progress:** week 4, day 6 (27/190 days total - 14.2%)
**next session:** day 28 - week 4 integration project

**you just built a system that processes 1000 customers in 25 seconds.**
**a freelancer charges €2,000–3,000 for exactly this.**
**tomorrow: polish it into a portfolio piece.**
