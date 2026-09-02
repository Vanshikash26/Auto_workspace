import requests

BOT_TOKEN = input("🔑 Bot Token paste karo: ")
CHAT_ID = input("💬 Apna Chat ID paste karo: ")

def send_message(text):
    """Telegram par message bhejo"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    response = requests.post(url, data=data)
    return response.json()

def get_coordinates(city):
    """City se coordinates nikalo"""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 1, "language": "en"}
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    if "results" not in data or not data["results"]:
        return None
    r = data["results"][0]
    return r["latitude"], r["longitude"], r["name"]

def get_weather(lat, lon):
    """Coordinates se weather nikalo"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": lat, "longitude": lon, "current_weather": True}
    response = requests.get(url, params=params, timeout=10)
    return response.json()["current_weather"]

# ---------- MAIN ----------
city = input("🌍 City ka naam daalo: ")
coords = get_coordinates(city)

if coords:
    lat, lon, name = coords
    weather = get_weather(lat, lon)

    # Sundar message banao
    message = f"🌤️ {name} ka Weather\n"
    message += f"🌡️ Temperature: {weather['temperature']}°C\n"
    message += f"💨 Wind Speed: {weather['windspeed']} km/h"

    # Telegram par bhejo
    result = send_message(message)
    if result.get("ok"):
        print("✅ Weather Telegram par bhej diya!")
    else:
        print(f"❌ Error: {result}")
else:
    print(f"❌ City '{city}' nahi mili!")
    