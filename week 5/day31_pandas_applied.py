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