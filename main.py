from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB", "killmysub")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "subscriptions")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

# Initialize FastAPI app
app = FastAPI()

# Setup MongoDB client
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

class ScanRequest(BaseModel):
    email: str
    phone: str

@app.post("/scan")
async def scan(request: ScanRequest):
    try:
        data = {
            "email": request.email,
            "phone": request.phone,
            "timestamp": datetime.utcnow().isoformat()
        }

        # Save to MongoDB
        collection.insert_one(data)

        # Send Discord webhook
        if DISCORD_WEBHOOK:
            requests.post(DISCORD_WEBHOOK, json=data)

        return {"status": "success", "message": "Data saved and webhook sent."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")