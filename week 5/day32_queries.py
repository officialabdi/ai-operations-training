import sqlite3
conn = sqlite3.connect("luigi.db")
cursor = conn.cursor()

cursor.execute("select customer_name, item from orders")
rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.execute("select customer_name, item, quantity from orders where item = 'Pepperoni'")
rows = cursor.fetchall()
for row in rows:
    print(row)

print("---")
cursor.execute("""
    select customer_name, sum(quantity * price) as total_spent
    from orders
    group by customer_name
""")
rows = cursor.fetchall()
for row in rows:
    print(row)

print("---")
cursor.execute("""
    select orders.customer_name, customers.email, sum(orders.quantity * orders.price)as total_spent
    from orders
    join customers on orders.customer_name = customers.customer_name
    group by orders.customer_name
""")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.execute("""
    select item, sum(quantity) as total_quantity_sold
    from orders
    group by item
    order by total_quantity_sold DESC
""")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()