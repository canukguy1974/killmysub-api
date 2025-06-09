from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import requests
import datetime

# Load environment variables
load_dotenv()

# MongoDB Setup
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB", "killmysub")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "subscriptions")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

# FastAPI app
app = FastAPI()

# Pydantic input model
class ScanRequest(BaseModel):
    email: str
    phone: str

@app.get("/")
def root():
    return {"message": "KillMySub API is alive."}

@app.post("/scan")
async def scan(request: ScanRequest):
    try:
        data = {
            "email": request.email,
            "phone": request.phone,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

        # Insert into MongoDB — do NOT try to return this result directly
        collection.insert_one(data)

        # Send to Discord webhook
        if DISCORD_WEBHOOK:
            requests.post(DISCORD_WEBHOOK, json=data)

        return {"status": "success", "message": "Data saved and webhook sent."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

