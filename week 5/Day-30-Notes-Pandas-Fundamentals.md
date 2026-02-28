# DAY 30: PANDAS FUNDAMENTALS
## AI Operations Training - Week 5, Day 2

---

## what you learned today

### core skills:
- load a CSV into a DataFrame and inspect it professionally
- filter rows, select columns, and sort data using pandas syntax
- add new columns using .apply() and save enriched data back to CSV

### the architecture "why":
**day 27:** processed CSVs with Python's built-in csv module — manual loops, limited
**day 30:** pandas handles the same data in one line, works on 10 rows or 10 million

**the business reality:**
every client has data in spreadsheets or CSVs.
pandas is how professionals read, clean, transform, and analyse that data.
it's the industry standard used by data engineers, analysts, and AI developers worldwide.

---

## concept 1: what is a DataFrame?

a DataFrame is a table — rows and columns, exactly like a spreadsheet — but in Python memory where you can manipulate it instantly.

```
   customer_id              name  visit_count customer_type loyalty_tier
0            1       Marco Rossi           12           VIP         Gold
1            2      Sarah Murphy            1           new       Bronze
2            3        John Byrne            5       regular       Silver
3            4       Aoife Kelly            3       regular       Bronze
4            5      Declan Walsh            0       no_show         None
```

- every **column** is a **Series** — a single column of data
- the whole **table** is a **DataFrame** — multiple Series side by side
- the numbers on the left (0, 1, 2...) are the **index** — row numbers added automatically

---

## concept 2: loading and inspecting data

```python
import pandas as pd

# load csv into dataframe — one line replaces entire csv.DictReader block
df = pd.read_csv("customers.csv")

# inspect it
df.shape              # (rows, columns) → (10, 6)
df.columns.tolist()   # list of column names
df.head()             # first 5 rows
df.dtypes             # data type of each column
df.describe()         # basic stats: count, mean, min, max etc.
```

### what df.describe() tells you
```
       customer_id  visit_count
count     10.00000    10.000000   ← how many rows
mean       5.50000     5.100000   ← average
std        3.02765     5.216427   ← how spread out the data is
min        1.00000     0.000000   ← lowest value
max       10.00000    15.000000   ← highest value
```

pandas only describes numeric columns automatically.
this is actionable — you can see avg visits, identify outliers, spot no-shows instantly.

---

## concept 3: selecting columns

```python
# single column → single brackets → returns a Series
df['name']

# multiple columns → double brackets (outer = select, inner = list) → returns DataFrame
df[['name', 'customer_type', 'visit_count']]
```

### why double brackets for multiple columns?
```python
df['name']                          # passing a string
df[['name', 'visit_count']]         # passing a LIST inside the selection brackets
#  ↑ outer brackets = select from df
#    ↑ inner brackets = the list of columns you want
```

single column = single brackets.
multiple columns = double brackets containing a list.

---

## concept 4: filtering rows

put a condition inside brackets to filter:

```python
# only VIP customers
vip = df[df['customer_type'] == 'VIP']

# customers with 5 or more visits
loyal = df[df['visit_count'] >= 5]

# no shows only
no_shows = df[df['customer_type'] == 'no_show']
```

### how filtering works
```python
df['customer_type'] == 'VIP'
# returns: [True, False, False, False, False, True, False, False, False, True]
# pandas keeps only the rows where True
```

you can combine conditions:
```python
# VIP customers with 10+ visits
df[(df['customer_type'] == 'VIP') & (df['visit_count'] >= 10)]
```

---

## concept 5: sorting

```python
# sort by visit count, highest first
df.sort_values('visit_count', ascending=False)

# sort by visit count, lowest first
df.sort_values('visit_count', ascending=True)

# sort by name alphabetically
df.sort_values('name')
```

---

## concept 6: .apply()

runs a function on every row of a column automatically — replaces a loop.

```python
def assign_tier(visits):
    if visits >= 10:
        return 'Gold'
    elif visits >= 5:
        return 'Silver'
    elif visits >= 1:
        return 'Bronze'
    else:
        return 'None'

# without .apply() — manual loop
tiers = []
for visits in df['visit_count']:
    tiers.append(assign_tier(visits))
df['loyalty_tier'] = tiers

# with .apply() — one line
df['loyalty_tier'] = df['visit_count'].apply(assign_tier)
```

read it left to right:
- `df['visit_count']` — take the visit_count column
- `.apply(assign_tier)` — run assign_tier() on every value in that column

pandas calls `assign_tier(12)` → `'Gold'`, then `assign_tier(1)` → `'Bronze'`, and so on for all rows.
returns a new Series which you assign as a new column.

**rule:** any time you want to run a function on every row of a column — use .apply()

---

## concept 7: value_counts()

counts how many times each unique value appears in a column — instant segment breakdown.

```python
df['customer_type'].value_counts()
# customer_type
# VIP        3
# regular    3
# new        2
# no_show    2

df['loyalty_tier'].value_counts()
# loyalty_tier
# Bronze    3
# Silver    3
# Gold      2
# None      2
```

default sort: highest count first.
to change sort order:
```python
df['loyalty_tier'].value_counts().sort_index()          # alphabetical
df['loyalty_tier'].value_counts().sort_values()         # count ascending
```

you can chain pandas methods — each method returns a Series you can call the next method on.

---

## concept 8: saving back to csv

```python
df.to_csv("customers_enriched.csv", index=False)
# index=False → don't write the row numbers (0,1,2...) as a column
```

---

## the complete code

```python
import pandas as pd

# ── LOAD ──────────────────────────────────────────────────────────────────────
df = pd.read_csv(r"c:\Users\abdi0\OneDrive\ai road 2026\day 30\customers.csv")

# ── INSPECT ───────────────────────────────────────────────────────────────────
print("=== SHAPE ===")
print(df.shape)

print("\n=== COLUMNS ===")
print(df.columns.tolist())

print("\n=== FIRST 5 ROWS ===")
print(df.head())

print("\n=== DATA TYPES ===")
print(df.dtypes)

print("\n=== BASIC STATS ===")
print(df.describe())

# ── SELECT ────────────────────────────────────────────────────────────────────
print("\n=== SINGLE COLUMN ===")
print(df['name'])

print("\n=== MULTIPLE COLUMNS ===")
print(df[['name', 'customer_type', 'visit_count']])

# ── FILTER ────────────────────────────────────────────────────────────────────
print("\n=== VIP CUSTOMERS ONLY ===")
vip_customers = df[df['customer_type'] == 'VIP']
print(vip_customers[['name', 'visit_count']])

print("\n=== CUSTOMERS WITH 5+ VISITS ===")
loyal = df[df['visit_count'] >= 5]
print(loyal[['name', 'visit_count', 'customer_type']])

print("\n=== NO SHOWS ===")
no_shows = df[df['customer_type'] == 'no_show']
print(no_shows[['name', 'last_visit']])

# ── SORT ──────────────────────────────────────────────────────────────────────
print("\n=== SORTED BY VISIT COUNT (highest first) ===")
sorted_df = df.sort_values('visit_count', ascending=False)
print(sorted_df[['name', 'visit_count', 'customer_type']])

# ── ADD COLUMN ────────────────────────────────────────────────────────────────
def assign_tier(visits):
    if visits >= 10:
        return 'Gold'
    elif visits >= 5:
        return 'Silver'
    elif visits >= 1:
        return 'Bronze'
    else:
        return 'None'

df['loyalty_tier'] = df['visit_count'].apply(assign_tier)

print("\n=== ADD LOYALTY TIER COLUMN ===")
print(df[['name', 'visit_count', 'loyalty_tier']])

# ── BREAKDOWN ─────────────────────────────────────────────────────────────────
print("\n=== CUSTOMER TYPE BREAKDOWN ===")
print(df['customer_type'].value_counts())

print("\n=== LOYALTY TIER BREAKDOWN ===")
print(df['loyalty_tier'].value_counts())

# ── SAVE ──────────────────────────────────────────────────────────────────────
output_path = r"c:\Users\abdi0\OneDrive\ai road 2026\day 30\customers_enriched.csv"
df.to_csv(output_path, index=False)
print(f"\n✅ Saved enriched data to customers_enriched.csv")
```

---

## pandas vs csv module — the real difference

| task | csv module (day 27) | pandas (day 30) |
|------|--------------------|--------------------|
| load file | 5 lines | 1 line |
| filter rows | for loop + if statement | 1 line |
| sort data | manual sort logic | 1 line |
| add new column | loop + append | 1 line with .apply() |
| get breakdown | loop + counter dict | 1 line with value_counts() |
| save to csv | 5 lines | 1 line |
| handle 1M rows | very slow | fast |

use csv module for simple, small scripts.
use pandas for any real client data work.

---

## bugs you hit today

### bug 1: customers_type vs customer_type
```python
df[df['customers_type'] == 'VIP']   # ❌ extra 's'
df[df['customer_type'] == 'VIP']    # ✅ correct
```
KeyError tells you exactly which key it couldn't find — always read it.

### bug 2: 'vip' vs 'VIP'
```python
df[df['customer_type'] == 'vip']    # ❌ lowercase — no match
df[df['customer_type'] == 'VIP']    # ✅ must match data exactly
```
values inside quotes must match your data exactly including capitalisation.

---

## proof of work — answers

**q1: single vs double brackets?**
single brackets select one column and return a Series.
double brackets pass a list of columns and return a DataFrame.

**q2: client asks how many customers per region?**
`df['region'].value_counts()` — one line, instant breakdown.

**q3: why did loyalty tier sort Bronze first not Gold?**
value_counts() sorts by count (highest number) not by your custom logic.
Bronze appeared first because it had the highest count (3).

---

## achievements

- [x] installed pandas 3.0.1
- [x] loaded CSV into DataFrame and inspected professionally
- [x] selected single and multiple columns correctly
- [x] filtered rows by customer type, visit count, status
- [x] sorted data by column value
- [x] added loyalty_tier column using .apply()
- [x] used value_counts() for instant segment breakdown
- [x] saved enriched DataFrame back to CSV

**day 30 complete ✓**

---

## day 31 preview: pandas applied

**tomorrow: the more powerful pandas operations**
- groupby — segment your data and calculate stats per group
- merge — combine two DataFrames like a SQL JOIN
- real data manipulation on messy datasets
- building a full data analysis report for Luigi

---

## file organisation

```
ai-operations-training/
└── day-30/
    ├── day30_pandas.py          (today's code)
    ├── customers.csv            (input)
    ├── customers_enriched.csv   (output with loyalty_tier)
    └── day-30-notes.md          (this file)
```

---

## the simple summary

### day 30 in three sentences:
1. **a DataFrame is a table in Python memory — load any CSV in one line with pd.read_csv()**
2. **filter with df[condition], select columns with df[['col1','col2']], sort with .sort_values()**
3. **.apply() runs a function on every row without a loop — value_counts() gives instant breakdowns**

---

## grade for day 30: b+

**what went well:**
- all pandas operations working correctly ✓
- spotted and fixed typo bugs independently ✓
- clean output across all sections ✓
- correct answers to all proof of work questions ✓

**what to work on:**
- ask what a concept does before typing code — good instinct shown today, keep it up
- read error messages fully — KeyError always tells you exactly what went wrong

---

**created:** day 30 of ai operations training
**your progress:** week 5, day 2 (30/190 days - 15.8%)
**next session:** day 31 - pandas applied (groupby, merge, real data manipulation)

**you can now analyse any client dataset professionally.**
**tomorrow: the operations that turn raw data into business reports.**
