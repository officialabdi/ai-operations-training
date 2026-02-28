# Day 31 Notes — Pandas Applied

---

## Missing Values

Every real dataset has gaps. In Pandas, missing values appear as NaN. Three operations for dealing with them:

`isnull()` returns a True/False grid showing exactly where gaps exist.

`isnull().sum()` counts the number of nulls per column, giving you a quick damage report. This is the first thing you run on any new client dataset.

`fillna("value")` replaces nulls with a value you choose — but does not change the original DataFrame unless you reassign it back to the column.

When to fill vs drop: fill when the rest of the row is valuable and you can use a sensible default. Drop when a missing value makes the entire row useless.

---

## Groupby

Groupby splits a DataFrame into groups based on a column, then runs a calculation on each group separately.

Structure: `DataFrame.groupby("column")["column_to_calculate"].calculation()`

Calculations used today:
- `.sum()` — totals the values per group
- `.count()` — counts how many rows are in each group
- `.mean()` — gives the average value per group

Business use: turn raw transaction data into per-customer or per-category summaries for client reporting.

---

## Merge

Merge combines two DataFrames by matching rows that share a common value in a specified column.

Structure: `pd.merge(left_df, right_df, on="shared_column")`

Default behaviour: only keeps rows where the shared column value exists in both DataFrames. Rows that appear in only one table are dropped.

Business use: connect orders to customer details, connect products to pricing tables, connect any two datasets that share a common identifier.

---

## The Reporting Pattern

Merge first to bring all relevant data into one DataFrame, then groupby to summarise it. This two-step pattern covers the majority of client reporting work.

---

## Code Reference — Day 31

```python
import pandas as pd

orders = pd.DataFrame({
    "order_id": [1, 2, 3, 4, 5, 6],
    "customer": ["Maria", "Luigi", "Maria", "Tom", "Luigi", "Maria"],
    "item": ["Margherita", "Pepperoni", "Calzone", "Margherita", "Calzone", "Pepperoni"],
    "price": [12.0, 15.0, 13.0, 12.0, 13.0, 15.0],
    "status": ["delivered", "delivered", "cancelled", "delivered", None, "delivered"]
})

customers = pd.DataFrame({
    "customer": ["Maria", "Luigi", "Tom", "Sara"],
    "loyalty_tier": ["Gold", "Silver", "Bronze", "Gold"],
    "email": ["maria@email.com", "luigi@email.com", "tom@email.com", "sara@email.com"]
})

# Missing values
print(orders.isnull())
print(orders.isnull().sum())
print(orders.fillna("unknown"))

# Groupby
print(orders.groupby("customer")["price"].sum())
print(orders.groupby("customer")["price"].count())
print(orders.groupby("customer")["price"].mean())

# Merge
merged = pd.merge(orders, customers, on="customer")
print(merged)
print(merged.groupby("loyalty_tier")["price"].sum())
```

---

*Day 31 of 190 — Week 5: Pandas & SQL*
