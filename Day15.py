import requests

print("🚀 Internet se baat shuru...")

# ---------- 1. Website ka HTML Download karna ----------
url = "https://quotes.toscrape.com"
response = requests.get(url)

# Status code check karo (200 matlab website ne welcome kiya)
print(f"\nWebsite Status Code: {response.status_code}")

# HTML code ko file mein save karo
with open("website.html", "w", encoding="utf-8") as file:
    file.write(response.text)
print("✅ website.html save ho gayi! Isko browser mein khol kar dekho.")


# ---------- 2. API Tester (Machine to Machine baat) ----------
# GitHub ka API call karte hain (kisi user ki details nikalne ke liye)
api_url = "https://api.github.com/users/octocat"
api_response = requests.get(api_url)

# JSON data ko Python dictionary mein badlo
data = api_response.json()

print("\n👤 GitHub API Data:")
print(f"Username: {data['login']}")
print(f"Bio: {data['bio']}")
print(f"Followers: {data['followers']}")
# Headers = Tumhara ID Card
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Header bhej kar request karo
safe_response = requests.get("https://httpbin.org/headers", headers=headers)
print("\nServer ko kya dikha:")
print(safe_response.json())