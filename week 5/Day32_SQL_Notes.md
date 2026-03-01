# Day 32 — SQL Basics
**AI Operations Mastery · Week 5 · Pandas & SQL**

---

## What is SQL

SQL (Structured Query Language) is the language used to talk to a database. A database is a collection of linked tables. SQL lets you ask precise questions and receive only the rows and columns you asked for — without loading everything into memory.

Almost every business tool that stores data — booking systems, POS tills, CRMs, loyalty apps — has a database underneath it. SQL is how you get data out of it.

---

## SQL vs Pandas

Pandas loads an entire file into your computer's memory. That works for thousands of rows. A real client database might have 500,000 rows or more — Pandas would crash the machine.

SQL filters inside the database before sending anything to you. Only the rows you asked for arrive. That's why SQL exists and why real client systems use it.

---

## SQLite

SQLite is a database that lives in a single file on your computer. No server, no installation, no passwords. It is built into Python. The SQL you write for SQLite is identical to PostgreSQL and MySQL — only the connection code changes when you upgrade to a real client database.

---

## The Clause Order — Always in This Sequence

```
SELECT    →  which columns you want
FROM      →  which table to look in
JOIN      →  bring in a second table (if needed)
WHERE     →  filter rows before any calculation
GROUP BY  →  collapse rows into summaries
ORDER BY  →  sort the result
```

SELECT and FROM are always required. Every other clause is optional depending on what you need.

---

## SELECT and FROM

Picks which columns you want and which table to get them from. Writing `SELECT *` returns all columns — avoid this on large tables as it is slow.

### Template
```python
cursor.execute("""
    SELECT column_one, column_two
    FROM table_name
""")
rows = cursor.fetchall()
for row in rows:
    print(row)
```

### Luigi example
```python
cursor.execute("SELECT customer_name, item FROM orders")
```

---

## WHERE

Filters rows before any results are returned. Only rows matching the condition come back. Text values go in single quotes. Numbers do not need quotes. WHERE runs before GROUP BY — it filters raw rows, not summaries.

### Template
```python
cursor.execute("""
    SELECT column_one, column_two
    FROM table_name
    WHERE column_name = 'value'
""")
```

### Operators you can use in WHERE
```
=        exact match
!=       not equal
>        greater than
<        less than
>=       greater than or equal
LIKE     pattern match  (e.g. WHERE name LIKE 'M%' means starts with M)
```

### Luigi example
```python
cursor.execute("""
    SELECT customer_name, item, quantity
    FROM orders
    WHERE item = 'Pepperoni'
""")
```

---

## GROUP BY and Aggregate Functions

GROUP BY collapses all rows that share the same value into a single summary row. Must be paired with an aggregate function on every other column in SELECT.

### Aggregate functions
```
SUM(column)       adds up values
COUNT(column)     counts the number of rows
AVG(column)       calculates the average
MAX(column)       returns the highest value
MIN(column)       returns the lowest value
```

Use `AS` to give the result column a readable name.

### Template
```python
cursor.execute("""
    SELECT column_name, SUM(value_column) AS total
    FROM table_name
    GROUP BY column_name
""")
```

### Luigi example — total spend per customer
```python
cursor.execute("""
    SELECT customer_name, SUM(quantity * price) AS total_spent
    FROM orders
    GROUP BY customer_name
""")
```

---

## ORDER BY

Sorts the result. `DESC` sorts highest to lowest. `ASC` sorts lowest to highest and is the default. ORDER BY always comes after GROUP BY. The column name must match exactly what you named it in SELECT, including any alias set with AS.

### Template
```python
cursor.execute("""
    SELECT column_name, SUM(value_column) AS total
    FROM table_name
    GROUP BY column_name
    ORDER BY total DESC
""")
```

### Luigi example — best sellers
```python
cursor.execute("""
    SELECT item, SUM(quantity) AS total_quantity_sold
    FROM orders
    GROUP BY item
    ORDER BY total_quantity_sold DESC
""")
```

---

## JOIN

JOIN combines columns from two tables based on a matching column. The ON condition is the bridge — without it SQL does not know how the tables relate.

Real databases never store everything in one table. Orders live in one table, email addresses in another. JOIN connects them so you can pull both into one result.

### Template
```python
cursor.execute("""
    SELECT table_one.column, table_two.column
    FROM table_one
    JOIN table_two ON table_one.shared_column = table_two.shared_column
""")
```

### Full template — JOIN with GROUP BY and ORDER BY
```python
cursor.execute("""
    SELECT table_one.group_column, table_two.extra_column, SUM(table_one.value_column) AS total
    FROM table_one
    JOIN table_two ON table_one.shared_column = table_two.shared_column
    GROUP BY table_one.group_column
    ORDER BY total DESC
""")
```

### Luigi example — spend per customer with email
```python
cursor.execute("""
    SELECT orders.customer_name, customers.email, SUM(orders.quantity * orders.price) AS total_spent
    FROM orders
    JOIN customers ON orders.customer_name = customers.customer_name
    GROUP BY orders.customer_name
    ORDER BY total_spent DESC
""")
```

---

## Python Connection Template

```python
import sqlite3

# Open connection
conn = sqlite3.connect("database_name.db")
cursor = conn.cursor()

# Run queries here
cursor.execute(""" YOUR SQL HERE """)
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close ONCE at the very end — never in the middle
conn.close()
```

### Key rules
- `sqlite3.connect()` opens the connection to the database file
- `conn.cursor()` creates the cursor that sends and receives queries
- `cursor.execute()` sends a SQL query to the database
- `cursor.fetchall()` collects all rows sent back as a list of tuples
- `conn.close()` closes the connection — call this ONCE at the very end only

---

## Database Setup Template

```python
import sqlite3

conn = sqlite3.connect("luigi.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS table_name (
        id INTEGER PRIMARY KEY,
        text_column TEXT,
        number_column INTEGER,
        decimal_column REAL
    )
""")

# Insert rows
cursor.executemany("""
    INSERT OR IGNORE INTO table_name VALUES (?, ?, ?, ?)
""", [
    (1, "value", 10, 9.99),
    (2, "value", 20, 14.99),
])

conn.commit()
conn.close()
```

---

## Common Error — Database is Locked

If you see `sqlite3.OperationalError: database is locked`, another script crashed without reaching `conn.close()` and is still holding the file open.

**Fix:** Close the terminal and reopen it. If still locked, delete the `.db` file and recreate it — the data is test data and takes seconds to rebuild.

---

## Business Value

Every query you wrote today maps directly to a client deliverable:

- Filtered order list → answer a client's question about specific products in seconds
- Spend per customer → loyalty report, VIP identification, re-engagement targeting
- Best-seller ranking → stock decisions, menu optimisation, promotional planning
- JOIN with emails → marketing list of top spenders ready to export

The difference between you and someone who doesn't know SQL is that you can answer those questions directly from a client's database in minutes rather than asking their developer to do it.

---

*Day 32 complete · git add . → git commit → git push*
