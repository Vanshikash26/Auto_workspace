import requests

# Weather codes ka matlab
WEATHER_CODES = {
    0: "☀️ Clear Sky", 1: "🌤️ Mainly Clear", 2: "⛅ Partly Cloudy",
    3: "☁️ Overcast", 45: "🌫️ Fog", 48: "🌫️ Freezing Fog",
    51: "🌦️ Light Drizzle", 61: "🌧️ Light Rain", 63: "🌧️ Rain",
    71: "🌨️ Snow", 80: "🌧️ Rain Showers", 95: "⛈️ Thunderstorm"
}

def get_coordinates(city):
    """City ke naam se latitude/longitude nikalo"""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 1, "language": "en"}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    # Agar city nahi mili
    if "results" not in data or len(data["results"]) == 0:
        return None

    result = data["results"][0]
    return result["latitude"], result["longitude"], result["name"]

def get_weather(lat, lon):
    """Coordinates se weather nikalo"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": lat, "longitude": lon, "current_weather": True}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()["current_weather"]

# ---------- MAIN ----------
def main():
    print("🌦️  WEATHER CLI\n")
    city = input("🌍 City ka naam daalo: ")

    try:
        # Step 1: City → Coordinates
        coords = get_coordinates(city)
        if coords is None:
            print(f"❌ '{city}' nahi mila! Spelling check karo.")
            return

        lat, lon, name = coords
        print(f"📍 Mila: {name} ({lat}, {lon})")

        # Step 2: Coordinates → Weather
        weather = get_weather(lat, lon)
        code = weather["weathercode"]
        description = WEATHER_CODES.get(code, f"Code {code}")

        print(f"\n🌤️  {name} ka Weather:")
        print(f"   {description}")
        print(f"   🌡️  Temperature : {weather['temperature']}°C")
        print(f"   💨 Wind Speed   : {weather['windspeed']} km/h")

    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")

if __name__ == "__main__":
    main()