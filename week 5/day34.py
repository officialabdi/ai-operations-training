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


"""
Topic: Data Pipeline — CSV + SQL + Pandas Combined

pd.read_csv()
Reads a CSV file from your file system and returns a DataFrame. The first row of the CSV becomes the column headers. Pandas automatically detects data types — strings, integers, floats.
Requires the CSV file to be in the same folder as your script, or you must provide the full file path.

pd.to_sql()
Writes a DataFrame into a SQLite database as a table. Takes three required inputs: the table name, the database connection, and the if_exists parameter.
if_exists="replace" — wipes the existing table and writes fresh data. Use this when the client sends you an updated file.
if_exists="append" — adds new rows to the existing table. Use this when you're adding to historical data.
index=False — stops Pandas from writing its internal row numbers into the database as a column.
The database file is created automatically if it doesn't exist yet.

pd.read_sql()
Runs a SQL query against a database and returns the results as a DataFrame. Takes two inputs: the SQL query as a string, and the database connection.
The returned DataFrame behaves exactly like any other DataFrame — you can add columns, filter it, or run further calculations on it.

conn.close()
Closes the connection to the database once you're finished. Always close the connection at the end of your script. Leaving it open can cause issues if the script runs again or if another process tries to access the database.

A data pipeline
A script that moves data through a series of steps in sequence — load, store, query, analyse — and produces a clean output. The value to a client is automation: they send you a file, the script runs, they get an answer.

The full sequence used today

pd.read_csv() — load the client's CSV into a DataFrame
sqlite3.connect() — open or create the database
df.to_sql() — write the DataFrame into the database as a table
pd.read_sql() — query the database with SQL, get back a DataFrame
DataFrame operations — add calculated columns, filter, sort
conn.close() — close the database connection

"""