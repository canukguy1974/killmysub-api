import os
from pymongo import MongoClient
from twilio.rest import Client
from datetime import datetime

# Load env vars
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_FROM_NUMBER")

# Setup clients
mongo = MongoClient(MONGO_URI)
db = mongo[MONGO_DB]
collection = db[MONGO_COLLECTION]

twilio = Client(TWILIO_SID, TWILIO_TOKEN)

# Pull all users from DB
users = collection.find()

for user in users:
    email = user.get("email")
    phone = user.get("phone")
    subscriptions = user.get("subscriptions", [])

    if not phone or not subscriptions:
        continue

    # Format message
    msg_lines = [f"KillMySub Daily Report ({datetime.utcnow().strftime('%b %d')}):"]
    for sub in subscriptions:
        name = sub.get("name", "Unknown Service")
        price = sub.get("price", "N/A")
        msg_lines.append(f"🔸 {name} - {price}")

    msg_lines.append("\nWe'll warn you 2 days before any charges 💣")

    message_body = "\n".join(msg_lines)

    try:
        twilio.messages.create(
            body=message_body,
            from_=TWILIO_FROM,
            to=phone
        )
        print(f"✅ Sent summary to {email} ({phone})")
    except Exception as e:
        print(f"❌ Failed to send SMS to {email}: {e}")
