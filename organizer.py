import os
import shutil

# Category mapping (kaunsi extension kis category mein)
categories = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".doc", ".docx", ".txt"],
    "Videos": [".mp4", ".avi", ".mkv"],
    "Audio": [".mp3", ".wav"],
    "Code": [".py", ".js", ".html"],
    "Archives": [".zip", ".rar", ".7z"],
}

# Organize karne wala function
def organize(folder):
    moved = 0

    for item in os.listdir(folder):
        full_path = os.path.join(folder, item)

        # Folder ko skip karo, sirf files uthao
        if os.path.isdir(full_path):
            continue

        # Naam ko todo: naam + extension
        _, ext = os.path.splitext(item)
        ext = ext.lower()

        # Category dhundo (na mile toh Others)
        target = "Others"
        for category, extensions in categories.items():
            if ext in extensions:
                target = category
                break

        # Category folder banao
        target_folder = os.path.join(folder, target)
        os.makedirs(target_folder, exist_ok=True)

        # File ko move karo (cut-paste)
        shutil.move(full_path, os.path.join(target_folder, item))
        print(f"📦 {item} → {target}")
        moved += 1

    print(f"\n✅ Total {moved} files organize ho gayi!")

# Test folder par chalao
organize("messy_folder")