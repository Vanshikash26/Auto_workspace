import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

print("🚀 Multi-Page Quotes Scraper Started...\n")

all_quotes = []
base_url = "https://quotes.toscrape.com/page/"

# 10 pages hain (page/1/ se page/10/ tak)
for page_num in range(1, 11):
    url = f"{base_url}{page_num}/"
    print(f"📄 Scraping page {page_num}/10...")
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    quotes = soup.select("div.quote")
    for quote in quotes:
        text = quote.select_one("span.text").get_text()
        author = quote.select_one("small.author").get_text()
        all_quotes.append({"Quote": text, "Author": author})
    
    # Politeness: Random delay (1-3 seconds)
    delay = random.uniform(1, 3)
    print(f"   ✅ {len(quotes)} quotes mile. Waiting {delay:.1f}s...\n")
    time.sleep(delay)

print(f"\n🎉 Total {len(all_quotes)} quotes scrape ho gaye!")

# CSV export
df = pd.DataFrame(all_quotes)
df.to_csv("all_quotes.csv", index=False)
print("✅ all_quotes.csv ban gayi!")


print("\n\n🚀 ALL BOOKS SCRAPER (50 PAGES)...\n")

all_books = []
base_url = "https://books.toscrape.com/catalogue/page-"

# 50 pages hain (page-1.html se page-50.html tak)
for page_num in range(1, 51):
    url = f"{base_url}{page_num}.html"
    print(f"📖 Scraping page {page_num}/50...", end=" ")
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    books = soup.select("article.product_pod")
    for book in books:
        title = book.select_one("h3 a")["title"]
        price_text = book.select_one("p.price_color").get_text()
        price = float(price_text.replace("£", "").replace("Â", "").strip())
        all_books.append({"Title": title, "Price": price})
    
    print(f"✅ {len(books)} books")
    
    # Politeness: Fixed 1 second delay
    time.sleep(1)

print(f"\n🎉 Total {len(all_books)} books scrape ho gaye!")

# CSV export
df_books = pd.DataFrame(all_books)
df_books.to_csv("all_books.csv", index=False)
print("✅ all_books.csv ban gayi!")