import sqlite3
import pandas as pd

conn = sqlite3.connect("luigi_pizzeria.db")

df = pd.read_sql("select * FROM orders where status = 'delivered'", conn)
print(df)
print(df["price"].sum())
conn.close()

import sqlite3
import pandas as pd

conn = sqlite3.connect("luigi_pizzeria.db")

df = pd.read_sql("select * from orders where status = 'delivered'", conn)

revenue_by_customer = df.groupby("customer")["price"].sum()

print(revenue_by_customer)
conn.close()

import sqlite3
import pandas as pd

conn = sqlite3.connect("luigi_pizzeria.db")

df = pd.read_sql("select * from orders where status = 'delivered'", conn)

summary = df.groupby("customer")["price"].sum().reset_index()
summary.columns = ["customer", "total_spent"]

summary.to_sql("customer_summary", conn, if_exists="replace", index=False)

result = pd.read_sql("select * from customer_summary", conn)
print(result)
conn.close()


"""FULL NOTES — Day 33: SQL + Python Integration
sqlite3
Python's built-in library for connecting to SQLite databases. No installation needed. Every database session follows the same three steps: connect, create cursor, execute commands.
sqlite3.connect("filename.db") — opens the database file. Creates it if it doesn't exist.
conn.cursor() — creates a cursor object. The cursor is what actually sends commands to the database.
cursor.executescript() — runs multiple SQL statements at once. Used for setup tasks like creating tables and inserting data.
cursor.execute() — runs a single SQL statement. Used for queries.
cursor.fetchall() — collects all results after a query. Returns a list of tuples. Each tuple is one row.
conn.commit() — saves any changes made to the database.
conn.close() — closes the connection. Always do this when finished."""