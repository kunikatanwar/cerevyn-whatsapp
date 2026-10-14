📦 Cerevyn WhatsApp Sales & Quotation Assistant
Problem Statement (PS05)
Build a WhatsApp‑style assistant that understands product enquiries, collects quantities and prepares a quotation from a fixed catalogue. The solution is demonstrated via a local webhook simulator (FastAPI) and includes a full CI pipeline, tests, and an Azure deployment plan.

Table of Contents
Features
Tech Stack
Repository Layout
Setup & Installation
Running the Application
Running Tests
Demo Walk‑through
Azure Deployment Plan
Contributing
Features
Natural‑language product enquiry detection (lightweight keyword / spaCy model).
Per‑sender cart – each simulated WhatsApp user gets an isolated cart.
Stock validation – prevents quoting unavailable quantities.
Tax & total calculation (configurable tax rate).
Quotation confirmation – only after explicit user confirmation is an enquiry ID generated.
Human hand‑off for unsupported intents – returns the conversation context.
Idempotent webhook – repeated message_id values are ignored.
Persistent storage – SQLite stores catalogue, carts, quotations and conversation history.
Dockerised – ready for local dev and Azure App Service.
GitHub Actions CI – lint, unit tests and Docker build.
Tech Stack
Python 3.11
FastAPI – webhook & HTTP API
SQLModel (SQLAlchemy + Pydantic) – SQLite ORM
spaCy (or simple regex) for intent/entity extraction (no paid LLM).
Docker – container runtime
GitHub Actions – CI/CD pipeline
Azure – optional deployment (App Service + Azure Storage)
Repository Layout
text

cerevyn-whatsapp-sales-assistant/
├─ .github/workflows/ci.yml          # GitHub Actions CI
├─ docs/azure-plan.md               # Azure deployment design
├─ src/
│   ├─ main.py                      # FastAPI entry point
│   ├─ models.py                    # DB models (Product, Cart, Quotation, MessageLog)
│   ├─ db.py                        # SQLite engine & session helper
│   ├─ catalogue.py                 # Load static catalogue JSON
│   ├─ intent.py                    # Simple intent / entity extraction
│   ├─ quotation.py                 # Cart & quotation business logic
│   └─ webhook.py                   # `/webhook` endpoint (WhatsApp‑style simulator)
├─ tests/
│   ├─ test_intent.py
│   ├─ test_quotation.py
│   └─ test_webhook.py
├─ catalogue.json                    # 10+ product definitions
├─ sample_events/                    # Example webhook payloads (JSON)
│   ├─ user1_enquiry.json
│   └─ user2_duplicate.json
├─ requirements.txt                  # Python dependencies
├─ .env.example                      # Example environment variables
└─ README.md                         # This file
Setup & Installation
Clone the repo
bash

git clone <repo-url>
cd cerevyn-whatsapp-sales-assistant
Create a virtual environment & install dependencies
bash

python -m venv .venv
.venv\Scripts\activate   # Windows PowerShell
pip install -r requirements.txt
Load the catalogue – the JSON file is read automatically on startup.
Configure environment – copy the example file:
bash

copy .env.example .env
The default SQLite DB file will be data/app.db.
Running the Application
bash

uvicorn src.main:app --reload
The webhook endpoint is available at http://127.0.0.1:8000/webhook. Simulate messages with curl or the JSON files in sample_events/:

bash

curl -X POST http://127.0.0.1:8000/webhook \
     -H "Content-Type: application/json" \
     -d @sample_events/user1_enquiry.json
The response JSON contains the outgoing message text that would be sent back to the user.

Running Tests
bash

pytest -q
All tests should pass. The CI workflow runs the same command.

Demo Walk‑through
User asks for a product – bot extracts the product ID.
Bot asks for quantity if missing.
User provides quantity – bot validates stock, adds to cart.
User adds another product – repeat steps.
User confirms – bot returns a formatted quotation with line totals, tax, and grand total, plus a unique enquiry ID.
Unsupported request – bot replies with a hand‑off message containing the conversation context.
Duplicate message_id – webhook silently ignores the payload.
Two independent users – each maintains its own cart.
Azure Deployment Plan
See 
docs/azure-plan.md
 for a full architecture, resource choices, CI/CD integration and cost‑control notes.

Contributing
Fork the repository and submit pull requests. Keep the code style consistent (use ruff/black), add unit tests for new features, and update documentation as needed.

The repository follows the Cerevyn assessment guidelines. No real credentials or paid APIs are used.

