# ALERT SCRAPER 
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import logging

# ========================================================
#   CONFIG
# ========================================================
URL = "https://books.toscrape.com"
STATE_FILE = "seen_books.csv"     # Yaad rakhne wali file

SEND_EMAIL = True                      
SENDER_EMAIL = "vanshika.sh26@gmail.com"   
RECEIVER_EMAIL = "vanshika.sh26@gmail.com"

# ========================================================
#   LOGGING (console + file)
# ========================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("alert.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# ========================================================
#   STATE MANAGEMENT (yaad rakhna)
# ========================================================
def load_seen():
    """Pichli baar jo dekha tha, wo CSV se load karo"""
    if os.path.exists(STATE_FILE):
        df = pd.read_csv(STATE_FILE)
        return set(df["Title"].tolist())
    return set()   # pehli baar hai, kuch nahi dekha

def save_seen(titles):
    """Ab jo dekha, wo CSV mein save karo"""
    pd.DataFrame({"Title": list(titles)}).to_csv(STATE_FILE, index=False)

# ========================================================
#   SCRAPE (Day 22 wala reliability ke saath)
# ========================================================
def scrape_books():
    headers = {"User-Agent": "Mozilla/5.0 (Ethical Alert Bot)"}
    response = requests.get(URL, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    books = []
    for b in soup.select("article.product_pod"):
        title = b.select_one("h3 a")["title"]
        price = b.select_one("p.price_color").get_text()
        price = float(price.replace("£", "").replace("Â", "").strip())
        books.append({"Title": title, "Price": price})
    return books

# ========================================================
#   ALERT (abhi print/log, aage email)
# ========================================================
# ========================================================
#   ALERT (Email ke saath!)
# ========================================================
def send_alert(new_books):
    # Pehle console/log mein dikhao
    logging.info("🔔 ALERT! Nayi books mili:")
    for b in new_books:
        logging.info(f"   📖 {b['Title']} — £{b['Price']}")

    # Agar email bhejni hai
    if not SEND_EMAIL:
        return

    # --- Email body banao (nayi books ki list) ---
    body = "🔔 ALERT! Ye nayi books mili:\n\n"
    for b in new_books:
        body += f"📖 {b['Title']} — £{b['Price']}\n"
    body += f"\nTotal: {len(new_books)} nayi books!"

    # --- Email bhejo (Day 13 wala code) ---
    try:
        import smtplib
        from email.mime.text import MIMEText

        # App Password runtime par lo (file mein save NAHI hoga)
        app_password = input("🔑 Gmail App Password daalo: ")

        msg = MIMEText(body)
        msg["Subject"] = f"🔔 {len(new_books)} Nayi Books Mili!"
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, app_password)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()

        logging.info("✅ Email successfully bhej di gayi!")

    except Exception as e:
        logging.error(f"❌ Email bhejne mein error: {e}")

# ========================================================
#   MAIN LOGIC
# ========================================================
def main():
    logging.info("🔔 ALERT SCRAPER STARTED")

    # Step 1: Pehle kya dekha tha?
    seen_before = load_seen()
    logging.info(f"Pehle se {len(seen_before)} books seen")

    # Step 2: Abhi kya hai?
    current = scrape_books()
    logging.info(f"Abhi {len(current)} books scrape hui")

    # Step 3: NEW = jo pehle nahi dekhi
    new_books = [b for b in current if b["Title"] not in seen_before]

    # Step 4: Alert sirf nayi ke liye
    if new_books:
        logging.info(f"🎉 {len(new_books)} NEW books mili!")
        send_alert(new_books)
    else:
        logging.info("😴 Koi nayi book nahi (sab pehle dekh chuke)")

    # Step 5: State update karo (sab yaad kar lo)
    all_seen = seen_before | {b["Title"] for b in current}
    save_seen(all_seen)
    logging.info(f"State updated: {len(all_seen)} total seen")

if __name__ == "__main__":
    main()