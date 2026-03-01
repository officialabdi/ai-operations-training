import pandas as pd

df = pd.read_csv(r"c:\Users\abdi0\OneDrive\ai road 2026\day 30\customers.csv")

print("=== SHAPE ===")
print(df.shape)

print("\n=== COLUMNS ===")
print(df.columns.tolist())

print("\n=== FIRST 6 ROWS ===")
print(df.head())

print("\n=== DATA TYPES ===")
print(df.dtypes)

print("\n=== BASIC STATS ===")
print(df.describe())

print("\n=== single column ===")
print(df['name'])

print("\n=== multiple columns ===")
print(df[['name', 'customer_type', 'visit_count']])

print("\n=== vip customers only ===")
vip_customers = df[df['customer_type'] == 'VIP']
print(vip_customers[['name', 'visit_count']])

print("\n=== customers with 5+ visits ===")
loyal = df[df['visit_count'] >= 5]
print(loyal[['name', 'visit_count', 'customer_type']])

print("\n=== NO SHOWS ===")
no_shows = df[df['customer_type'] == 'no_show']
print(no_shows[['name', 'last_visit']])


# ── SORTING ───────────────────────────────────────────────────────────────────

print("\n=== SORTED BY VISIT COUNT (highest first) ===")
sorted_df = df.sort_values('visit_count', ascending=False)
print(sorted_df[['name', 'visit_count', 'customer_type']])

print("\n=== add loyalty tier column ===")

def assign_tier(visits):
    if visits >= 10:
        return 'Gold'
    elif visits >= 5:
        return 'Silver'
    elif visits >= 1:
        return 'Bronze'
    else:
        return 'None'
    
df['loyalty_tier'] = df['visit_count'].apply(assign_tier)
print(df[['name', 'visit_count', 'loyalty_tier']])

print("\n=== customer type breakdown ===")
print(df['customer_type'].value_counts())

print("\n=== loyalty tier breakdown")
print(df['loyalty_tier'].value_counts())

output_path = r"c:\Users\abdi0\OneDrive\ai road 2026\day 30\customers_enriched.csv"
df.to_csv(output_path, index=False)
print(f"\n Saved enriched data to customers_enriched.csv")