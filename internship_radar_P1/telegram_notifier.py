import requests

def send_telegram_alert(bot_token, chat_id, new_jobs):
    """Nayi jobs ka alert Telegram par bhejo"""
    if not new_jobs:
        return
    
    # Message format karo (Plain text to avoid errors)
    message = f"🎯 InternShip Radar Alert!\n"
    message += f"Found {len(new_jobs)} NEW jobs matching your skills:\n\n"
    
    # Top 5 jobs dikhao (zyada lamba message Telegram reject kar deta hai)
    for i, job in enumerate(new_jobs[:5], 1): 
        message += f"{i}. {job['title']}\n"
        message += f"🏢 {job['company']} | {job['mode_label']} | {job['location']}\n"
        message += f"💰 {job['stipend']} | Score: {job['total']}\n"
        message += f"🔗 {job.get('url', 'No URL')}\n\n"
        
    if len(new_jobs) > 5:
        message += f"...and {len(new_jobs) - 5} more jobs in the Excel report."

    # Telegram API ko call karo
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    
    try:
        response = requests.post(url, data=data)
        if response.json().get("ok"):
            print("✅ Telegram alert sent to your phone!")
        else:
            print(f"❌ Telegram error: {response.json()}")
    except Exception as e:
        print(f"❌ Telegram network error: {e}")