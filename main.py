# main.py - FastAPI backend for KillMySub

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
import os
import requests
from datetime import datetime  # ✅ This was missing

app = FastAPI()

# Middleware (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Setup
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

# Request Body Model
class SubscriptionRequest(BaseModel):
    email: str
    phone: str

# Helper to convert ObjectId and datetime to JSON-serializable types
def serialize_subscription(subscription):
    subscription["_id"] = str(subscription["_id"])
    if isinstance(subscription.get("next_charge"), datetime):
        subscription["next_charge"] = subscription["next_charge"].isoformat()
    return subscription

@app.post("/scan")
async def scan_subscriptions(data: SubscriptionRequest):
    try:
        # Save to DB
        subscription_data = {
            "email": data.email,
            "phone": data.phone,
            "timestamp": datetime.utcnow()
        }
        result = collection.insert_one(subscription_data)

        # Send to Discord webhook
        requests.post(DISCORD_WEBHOOK, json={
            "content": f"🔔 New Scan\n📧 Email: {data.email}\n📱 Phone: {data.phone}\n🕒 {subscription_data['timestamp']}"
        })

        return {"message": "Subscription data saved successfully", "id": str(result.inserted_id)}
    except Exception as e:
        return {"detail": f"Error: {e}"}

@app.get("/")
def root():
    return {"message": "KillMySub API is live"}
