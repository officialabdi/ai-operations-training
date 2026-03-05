# Day 35 - Full Data Stack Pipeline
# Luigi's Pizzeria - Weekly Sales Report

# --- STEP 1: IMPORT LIBRARIES ---
import pandas as pd
import sqlite3
import os

try:
    # --- STEP 2: LOAD CSV ---
    data = {
        "order_id": [1, 2, 3, 4, 5],
        "customer": ["Mario", "Luigi", "Sofia", "Mario", "Sofia"],
        "item": ["Margherita", "Pepperoni", "Margherita", "Calzone", "Pepperoni"],
        "quantity": [2, 1, 3, 1, 2],
        "price": [12.00, 14.00, 12.00, 10.00, 14.00]
    }

    df = pd.DataFrame(data)
    print("CSV loaded:")
    print(df)

    # --- STEP 3: STORE IN SQLITE ---
    conn = sqlite3.connect("luigi_pipeline.db")
    df.to_sql("sales", conn, if_exists="replace", index=False)
    print("Data stored in SQLite.")

    # --- STEP 4: QUERY WITH SQL ---
    query = """
        SELECT customer, SUM(quantity * price) AS total_spent
        FROM sales
        GROUP BY customer
        ORDER BY total_spent DESC
    """

    results = pd.read_sql(query, conn)
    print("Query results:")
    print(results)

    # --- STEP 5: ANALYSE WITH PANDAS ---
    total_revenue = results["total_spent"].sum()
    results["revenue_share"] = (results["total_spent"] / total_revenue * 100).round(2)
    print("Analysis:")
    print(results)

    # --- STEP 6: EXPORT REPORT ---
    results.to_csv("luigi_report.csv", index=False)
    conn.close()
    print("Report saved to luigi_report.csv")

except Exception as e:
    print(f"Pipeline failed: {e}")
