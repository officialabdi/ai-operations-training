import pandas as pd

df = pd.read_csv("luigi_sales.csv")

print(df)
print(df.dtypes)

import sqlite3
conn = sqlite3.connect("luigi.db")

df.to_sql("sales" , conn, if_exists="replace", index=False)

print("data written to database")

query = "select product, quantity from sales order by quantity DESC limit 3 "
top_products = pd.read_sql(query, conn)
print(top_products)

#Full and clean version

import pandas as pd
import sqlite3

#step 1 load csv
df = pd.read_csv("luigi_sales.csv")
print("csv loaded:")
print(df)

#step 2 store in database
conn = sqlite3.connect("luigi.db")
df.to_sql("sales", conn, if_exists="replace", index=False)
print("\ndata written to database")

#step 3 query with sql
query = "select product, category, quantity, price from sales order by quantity DESC"
results = pd.read_sql(query, conn)
print("\nall products by quantity:")
print(results)

#step 4 analyse with pandas
total_revenue = results["quantity"] * results["price"]
results["revenue"] = total_revenue
print("\nrevenue per product:")
print(results[["product", "revenue"]])
conn.close()