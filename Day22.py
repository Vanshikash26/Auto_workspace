import requests
import random
import time
import logging

# ========================================================
#   1. LOGGING SETUP (Console + File dono mein likho)
# ========================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("scraper.log", encoding="utf-8"),  # file mein
        logging.StreamHandler()                                 # console mein
    ]
)

# ========================================================
#   2. USER-AGENT ROTATION (Block se bachne ke liye)
# ========================================================
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/119.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Firefox/121.0",
]

# ========================================================
#   3. SESSION (cookies + connection persist)
# ========================================================
session = requests.Session()

# ========================================================
#   4. RELIABLE FETCH (Retry + Timeout + Random Delay)
# ========================================================
def reliable_fetch(url, max_retries=3):
    """Safe fetch - fail ho toh retry, timeout, random delay"""

    for attempt in range(1, max_retries + 1):
        try:
            logging.info(f"Attempt {attempt}/{max_retries} → {url}")

            # Random User-Agent choose karo (har baar alag browser jaisa)
            headers = {"User-Agent": random.choice(USER_AGENTS)}

            # Timeout = 10 sec (site hang ho toh rukna mat)
            response = session.get(url, headers=headers, timeout=10)

            # 4xx/5xx error ho toh exception raise karo
            response.raise_for_status()

            logging.info(f"✅ Success! Status {response.status_code}")
            return response

        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Attempt {attempt} failed: {e}")

            # Agar aur attempts bache hain, toh wait karke retry
            if attempt < max_retries:
                wait = random.uniform(2, 5)
                logging.info(f"⏳ {wait:.1f}s wait karke retry...")
                time.sleep(wait)
            else:
                logging.error(f"🚫 All {max_retries} attempts failed: {url}")
                return None

# ========================================================
#   5. USE IT: Multiple pages scrape karo
# ========================================================
if __name__ == "__main__":
    logging.info("🚀 RELIABLE SCRAPER STARTED")

    total_quotes = 0

    for page in range(1, 4):   # 3 pages scrape karenge
        url = f"https://quotes.toscrape.com/page/{page}/"
        response = reliable_fetch(url)

        if response:
            count = response.text.count('class="quote"')
            total_quotes += count
            logging.info(f"📄 Page {page}: {count} quotes mile")
        else:
            logging.warning(f"⚠️ Page {page} skip karna pada (fetch failed)")

        # Politeness: pages ke beech random delay
        time.sleep(random.uniform(1, 2))

    logging.info(f"🎉 DONE! Total {total_quotes} quotes scrape hue")