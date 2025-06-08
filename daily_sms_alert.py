import os
from datetime import datetime, timedelta
from pymongo import MongoClient
from dotenv import load_dotenv
from twilio.rest import Client

# Load .env
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_FROM = os.getenv("TWILIO_FROM")

# Init clients
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]
twilio_client = Client(TWILIO_SID, TWILIO_AUTH)

# Dates
today = datetime.now().date()
tomorrow = today + timedelta(days=1)

# Scan subs
count = 0
for sub in collection.find():
    next_charge = sub.get("next_charge")
    phone = sub.get("phone")
    if not next_charge or not phone:
        continue

    try:
        charge_date = datetime.strptime(next_charge, "%Y-%m-%d").date()
        if today <= charge_date <= tomorrow:
            msg = f"⚠️ Reminder: Your {sub['service']} subscription is scheduled to charge on {next_charge}."
            twilio_client.messages.create(
                body=msg,
                from_=TWILIO_FROM,
                to=phone
            )
            print(f"[+] Sent to {phone}: {msg}")
            count += 1
    except:
        continue

print(f"[✓] Done. {count} alerts sent.")
