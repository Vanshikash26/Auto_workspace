import requests
import json

print("🔌 DAY 25: APIs - Internet ka WAITER!\n")

# ==========================================
# PART 1: GitHub API (Simple Object)
# ==========================================
print("=" * 50)
print("PART 1: GitHub API")
print("=" * 50)

url = "https://api.github.com/users/Vanshikash26"
response = requests.get(url)
print(f"Status Code: {response.status_code}")

# JSON ko Python dict mein badlo
data = response.json()

# Specific fields nikalo (dict jaise access karo)
print(f"Username  : {data['login']}")
print(f"Name      : {data['name']}")
print(f"Followers : {data['followers']}")
print(f"Repos     : {data['public_repos']}")


# ==========================================
# PART 2: JSONPlaceholder (Array of Objects)
# ==========================================
print("\n" + "=" * 50)
print("PART 2: JSONPlaceholder (100 posts)")
print("=" * 50)

url2 = "https://jsonplaceholder.typicode.com/posts"
response2 = requests.get(url2)
posts = response2.json()   # Ye ek LIST hai (100 dicts)

print(f"Total posts: {len(posts)}")

# Pehle 3 posts loop se dekho
for i, post in enumerate(posts[:10]):
    print(f"\n📝 Post {i+1}: {post['title'][:45]}...")
    print(f"   by userId: {post['userId']}")


# ==========================================
# PART 3: Open-Meteo Weather (Delhi!)
# ==========================================
print("\n" + "=" * 50)
print("PART 3: Open-Meteo Weather (Delhi)")
print("=" * 50)

# Query parameters (? ke baad wale) - dict mein do
params = {
    "latitude": 28.66,      # Delhi
    "longitude": 77.43,
    "current_weather": True
}

url3 = "https://api.open-meteo.com/v1/forecast"
response3 = requests.get(url3, params=params)
weather = response3.json()

# Nested JSON navigate karo: weather -> current_weather -> temperature
current = weather["current_weather"]

# Weather code ka matlab
weather_codes = {0: "☀️ Clear", 1: "🌤️ Mainly Clear", 2: "⛅ Partly Cloudy",
                 3: "☁️ Overcast", 45: "🌫️ Fog", 61: "🌧️ Rain", 71: "🌨️ Snow"}
code = current["weathercode"]
description = weather_codes.get(code, f"Code {code}")

print(f"🌍 Delhi ka Weather:")
print(f"   {description}")
print(f"   🌡️  Temperature : {current['temperature']}°C")
print(f"   💨 Wind Speed   : {current['windspeed']} km/h")


# ==========================================
# BONUS: Pretty Print (JSON ko sundar dikhao)
# ==========================================
print("\n" + "=" * 50)
print("BONUS: Pretty Print (weather JSON)")
print("=" * 50)
print(json.dumps(weather, indent=2))

# Comments API try karo
response4 = requests.get("https://jsonplaceholder.typicode.com/comments?postId=1")
comments = response4.json()
print(f"\nTotal comments: {len(comments)}")
print(f"Pehla comment: {comments[0]['email']}")
