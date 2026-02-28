import sqlite3

conn = sqlite3.connect("luigi.db")
cursor = conn.cursor()

# Orders table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        customer_name TEXT,
        item TEXT,
        quantity INTEGER,
        price REAL,
        order_date TEXT
    )
""")

cursor.executemany("""
    INSERT OR IGNORE INTO orders VALUES (?, ?, ?, ?, ?, ?)
""", [
    (1, "Maria",   "Margherita",    2, 12.50, "2024-01-10"),
    (2, "John",    "Pepperoni",     1, 14.00, "2024-01-11"),
    (3, "Maria",   "Garlic Bread",  3,  4.50, "2024-01-11"),
    (4, "Ahmed",   "Pepperoni",     2, 14.00, "2024-01-12"),
    (5, "John",    "Margherita",    1, 12.50, "2024-01-15"),
    (6, "Ahmed",   "Calzone",       1, 16.00, "2024-01-15"),
    (7, "Siobhan", "Margherita",    4, 12.50, "2024-01-16"),
    (8, "Siobhan", "Garlic Bread",  2,  4.50, "2024-01-17"),
    (9, "Maria",   "Calzone",       1, 16.00, "2024-01-18"),
   (10, "John",    "Pepperoni",     3, 14.00, "2024-01-20"),
])

# Customers table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        customer_name TEXT,
        email TEXT
    )
""")

cursor.executemany("""
    INSERT OR IGNORE INTO customers VALUES (?, ?, ?)
""", [
    (1, "Maria",   "maria@email.com"),
    (2, "John",    "john@email.com"),
    (3, "Ahmed",   "ahmed@email.com"),
    (4, "Siobhan", "siobhan@email.com"),
])

conn.commit()
print("Database created.")
conn.close()