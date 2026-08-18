import pandas as pd

# Messy data jisme missing values aur duplicates hain
data = {
    "Date": ["2026-08-01", "2026-08-01", "2026-08-02", "2026-08-02", "2026-08-03", "2026-08-03", "2026-08-04"],
    "Region": ["North", "North", "South", "South", "North", "East", None],
    "Product": ["Laptop", "Laptop", "Phone", "Tablet", "Phone", "Laptop", "Phone"],
    "Sales": [50000, 50000, 20000, 15000, 22000, 45000, 18000]
}

df = pd.DataFrame(data)

# CSV mein save karo
df.to_csv("messy_sales.csv", index=False)
print("✅ messy_sales.csv ban gayi! Isme duplicates aur None values hain.")