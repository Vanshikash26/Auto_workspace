import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://books.toscrape.com"
response = requests.get(url)
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "html.parser")

# CSS selector se saare book blocks dhundo
books = soup.select("article.product_pod")

all_books = []
for book in books:
    # Title (h3 ke andar wale <a> tag ka 'title' attribute)
    title = book.select_one("h3 a")["title"]

    # Price nikalo aur CLEAN karo (£ hatao, float banao)
    price_text = book.select_one("p.price_color").get_text()
    price = float(price_text.replace("£", "").replace("Â", "").strip())

    # Rating (class se - dusri class mein rating hoti hai)
    rating = book.select_one("p.star-rating")["class"][1]

    # Availability (faltu spaces hatao)
    availability = book.select_one("p.instock.availability").get_text().strip()

    # Sab ko ek dict mein jodo
    all_books.append({
        "Title": title,
        "Price": price,
        "Rating": rating,
        "Availability": availability,
    })

print(f"✅ {len(all_books)} books scrape ho gayi!\n")
print("Pehli 3 books:")
for b in all_books[:3]:
    print(f"📖 {b['Title']} | £{b['Price']} | {b['Rating']} | {b['Availability']}")

# CSV mein export karo (pandas se)
df = pd.DataFrame(all_books)
df.to_csv("books.csv", index=False)
print("\n✅ books.csv ban gayi! Excel/Sheets mein khol kar dekho.")