import os

# Test folder ka naam
folder = "messy_folder"

# Folder banao (agar pehle se hai toh error mat do)
os.makedirs(folder, exist_ok=True)

# Nakli messy files (har type ki)
files = [
    "photo1.jpg", "photo2.png", "song.mp3", "movie.mp4",
    "notes.txt", "report.pdf", "script.py", "index.html",
    "backup.zip", "data.docx", "image.gif", "video.mkv",
    "data.csv", "mystery.xyz"
]

# Har file banao
for f in files:
    with open(os.path.join(folder, f), "w") as file:
        file.write("test")

print(f"✅ {folder} mein {len(files)} messy files bana di!")