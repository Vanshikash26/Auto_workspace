# ---------- WRITE ("w") : Nayi file / overwrite ----------
with open("notes.txt", "w") as file:
    file.write("Hello! Ye meri pehli file hai.\n")
    file.write("Main automation seekh rahi hu.\n")
print("Step 1: File likh di gayi ✅")

# ---------- READ ("r") : File padhna ----------
with open("notes.txt", "r") as file:
    content = file.read()
print("Step 2: File ka content:")
print(content)

# ---------- APPEND ("a") : End mein jodna ----------
with open("notes.txt", "a") as file:
    file.write("Aaj Day 6 complete kiya!\n")
print("Step 3: Naya line jud gaya ✅")

# ---------- READ again : Append verify karna ----------
with open("notes.txt", "r") as file:
    print("Step 4: Final content:")
    print(file.read())


entry = input("Aaj ki entry likho: ")

