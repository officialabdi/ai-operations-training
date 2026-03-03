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