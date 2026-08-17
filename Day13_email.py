'''import pandas as pd

# ---------- Sales data ----------
sales = pd.DataFrame({
    "Region": ["North", "South", "North", "South", "North", "South"],
    "Product": ["Laptop", "Phone", "Phone", "Laptop", "Tablet", "Tablet"],
    "Amount": [50000, 20000, 22000, 55000, 15000, 16000],
})
print("Sales data:")
print(sales)

# ---------- 1. groupby: region-wise total ----------
region_total = sales.groupby("Region")["Amount"].sum()
print("\nRegion-wise total:")
print(region_total)

# ---------- 2. merge: do tables jodo ----------
products = pd.DataFrame({
    "Product": ["Laptop", "Phone", "Tablet"],
    "Category": ["Electronics", "Mobile", "Electronics"],
})
merged = sales.merge(products, on="Product")
print("\nMerged (sales + category):")
print(merged)

# ---------- 3. fillna: missing values bharo ----------
messy = pd.DataFrame({"Name": ["A", "B", None], "Marks": [10, None, 30]})
clean = messy.fillna(0)
print("\nMissing values bhari (fillna 0):")
print(clean)

# ---------- 4. to_excel: Excel export ----------
merged.to_excel("sales_report.xlsx", index=False)
print("\n✅ sales_report.xlsx ban gayi!")'''



# main work 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Runtime par input lo (kahin save NAHI hota)
sender = input("Apna Gmail: ")
app_password = input("App Password: ")
receiver = input("Kisko bhejna hai: ")

msg = MIMEMultipart()
msg["From"] = sender
msg["To"] = receiver
msg["Subject"] = "Test from Python! 🐍"
msg.attach(MIMEText("Hello! Ye email Python ne bheji hai. 🎉", "plain"))

# Attachment (sales_report.xlsx) ---> tdqk bybp ocsn vqru
with open("sales_report.xlsx", "rb") as f:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(f.read())
encoders.encode_base64(part)
part.add_header("Content-Disposition", "attachment; filename=sales_report.xlsx")
msg.attach(part)

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, app_password)
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()
    print("✅ Email bhej di with attachment!")
except Exception as e:
    print(f"❌ Error: {e}")
    