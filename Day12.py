import pandas as pd

# ---------- 1. DataFrame banao (dict se) ----------
data = {
    "Name": ["Aarav", "Diya", "Kabir", "Meera", "Rohan"],
    "Age": [22, 21, 23, 21, 24],
    "City": ["Delhi", "Mumbai", "Pune", "Jaipur", "Delhi"],
    "Marks": [85, 92, 78, 95, 88],
}
df = pd.DataFrame(data)
print("DataFrame:")
print(df)

# CSV mein save karo
df.to_csv("students.csv", index=False)
print("\n✅ students.csv ban gayi!")

# ---------- 2. CSV wapas load karo ----------
df = pd.read_csv("students.csv")
print("\nPehli 3 rows (head):")
print(df.head(3))
print("\nShape (rows, columns):", df.shape)
print("Columns:", list(df.columns))

# ---------- 3. Filter + Sort ----------
toppers = df[df["Marks"] > 85]
print("\nToppers (Marks > 85):")
print(toppers)

sorted_df = df.sort_values("Marks", ascending=False)
print("\nSorted (highest first):")
print(sorted_df)
# Messy data (kuch values missing)
messy = pd.DataFrame({"Name": ["A", "B", None], "Marks": [10, None, 30]})
print("\nMissing values count:")
print(messy.isnull().sum())