def send_email_alert(new_jobs):
    """Nayi jobs ki email alert bhejo"""
    import config

    if not config.SEND_EMAIL:
        return

    try:
        import smtplib
        from email.mime.text import MIMEText

        # Email body banao
        body = f"🎯 InternShip Radar: {len(new_jobs)} NAYI jobs mili!\n\n"
        for i, job in enumerate(new_jobs, 1):
            body += f"{i}. {job['title']} @ {job['company']}\n"
            body += f"   📊 Match Score: {job['total']}\n"
            body += f"   🔗 Apply: {job.get('url', 'N/A')}\n\n"
        body += "— InternShip Radar 🤖"

        # App Password runtime par lo (security!)
        app_password = input("🔑 Gmail App Password daalo: ")

        msg = MIMEText(body)
        msg["Subject"] = f"🎯 {len(new_jobs)} Nayi Jobs Mili! - InternShip Radar"
        msg["From"] = config.SENDER_EMAIL
        msg["To"] = config.RECEIVER_EMAIL

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(config.SENDER_EMAIL, app_password)
        server.sendmail(config.SENDER_EMAIL, config.RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("✅ Email alert bhej diya!")

    except Exception as e:
        print(f"❌ Email error: {e}")