import requests
import re
import time

print("⚖️ ETHICS & CLEANING PIPELINE STARTED...\n")

# ---------- 1. ROBOTS.TXT CHECKER (Ethics) ----------
def check_robots_txt(domain):
    url = f"{domain}/robots.txt"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"✅ {domain} ka robots.txt mil gaya!")
            # Simple check: agar pure 'Disallow: /' hai toh mana hai
            if "Disallow: /" in response.text and "Allow" not in response.text:
                print("🚫 WARNING: Site ne scraping mana ki hai! Abort karo.")
            else:
                print("✅ Scraping allowed (par rules padh lena).")
        else:
            print("❌ robots.txt nahi mila (404). Default allowed samjho, par careful raho.")
    except Exception as e:
        print(f"Error: {e}")

print("🕵️ Checking Ethics (robots.txt)...")
check_robots_txt("https://quotes.toscrape.com")
check_robots_txt("https://books.toscrape.com")


# ---------- 2. DATA CLEANING (Regex Magic) ----------
print("\n🧹 DATA CLEANING PIPELINE...\n")

# Internet se aisa ganda data aata hai
messy_data = [
    "Price: £51.77 (incl. tax)",
    "  Price: £20.00 (excl. tax)  ",
    "Out of stock - Price N/A",
    "Rating: 4.5/5 stars"
]

clean_data = []

for text in messy_data:
    # 1. String method: extra spaces hatao
    text = text.strip()
    
    # 2. Regex Magic: r'[\d\.]+' ka matlab hai "digits (0-9) aur dot (.) dhundo"
    numbers = re.findall(r'[\d\.]+', text)
    
    if numbers:
        # Pehla number nikalo aur float (decimal) mein badlo
        price = float(numbers[0])
        clean_data.append({"Original": text, "Clean_Value": price})
        print(f"✨ '{text}' -> {price}")
    else:
        print(f"⚠️ '{text}' -> No number found (Skipped)")
        
print(f"\n✅ Total {len(clean_data)} clean records ready for client!")

# ---------- 3. POLITE SCRAPER TEMPLATE ----------
print("\n🤖 Polite Scraper Test...")
urls = [
    "https://quotes.toscrape.com/page/1/",
    "https://quotes.toscrape.com/page/2/"
]

for url in urls:
    print(f"Fetching {url}...")
    # Hamesha User-Agent bhejo (taaki site ko lage tum Chrome ho)
    headers = {"User-Agent": "Mozilla/5.0 (Ethical Student Bot)"}
    requests.get(url, headers=headers)
    
    # Politeness: 2 second ruko
    time.sleep(2)
print("✅ Done without spamming the server!")