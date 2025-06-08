# main.py - FastAPI backend for KillMySub

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from uuid import uuid4

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Subscription(BaseModel):
    id: str
    service: str
    tier: str
    next_charge: str
    payment_method: str
    status: str = "active"

# In-memory fake DB
subs_db: List[Subscription] = []

@app.get("/api/subscriptions", response_model=List[Subscription])
def get_subs():
    return subs_db

@app.post("/api/subscriptions/{sub_id}/cancel")
def cancel_sub(sub_id: str):
    for sub in subs_db:
        if sub.id == sub_id:
            sub.status = "cancel_requested"
            return {"message": f"{sub.service} cancel initiated."}
    raise HTTPException(status_code=404, detail="Subscription not found")

@app.post("/api/subscriptions")
def add_fake_sub():
    new_sub = Subscription(
        id=str(uuid4()),
        service="Netflix",
        tier="Standard",
        next_charge="2025-06-15",
        payment_method="Visa **** 4242"
    )
    subs_db.append(new_sub)
    return new_sub
