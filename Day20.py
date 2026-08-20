import requests
from playwright.sync_api import sync_playwright

# ---------- 1. STATIC SITE (requests se) ----------
print("🌐 STATIC SITE TEST (requests)...")
url_static = "https://quotes.toscrape.com"
response = requests.get(url_static)
print(f"Status: {response.status_code}")
print(f"HTML length: {len(response.text)} characters")
print(f"'quote' mila HTML mein? {'quote' in response.text}")


# ---------- 2. DYNAMIC SITE (requests FAIL hoga) ----------
print("\n🌐 DYNAMIC SITE TEST (requests)...")
url_dynamic = "https://quotes.toscrape.com/js/"
response2 = requests.get(url_dynamic)
print(f"Status: {response2.status_code}")
print(f"'quote' mila HTML mein? {'quote' in response2.text}")
print("⚠️ Dekho: Dynamic site par 'quote' NAHI mila (JavaScript load nahi hua)!")


# ---------- 3. PLAYWRIGHT SE (Asli Browser) ----------
print("\n🎭 PLAYWRIGHT SE DYNAMIC SITE LOAD KAR RAHE HAIN...")

with sync_playwright() as p:
    # Browser kholo (headless=False = browser dikhega!)
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Dynamic site kholo
    page.goto(url_dynamic)

    # Title nikalo
    title = page.title()
    print(f"✅ Page Title: {title}")

    # Quotes nikalo (JavaScript load hone ke baad)
    quotes = page.query_selector_all("div.quote")
    print(f"✅ Playwright se {len(quotes)} quotes mile!")

    # Screenshot lo
    page.screenshot(path="dynamic_screenshot.png")
    print("✅ Screenshot save ho gaya: dynamic_screenshot.png")

    # Browser band karo
    browser.close()

print("\n🎉 DONE! Dynamic site successfully scrape ho gayi!")