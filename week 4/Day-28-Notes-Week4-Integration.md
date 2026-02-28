# DAY 28: WEEK 4 INTEGRATION PROJECT
## AI Operations Training - Week 4, Day 7 (Final)

---

## what you learned today

### core skills:
- set up professional logging that writes to both terminal and a permanent log file
- structure a production script with a CONFIG block and __name__ guard
- produce a clean summary report that you can show a client

### the architecture "why":
**days 22-27 taught you:** how to build a pipeline that works  
**day 28 teaches you:** how to build a pipeline that looks and behaves professionally

**the difference that matters:**
- a script that works = €500 freelance job
- a script that works + logs everything + has clean config + summary report = €3,000 freelance job
- the logic is identical. the professionalism around it is what justifies the price.

---

## concept 1: logging vs print statements

### the problem with print()
```python
print("Processing customer...")   # visible in terminal
# close terminal → gone forever
# run at 3am → no one watching
# client asks "what failed?" → no record
```

### the solution: logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log"),   # writes to file permanently
        logging.StreamHandler()                # also prints to terminal
    ]
)

logger = logging.getLogger(__name__)
```

**FileHandler** = writes every log message to `pipeline.log` permanently.
you can open it tomorrow, send it to a client, check what happened at 3am.

**StreamHandler** = prints the same messages to terminal so you see them live.

using both means you watch it live AND have a permanent record.

### when to use logging
- any script that runs automatically (scheduled, cloud, overnight)
- any script that processes more than ~20 rows
- any script you deliver to a client
- any script where failures need to be investigated later

### when print() is fine
- quick testing while building
- one-off scripts you run yourself and watch live
- day 1-27 style learning exercises

---

## concept 2: log levels

```python
logger.info("Pipeline started")              # normal event — everything fine
logger.warning("Recovered after 2 attempts") # something needed attention but recovered
logger.error("Failed permanently: Fatima")   # something failed and didn't recover
```

| level | when to use | example |
|-------|-------------|---------|
| INFO | normal operations | "Loaded 1000 customers" |
| WARNING | recovered issues | "Retried and succeeded" |
| ERROR | permanent failures | "Failed after 3 attempts" |

**why levels matter:**
when a client asks "what failed last night?" you search the log for ERROR only.
one line, instant answer, without reading thousands of INFO lines.

---

## concept 3: CONFIG dictionary

### without config (bad)
```python
async def process_customer(customer, semaphore):
    for attempt in range(3):          # hardcoded
        await asyncio.sleep(0.1)      # hardcoded
        if random.random() < 0.1:    # hardcoded
```

client says "increase retries to 5" → hunt through 200 lines → risk missing one

### with config (professional)
```python
CONFIG = {
    "input_file":  r"c:\full\path\to\customers.csv",
    "output_file": r"c:\full\path\to\results.csv",
    "max_retries":  3,
    "concurrency":  10,
    "api_delay":    0.1,
    "failure_rate": 0.1
}

# used throughout the code
for attempt in range(CONFIG['max_retries']):
    await asyncio.sleep(CONFIG['api_delay'])
```

client says "increase retries to 5" → change one number at the top → done

**rule:** any value that might change goes in CONFIG. never hardcode settings inside functions.

---

## concept 4: if __name__ == "__main__"

### what it does
when Python runs a file directly, it sets `__name__ = "__main__"`
when another file imports your file, it sets `__name__ = "the_filename"`

```python
# without the guard — dangerous
customers = read_customers(...)   # runs immediately when anyone imports this file

# with the guard — professional
if __name__ == "__main__":
    customers = read_customers(...)   # only runs when YOU run this file directly
```

### why it matters
in Month 3 and 4 you'll build systems where one file imports functions from another.
without this guard, importing your pipeline would immediately start processing 1000 customers.
that's a serious bug.

### the rule
```python
# outside the guard — reusable functions
def read_customers(): ...
def generate_prompt(): ...
async def process_customer(): ...

# inside the guard — code that actually runs the program
if __name__ == "__main__":
    customers = read_customers(...)
    results = asyncio.run(run_pipeline(customers))
```

functions and classes go outside. the run block goes inside. always.

---

## concept 5: full path vs relative path

```python
# relative path — fragile
"customers.csv"
# python looks in whatever folder the terminal is currently in
# breaks if terminal is in wrong folder

# full path — reliable
r"c:\Users\abdi0\OneDrive\ai road 2026\day 28\customers.csv"
# always works regardless of where terminal is
# r"..." = raw string, backslashes don't cause issues
```

**rule:** for client systems, always use full paths or config-driven paths.
relative paths break in production when scripts run automatically from different locations.

---

## concept 6: summary report

```python
def print_summary(results, elapsed):
    successful = [r for r in results if r['status'] == 'success']
    failed     = [r for r in results if r['status'] == 'failed']
    retried    = [r for r in results if r['attempts'] > 1]

    logger.info("-" * 50)
    logger.info("PIPELINE SUMMARY")
    logger.info("-" * 50)
    logger.info(f"Total processed : {len(results)}")
    logger.info(f"Successful      : {len(successful)}")
    logger.info(f"Failed          : {len(failed)}")
    logger.info(f"Retried         : {len(retried)}")
    logger.info(f"Time elapsed    : {elapsed:.2f} seconds")
    logger.info(f"Success rate    : {len(successful)/len(results)*100:.1f}%")
    logger.info("-" * 50)

    if failed:
        logger.warning("Failed customers:")
        for r in failed:
            logger.warning(f"  - {r['name']} (ID: {r['customer_id']})")
```

**why every pipeline needs a summary:**
- proves to a client the system ran successfully
- gives them the numbers they care about (success rate, time)
- lists every failure by name so they can act on it
- logged permanently so you can reference it later

---

## your actual output today

```
Total processed : 1000
Successful      : 999
Failed          : 1
Retried         : 102
Time elapsed    : 26.74 seconds
Success rate    : 99.9%
```

---

## what the log file gives you

when a client says "last night's pipeline had failures — which customers?"

you do NOT re-run anything.
you open `pipeline.log` and search for ERROR:

```
2026-02-25 21:20:53,985 | ERROR | Failed permanently: Fatima Al-Hassan | API timeout
```

name, timestamp, reason — all there permanently.
that's why professionals use logging, not print statements.

---

## the complete file structure

```
day-28/
├── day28_pipeline.py     ← production script
├── customers.csv         ← input data
├── results.csv           ← output: all 1000 prompts with status
└── pipeline.log          ← permanent record of every event
```

four files. a client gets all four. that's a deliverable.

---

## week 4 complete — what you can now build

| skill | days | status |
|-------|------|--------|
| Read/write CSV files | 22-23 | ✅ |
| HTTP methods GET/POST/PUT/DELETE | 24 | ✅ |
| Rate limiting & retry with backoff | 25 | ✅ |
| Async concurrency with gather | 26 | ✅ |
| 1000-row batch pipeline | 27 | ✅ |
| Production logging & config | 28 | ✅ |

you can now build a system that:
- reads any CSV from a client
- processes every row with personalised AI prompts
- handles failures automatically with retry
- runs 1000 rows in ~25 seconds
- logs everything permanently
- produces a clean results file and summary

that is a billable product.

---

## bugs you hit today and what they taught you

### bug 1: FileNotFoundError
python looks for files in the terminal's current folder, not the script's folder.
fix: use full paths in CONFIG or always cd into project folder first.

### bug 2: key mismatch (max_tries vs max_retries)
CONFIG had `max_tries` but code referenced `max_retries` — KeyError.
fix: CONFIG keys must match exactly what you reference in the code.
lesson: put all settings in CONFIG first, then reference them — never the other way around.

### bug 3: UnicodeEncodeError on ─ character
windows terminal couldn't display the unicode dash character.
fix: use regular hyphen `-` instead of `─` for dividers.
lesson: stick to standard ASCII characters in terminal output for cross-platform compatibility.

---

## proof of work — answers

**q1: difference between pipeline.log and terminal output?**
content is identical. terminal disappears when you close VS Code.
log file is permanent — available tomorrow, sendable to clients, searchable for errors.

**q2: why use if __name__ == "__main__":?**
separates reusable functions from the run block.
when Month 3 files import your functions, the pipeline won't accidentally start running.
functions outside, run block inside — always.

**q3: client asks which customers failed — how do you find out?**
open pipeline.log, search for ERROR.
every permanent failure was logged with the customer name, ID, and reason.
no need to re-run anything.

---

## achievements

- [x] set up professional logging to file and terminal
- [x] use log levels correctly (info, warning, error)
- [x] structure script with CONFIG block
- [x] use if __name__ == "__main__": correctly
- [x] use full paths to prevent FileNotFoundError
- [x] produce a client-ready summary report
- [x] deliver a complete 4-file project folder

**day 28 complete — week 4 complete ✓**

---

## week 5 preview: git, pandas & sql foundations

**next week you learn the professional data toolkit:**
- day 29: git — version control, GitHub, commit history as portfolio
- day 30-31: pandas — the industry standard for data manipulation
- day 32-33: SQL — querying databases like a professional
- day 34: combining CSV + SQL + Pandas into one data stack
- day 35: push everything to GitHub — your first public portfolio piece

**why this matters for your agency:**
every real client project involves messy data in databases, not clean CSVs.
pandas and SQL are how you handle it.
git is how you prove you built it.

---

## file organisation

```
ai-operations-training/
├── day-28/
│   ├── day28_pipeline.py    (production pipeline)
│   ├── customers.csv        (input)
│   ├── results.csv          (output)
│   ├── pipeline.log         (permanent log)
│   └── day-28-notes.md      (this file)
└── previous days...
```

---

## the simple summary

### day 28 in three sentences:
1. **logging replaces print statements in production — it writes permanently to a file so you can investigate failures without being present**
2. **CONFIG puts all settings in one place at the top so changes take one line, not a hunt through 200 lines of code**
3. **if __name__ == "__main__": separates reusable functions from the run block so other files can safely import your code**

---

## grade for day 28: b

**what went well:**
- pipeline ran successfully ✓
- logging working correctly ✓
- all concepts understood after explanation ✓
- good instinct to question what wasn't explained ✓

**what to work on:**
- run files via terminal from day 1 — stop using code runner entirely
- when you see a new concept in code, ask what it does before running
- answer proof of work questions with specific technical detail

---

**created:** day 28 of ai operations training
**your progress:** week 4 complete (28/190 days - 14.7%)
**next session:** day 29 - git fundamentals

**week 4 is done. you built a production pipeline from scratch.**
**next week: the professional data toolkit that every real project needs.**
