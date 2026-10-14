# app.py

"""FastAPI entry point for the WhatsApp Sales and Quotation Assistant (PS05)."""

from fastapi import FastAPI
from pydantic import BaseModel
from sqlmodel import Session, select
import uuid

import db, models, intent, utils

app = FastAPI()

@app.post("/webhook")
async def webhook(event: models.WebhookEvent):
    # Duplicate detection
    if db.is_duplicate(event.message_id):
        return {"status": "duplicate"}
    # Store raw event
    db.save_event(event)
    # Retrieve or create conversation state for the sender
    state = db.get_state(event.sender_id)
    # Process the incoming text
    response_text = intent.process(event.text, state)
    # Persist any state changes (e.g., cart updates)
    db.save_state(state)
    return {"reply": response_text}
