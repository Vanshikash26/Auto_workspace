import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os
import logging

# ========================================================
#   CONFIG
# ========================================================
URL = "https://books.toscrape.com"
HISTORY_FILE = "price_history.csv"
NUM_BOOKS = 5                      # Kitni books track karni hain
DROP_THRESHOLD_PERCENT = 10        # 10%+ gira toh ALERT
SEND_EMAIL = False                 # True karo toh email jayegi
SENDER_EMAIL = ""                  # Apna Gmail (agar email chahiye)
RECEIVER_EMAIL = ""                # Kisko bhejna hai

# ========================================================
#   LOGGING
# ========================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("price_tracker.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# ========================================================
#   SCRAPE: Top N books ke prices nikalo
# ========================================================
def scrape_prices():
    headers = {"User-Agent": "Mozilla/5.0 (Ethical Price Tracker)"}
    response = requests.get(URL, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    books = []
    for b in soup.select("article.product_pod")[:NUM_BOOKS]:
        title = b.select_one("h3 a")["title"]
        price_text = b.select_one("p.price_color").get_text()
        price = float(price_text.replace("£", "").replace("Â", "").strip())
        books.append({"Book": title, "Price": price})
    return books

# ========================================================
#   HISTORY: Purani prices load karo
# ========================================================
def load_history():
    if os.path.exists(HISTORY_FILE):
        return pd.read_csv(HISTORY_FILE)
    return pd.DataFrame(columns=["Timestamp", "Book", "Price"])

def get_last_price(history_df, book):
    """Kisi book ki sabse recent (aakhri) price nikalo"""
    book_history = history_df[history_df["Book"] == book]
    if book_history.empty:
        return None
    return book_history.iloc[-1]["Price"]

# ========================================================
#   ALERT: Price drop par email/log
# ========================================================
def send_price_alert(alerts):
    logging.info("🔔 PRICE DROP ALERT!")
    body = "💰 PRICE DROP ALERT!\n\n"
    for book, old, new, pct in alerts:
        logging.info(f"   📉 {book}: £{old} → £{new} ({pct:.1f}%)")
        body += f"📉 {book}: £{old} → £{new} ({pct:.1f}% drop)\n"

    if not SEND_EMAIL:
        return

    # Day 13 wala email code
    try:
        import smtplib
        from email.mime.text import MIMEText
        app_password = input("🔑 Gmail App Password daalo: ")
        msg = MIMEText(body)
        msg["Subject"] = "💰 Price Drop Alert!"
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, app_password)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        logging.info("✅ Alert email bhej di!")
    except Exception as e:
        logging.error(f"❌ Email error: {e}")

# ========================================================
#   MAIN LOGIC
# ========================================================
def main():
    logging.info("💰 PRICE TRACKER STARTED")

    # Step 1: Current prices scrape karo
    current = scrape_prices()
    logging.info(f"📥 {len(current)} books ke prices scrape hue")

    # Step 2: Purani history load karo
    history = load_history()

    # Step 3: Har book ka change detect karo
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alerts = []

    for item in current:
        book = item["Book"]
        price = item["Price"]
        last_price = get_last_price(history, book)

        if last_price is None:
            logging.info(f"🆕 {book}: £{price} (baseline set)")
        else:
            change_pct = ((price - last_price) / last_price) * 100
            if change_pct <= -DROP_THRESHOLD_PERCENT:
                logging.info(f"🔔 BIG DROP! {book}: £{last_price} → £{price} ({change_pct:.1f}%)")
                alerts.append((book, last_price, price, change_pct))
            elif change_pct < 0:
                logging.info(f"📉 {book}: £{last_price} → £{price} ({change_pct:.1f}%)")
            elif change_pct > 0:
                logging.info(f"📈 {book}: £{last_price} → £{price} (+{change_pct:.1f}%)")
            else:
                logging.info(f"➡️ {book}: £{price} (no change)")

    # Step 4: Alert bhejo agar koi bada drop hai
    if alerts:
        send_price_alert(alerts)
    else:
        logging.info("😴 Koi bada price drop nahi is baar")

    # Step 5: Current prices history mein save karo
    new_rows = pd.DataFrame([
        {"Timestamp": timestamp, "Book": item["Book"], "Price": item["Price"]}
        for item in current
    ])
    updated = pd.concat([history, new_rows], ignore_index=True)
    updated.to_csv(HISTORY_FILE, index=False)
    logging.info(f"💾 {len(current)} prices history mein save hue")

    # Step 6: Summary report
    prices = [item["Price"] for item in current]
    logging.info("\n📊 SUMMARY REPORT")
    logging.info(f"   Books tracked : {len(current)}")
    logging.info(f"   Average price : £{sum(prices)/len(prices):.2f}")
    logging.info(f"   Highest price : £{max(prices):.2f}")
    logging.info(f"   Lowest price  : £{min(prices):.2f}")

if __name__ == "__main__":
    main()

    