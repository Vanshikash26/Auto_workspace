import requests
from bs4 import BeautifulSoup

# ---------- 1. QUOTES SCRAPER ----------
print("💬 QUOTES SCRAPING...\n")
url = "https://quotes.toscrape.com"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Har quote ka block (div class="quote") dhundo
quote_blocks = soup.find_all("div", class_="quote")

for block in quote_blocks:
    text = block.find("span", class_="text").get_text()
    author = block.find("small", class_="author").get_text()
    print(f"💬 {text}")
    print(f"   ✍️ - {author}\n")


# ---------- 2. BOOK TITLES SCRAPER ----------
print("\n📖 BOOK TITLES SCRAPING...\n")
url2 = "https://books.toscrape.com"
response2 = requests.get(url2)
soup2 = BeautifulSoup(response2.text, "html.parser")

# Pehle 10 books (article class="product_pod")
books = soup2.find_all("article", class_="product_pod")[:10]

for book in books:
    title = book.find("h3").find("a").get("title")
    price = book.find("p", class_="price_color").get_text()
    print(f"📖 {title}")
    print(f"   💰 {price}\n")