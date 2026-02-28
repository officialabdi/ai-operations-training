# DAY 26: ASYNC REQUESTS & CONCURRENCY
## AI Operations Training - Week 4, Day 5

---

## what you learned today

### core skills:
- understand the difference between synchronous and asynchronous execution
- write async functions using `async def` and `await`
- use `asyncio.gather()` to run multiple tasks concurrently
- build a production batch processing system with real timing proof

### the architecture "why":
**days 22-25 taught you:** reliable API calls that don't crash  
**day 26 teaches you:** API calls that run fast enough for real client workloads

**the problem day 26 solves:**
```python
# days 22-25 (reliable but slow)
for customer in reservations:
    send_email(customer)   # waits 1.5s per email
# 200 emails = 300 seconds = 5 minutes

# day 26 (reliable AND fast)
await asyncio.gather(*tasks)   # all fire at once
# 200 emails = ~1.5 seconds
```

**real business impact:**
- without async: Luigi's Saturday batch takes 5 minutes, may time out on cloud
- with async: same batch takes 2 seconds, runs reliably in production
- clients pay for systems that are fast, not just ones that work

---

## the key concept: synchronous vs asynchronous

### synchronous (blocking)
```python
# each line waits for the previous to finish
response1 = requests.get(url)   # wait 1.5s...
response2 = requests.get(url)   # only starts after response1 done
response3 = requests.get(url)   # only starts after response2 done
# total: 4.5 seconds
```

### asynchronous (non-blocking)
```python
# tasks start and yield control while waiting
response1 = await session.get(url)   # starts, then yields
response2 = await session.get(url)   # starts while response1 waits
response3 = await session.get(url)   # starts while others wait
# total: ~1.5 seconds (the length of one call)
```

### why async works for api calls
API calls spend most of their time **waiting** for a response, not computing.
Your CPU is idle during that wait. Async lets Python do other work during those gaps.

**the waiter analogy:**
- bad waiter: takes table 1 order → goes to kitchen → waits → brings food → then goes to table 2
- good waiter: takes all orders → sends all to kitchen → delivers as food comes out
- same kitchen, much faster service

---

## the three keywords

| keyword | what it does |
|---------|-------------|
| `async def` | marks a function as async — it can pause and resume |
| `await` | pauses this function until the result is ready, yields control to other tasks |
| `asyncio.run()` | starts the async engine and runs your main function |

---

## critical distinction: await alone vs asyncio.gather()

### await alone = still sequential
```python
async def main():
    await greet("Luigi", 2)   # Luigi runs and FINISHES
    await greet("Maria", 1)   # only then Maria starts
# total: 3 seconds (2 + 1)
```

### asyncio.gather() = truly concurrent
```python
async def main():
    await asyncio.gather(
        greet("Luigi", 2),
        greet("Maria", 1)
    )
# total: 2 seconds (length of longest task)
```

**key point:** `async def` alone does NOT make things concurrent.
`asyncio.gather()` is what actually runs tasks simultaneously.

---

## step 1: your first async function

```python
import asyncio

async def greet(name, delay):
    print(f"Starting greeting for {name}")
    await asyncio.sleep(delay)   # simulates waiting for an API
    print(f"Hello, {name}!")

async def main():
    await asyncio.gather(
        greet("Luigi", 2),
        greet("Maria", 1)
    )

asyncio.run(main())
```

**output (concurrent):**
```
Starting greeting for Luigi
Starting greeting for Maria   ← both start before either finishes
Hello, Maria                  ← faster one finishes first (1s)
Hello, Luigi                  ← slower one finishes second (2s)

total: ~2 seconds (not 3)
```

---

## step 2: luigi's email batch system

```python
import asyncio
import time

async def send_confirmation_email(customer_name, reservation_time):
    """
    Simulates sending a confirmation email via API.
    In production this would call SendGrid or similar.
    """
    await asyncio.sleep(1.5)   # simulates API response time
    print(f"✅ Email sent to {customer_name} for {reservation_time}")
    return f"{customer_name}: confirmed"

async def process_batch(reservations):
    """
    Sends all confirmation emails concurrently.
    """
    tasks = []
    for customer, time_slot in reservations:
        task = send_confirmation_email(customer, time_slot)
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    return results

async def main():
    reservations = [
        ("Marco",   "Sat 7:00pm"),
        ("Sarah",   "Sat 7:30pm"),
        ("John",    "Sat 8:00pm"),
        ("Aoife",   "Sat 8:00pm"),
        ("Declan",  "Sat 8:30pm"),
        ("Fatima",  "Sat 9:00pm"),
    ]

    print(f"Processing {len(reservations)} reservations...\n")

    start = time.time()
    results = await process_batch(reservations)
    end = time.time()

    print(f"\n📊 Batch complete: {len(results)} emails sent in {end - start:.2f} seconds")
    print(f"Sequential would have taken: {len(reservations) * 1.5:.1f} seconds")

asyncio.run(main())
```

**your actual output:**
```
processing 6 reservations...

email sent to marco for sat 7:00pm
email sent to Sarah for Sat 7:30pm
email sent to John for Sat 8:00pm
email sent to Aoife for Sat 8:00pm
email sent to Declan for Sat 8:30pm
email sent to Fatima for Sat 9:00pm

batch complete: 6 emails sent in 1.51 seconds
Sequential would have taken: 9.0 seconds
```

**result: 6x speed improvement**

---

## the real numbers that matter to clients

| batch size | sequential | async | time saved |
|-----------|-----------|-------|-----------|
| 6 emails  | 9s        | 1.5s  | 7.5s      |
| 200 emails | 300s (5 min) | ~1.5s | 298.5s  |
| 500 SMS   | 400s      | ~0.8s | 399.2s    |

**why this matters for your freelance business:**
- bigger batches = bigger clients = higher fees
- cloud platforms time out after 30s — a 300s script fails in production
- async scripts don't time out because they finish in seconds
- you can charge more for a system that processes 10,000 rows vs 100

---

## the `asyncio.gather(*tasks)` pattern

```python
# build a list of tasks (coroutines, not yet running)
tasks = []
for customer, time_slot in reservations:
    task = send_confirmation_email(customer, time_slot)  # not running yet
    tasks.append(task)

# fire all tasks at the same time, wait for all to complete
results = await asyncio.gather(*tasks)
# the * unpacks the list into separate arguments
# results = list of return values in original order
```

**what `*tasks` means:**
```python
tasks = [task1, task2, task3]
asyncio.gather(*tasks)
# is the same as:
asyncio.gather(task1, task2, task3)
```

---

## bugs you hit today and what they taught you

### bug 1: wrong argument syntax
```python
# your mistake
await greet("luigi, 2")       # ❌ comma inside quotes = one string argument

# correct
await greet("Luigi", 2)       # ✅ comma outside quotes = two arguments
```

**lesson:** always count function parameters vs arguments passed

### bug 2: code runner using temp file
```
File "tempCodeRunnerFile.py"   # ← not your actual file
```

**lesson:** always run python files via terminal: `python day26_async.py`
code runner's play button creates a temp copy that may not have your latest changes

### bug 3: variables used before assignment
```python
start = time.time()
# missing: results = await process_batch(reservations)
# missing: end = time.time()
print(f"{len(results)} in {end - start:.2f}s")   # ❌ results and end not defined
```

**lesson:** if you use a variable in a print statement, trace back and make sure it was assigned above it

---

## what we didn't cover (intentional gap)

**`aiohttp`** — the library for real async HTTP requests

In production, `requests` library is **blocking** and doesn't work properly with async.
You'd use `aiohttp` instead for live API calls.

**why we skipped it today:**
- we used `asyncio.sleep()` to simulate API calls (no real network needed)
- `aiohttp` belongs with live API work in **Week 8** when you make real calls
- the mental model (async/gather) is the hard part — you have that now

---

## proof of work — questions you answered

**Q1: Why did all 6 emails print at almost the same moment?**
Each email was waiting (asyncio.sleep) not computing. While one waited, Python moved to the next task. Concurrency works here because the bottleneck is waiting, not CPU work.

**Q2: What is the difference between `await` alone and `asyncio.gather()`?**
`await` alone = sequential, one finishes then the next starts.
`asyncio.gather()` = concurrent, all start together simultaneously.

**Q3: 500 SMS at 0.8s each — sequential vs async?**
Sequential = 500 × 0.8 = 400 seconds.
Async = ~0.8 seconds (length of one call).
Freelancer value: faster = bigger clients, no cloud timeouts, justifies higher fees.

---

## achievements

- [x] understand sync vs async execution model
- [x] write `async def` and `await` correctly
- [x] use `asyncio.gather()` for true concurrency
- [x] build and run a batch email system with timing proof
- [x] debug 3 real errors independently

**day 26 complete: 4/4 skills mastered ✓**

---

## day 27 preview: the 1000-row prompt batch pipeline

**tomorrow you combine everything from week 4:**
- read a 1000-row CSV (days 22-23)
- make async calls for each row (day 26)
- handle rate limits and retries on failures (day 25)
- write results back to a new CSV

**by end of day 27:**
- a script that processes 1000 customer records
- generates an AI prompt for each one
- handles errors without crashing
- the kind of system you'd charge €2,000+ to build

---

## file organisation

**your day 26 structure:**
```
ai-operations-training/
├── day-26/
│   ├── day26_async.py       (all code from today)
│   └── day-26-notes.md      (this file)
└── previous days...
```

---

## the simple summary

### day 26 in three sentences:
1. **synchronous code waits for each task to finish before starting the next**
2. **async code starts a task, yields control while it waits, and runs other tasks in the gap**
3. **asyncio.gather() fires all tasks simultaneously — that's where the speed comes from**

### the pattern:
```python
async def main():
    tasks = [my_async_function(item) for item in my_list]
    results = await asyncio.gather(*tasks)
```

**this pattern processes any batch in the time of one single call**

---

## honest self-assessment

**what you understand (day 26):**
- [x] why async is faster than sync for API calls
- [x] difference between await alone vs asyncio.gather()
- [x] how to build a concurrent batch processor
- [x] that async works because api calls are I/O bound (waiting), not CPU bound

**what you don't understand yet (coming soon):**
- aiohttp for real async HTTP requests (week 8)
- async with databases (month 5)
- async frameworks like FastAPI (month 5)

---

## grade for day 26: b+

**what went well:**
- core concept understood ✓
- all 3 bugs debugged and fixed ✓
- proof of work completed ✓
- real timing output verified ✓

**what to work on:**
- answer explanation questions with more technical precision
- name the specific mechanic, not just the general idea

---

**created:** day 26 of ai operations training  
**your progress:** week 4, day 5 (26/190 days total - 13.7%)  
**next session:** day 27 - the 1000-row prompt batch pipeline

**you can now build systems that process batches in seconds, not minutes.**  
**tomorrow: the full week 4 pipeline comes together.**
