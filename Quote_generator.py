import requests

def get_random_quote():
    """Ek random quote nikalo"""
    url = "https://dummyjson.com/quotes/random"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data["quote"], data["author"]

def save_quote(quote, author):
    """Quote ko file mein save karo"""
    with open("quotes.txt", "a", encoding="utf-8") as file:
        file.write(f'"{quote}" - {author}\n')

# ---------- MAIN ----------
def main():
    print("💬 RANDOM QUOTE GENERATOR\n")

    try:
        quote, author = get_random_quote()

        print(f'"{quote}"')
        print(f"   ✍️  — {author}\n")

        # Save karne ka option
        choice = input("💾 File mein save karna hai? (y/n): ")
        if choice.lower() == "y":
            save_quote(quote, author)
            print("✅ quotes.txt mein save ho gaya!")

    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")

if __name__ == "__main__":
    main()