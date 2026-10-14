# db.py

"""Database utilities and ORM models for the PS05 Sales Assistant.
Uses SQLite via SQLModel (SQLAlchemy ORM).
"""

from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional, List
import os
import uuid

# SQLite database file
DB_PATH = os.path.join(os.path.dirname(__file__), "sales_assistant.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

# ---------- ORM models ----------

class Product(SQLModel, table=True):
    id: str = Field(primary_key=True)
    description: str
    price: float
    stock: int

class CartItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sender_id: str
    product_id: str
    quantity: int

class EventRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    message_id: str = Field(index=True, unique=True)
    sender_id: str
    timestamp: str
    text: str

class ConversationState(SQLModel, table=True):
    sender_id: str = Field(primary_key=True)
    # Store a JSON string representing the cart (list of dicts)
    cart_json: str = "[]"

# ---------- Helper functions ----------

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine)

def is_duplicate(message_id: str) -> bool:
    with get_session() as session:
        stmt = select(EventRecord).where(EventRecord.message_id == message_id)
        return session.exec(stmt).first() is not None

def save_event(event):
    from models import WebhookEvent
    rec = EventRecord(
        message_id=event.message_id,
        sender_id=event.sender_id,
        timestamp=event.timestamp,
        text=event.text,
    )
    with get_session() as session:
        session.add(rec)
        session.commit()

def get_state(sender_id: str):
    from utils import deserialize_cart, serialize_cart
    with get_session() as session:
        state = session.get(ConversationState, sender_id)
        if not state:
            state = ConversationState(sender_id=sender_id)
            session.add(state)
            session.commit()
        # Convert cart_json to Python list
        state.cart = deserialize_cart(state.cart_json)
        return state

def save_state(state):
    from utils import serialize_cart
    with get_session() as session:
        db_state = session.get(ConversationState, state.sender_id)
        if db_state:
            db_state.cart_json = serialize_cart(state.cart)
            session.add(db_state)
            session.commit()
