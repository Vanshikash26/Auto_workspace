from playwright.sync_api import sync_playwright

print("🎯 PLAYWRIGHT DEEP DIVE STARTED...\n")

with sync_playwright() as p:
    # Browser kholo (headless=False = browser dikhega)
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # ==========================================
    # PART 1: LOGIN AUTOMATION
    # ==========================================
    print("🔐 PART 1: LOGIN AUTOMATION...")

    # Login page kholo
    page.goto("https://the-internet.herokuapp.com/login")
    print("✅ Login page khul gaya!")

    # Username field mein type karo
    page.fill("#username", "tomsmith")
    print("✅ Username bhar diya!")

    # Password field mein type karo
    page.fill("#password", "SuperSecretPassword!")
    print("✅ Password bhar diya!")

    # Login button CLICK karo
    page.click("#login button")
    print("✅ Login button click kar diya!")

    # Wait karo jab tak success message aaye
    page.wait_for_selector("#flash")

    # Success message nikalo
    flash = page.inner_text("#flash")
    print(f"🎉 Login Result: {flash.strip()}")


    # ==========================================
    # PART 2: WIKIPEDIA SEARCH AUTOMATION
    # ==========================================
    print("\n🔍 PART 2: WIKIPEDIA SEARCH...")

    # Wikipedia kholo
    page.goto("https://en.wikipedia.org")
    print("✅ Wikipedia khul gaya!")

    # Search box mein type karo
    page.fill("#searchInput", "Python programming")
    print("✅ Search box mein likh diya!")

    # Search button click karo
    page.click("#search-form button")
    print("✅ Search button click kar diya!")

    # Wait karo jab tak results aayein
    page.wait_for_selector("h1")

    # Page title nikalo (jo page khula)
    title = page.inner_text("h1")
    print(f"🎉 Search Result Page: {title}")


    # ==========================================
    # PART 3: DYNAMIC QUOTES SCRAPE (with JS wait)
    # ==========================================
    print("\n📜 PART 3: DYNAMIC QUOTES SCRAPE...")

    page.goto("https://quotes.toscrape.com/js/")

    # Wait karo jab tak quotes JavaScript se load ho jayein
    page.wait_for_selector("div.quote")

    # Saare quote blocks dhundo
    quotes = page.query_selector_all("div.quote")
    print(f"✅ {len(quotes)} quotes mile!")

    # Pehle 3 quotes print karo
    for i, quote in enumerate(quotes[:3]):
        text = quote.query_selector("span.text").inner_text()
        author = quote.query_selector("small.author").inner_text()
        print(f"\n💬 Quote {i+1}: {text[:60]}...")
        print(f"   ✍️ Author: {author}")

    # Screenshot lo
    page.screenshot(path="day21_screenshot.png")
    print("\n✅ Screenshot save ho gaya!")

    # Browser band karo
    browser.close()

print("\n🎉 DAY 21 COMPLETE! Browser control mastered!")