import os

# ---------- 1. Folder ki saari files dekho ----------
files = os.listdir()
print("AJ folder mein ye sab hai:")
print(files)
print()

# ---------- 2. Folder banana (exists check ke saath) ----------
if not os.path.exists("mera_folder"):
    os.makedirs("mera_folder")
    print("mera_folder ban gaya ✅")
else:
    print("mera_folder pehle se tha ✅")
print()

# ---------- 3. Temp file banao, rename karo, delete karo ----------
with open("temp.txt", "w") as file:
    file.write("test data")
print("temp.txt ban gayi ✅")

os.rename("temp.txt", "naya_naam.txt")
print("Rename ho gaya: temp.txt -> naya_naam.txt ✅")

os.remove("naya_naam.txt")
print("naya_naam.txt delete ho gayi ✅")
print()

# ---------- 4. COMBO: Saari .py files dhundo ----------
print("Tumhari Python files (tumhari mehnat!):")
for item in files:
    if item.endswith(".py"):
        print(f"  🐍 {item}")