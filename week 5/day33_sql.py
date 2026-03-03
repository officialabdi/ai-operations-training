import sqlite3

# Step 1: Connect (creates the file if it doesn't exist)
conn = sqlite3.connect("luigi_pizzeria.db")

# Step 2: Create a cursor
cursor = conn.cursor()

# Step 3: Create a table and insert data
cursor.executescript("""
    DROP TABLE IF EXISTS orders;

    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        customer TEXT,
        item TEXT,
        quantity INTEGER,
        price REAL,
        status TEXT
    );

    INSERT INTO orders VALUES
        (1, 'Aoife', 'Margherita', 2, 12.50, 'delivered'),
        (2, 'Ciarán', 'Pepperoni', 1, 14.00, 'delivered'),
        (3, 'Sinéad', 'Garlic Bread', 3, 4.50, 'pending'),
        (4, 'Pádraig', 'Margherita', 1, 12.50, 'cancelled'),
        (5, 'Aoife', 'Pepperoni', 2, 14.00, 'delivered'),
        (6, 'Sinéad', 'Calzone', 1, 15.00, 'pending');
""")

conn.commit()
print("Database created.")
conn.close()