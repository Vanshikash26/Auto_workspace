import requests

# BotFather se mila token aur Chat ID (input se lo - safe!)
BOT_TOKEN = input("🔑 Bot Token paste karo: ")
CHAT_ID = input("💬 Apna Chat ID paste karo: ")

def send_message(text):
    """Telegram par message bhejne ka function"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    response = requests.post(url, data=data)
    return response.json()

# Pehla message bhejo
result = send_message("🎉 Hello! Mera pehla Telegram Bot kaam kar raha hai!")

if result.get("ok"):
    print("✅ Message bhej diya! Telegram check karo!")
else:
    print(f"❌ Error: {result}")
    