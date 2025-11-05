# 🚀 Webhook Transaction Processing Service

A production-ready **FastAPI** service that receives and processes transaction webhooks asynchronously with **Celery** and **Redis**, storing results in **PostgreSQL**.

**Live API:** [https://webhook.gowtham.work](https://webhook.gowtham.work)

This project demonstrates:

- ⚡ Fast API response times (<500ms)
- 🔄 Asynchronous background processing using a task queue
- 🔐 Idempotent transaction handling
- 💾 Reliable data persistence and API querying
- 🐳 Dockerized deployment for local and cloud environments

---

## 🧩 Architecture Overview

```
      ┌────────────────────┐
      │    Webhook API     │   ← FastAPI (Receives transaction)
      │    (Port 8000)     │      POST /v1/webhooks/transactions
      └─────────┬──────────┘
                │
                ▼ (Enqueue Task)
      ┌────────────────────┐
      │ Redis Message Queue│   ← Celery Broker
      │    (Port 6379)     │
      └─────────┬──────────┘
                │
                ▼ (Process Task)
      ┌────────────────────┐
      │ Celery Worker      │   ← Processes transaction after 30s delay
      │  (Background)      │
      └─────────┬──────────┘
                │
                ▼ (Store Result)
      ┌────────────────────┐
      │ PostgreSQL DB      │   ← Stores transaction records
      │    (Port 5432)     │
      └────────────────────┘
```

---

## ⚙️ Tech Stack

| Component          | Purpose                    | Version |
| ------------------ | -------------------------- | ------- |
| **FastAPI**        | REST API Framework         | 0.104+  |
| **SQLAlchemy**     | ORM for PostgreSQL         | 2.0+    |
| **Celery**         | Background task processing | 5.3+    |
| **Redis**          | Message broker for Celery  | 7.x     |
| **PostgreSQL**     | Data persistence           | 15.x    |
| **Docker Compose** | Container orchestration    | 3.9+    |
| **Uvicorn**        | ASGI server                | 0.24+   |

---

## 🧠 Features

✅ **Fast Response**: Returns `202 Accepted` within 500ms  
✅ **Async Processing**: Background task processing with 30s simulated delay  
✅ **Idempotency**: Duplicate transaction IDs are handled gracefully  
✅ **Transaction Tracking**: Query transaction status at any time  
✅ **Health Check**: Monitor service availability  
✅ **Production Ready**: Containerized with Docker Compose  
✅ **Database Persistence**: ACID-compliant PostgreSQL storage

---

## 📁 Project Structure

```
service/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application & routes
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── database.py          # Database engine & session
│   └── worker.py            # Celery worker configuration
├── tests/                   # Test files (optional)
├── .env                     # Environment variables
├── .env.example             # Example environment file
├── docker-compose.yml       # Docker orchestration
├── Dockerfile               # Container build instructions
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## 🚀 Quick Start

### Prerequisites

- **Docker** 20.10+ and **Docker Compose** 2.x
- **Python** 3.11+ (for local development without Docker)
- **Git**

### Option 1: Run with Docker (Recommended)

#### 1️⃣ Clone the repository

```bash
git clone https://github.com/s-gowtham-d/confluencr-assessment.git
cd confluencr-assessment/service
```

#### 2️⃣ Create `.env` file

**Example `.env` file:**

```env
# PostgreSQL Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=transactions_db

# Database URL for SQLAlchemy
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/transactions_db

# Redis URL for Celery
REDIS_URL=redis://redis:6379/0
```

#### 3️⃣ Start all services

```bash
# Build and start all containers
docker compose up -d

# Check if all services are running
docker compose ps
```

This starts:

- **FastAPI API** → http://localhost:8000
- **PostgreSQL DB** → localhost:5432
- **Redis Broker** → localhost:6379
- **Celery Worker** → Background process

#### 4️⃣ Verify services are running

```bash
# Check API health
curl http://localhost:8000/

# View logs
docker compose logs -f

# View specific service logs
docker compose logs -f api
docker compose logs -f worker
```

#### 5️⃣ Stop services

```bash
# Stop all containers
docker compose down

# Stop and remove volumes (deletes database data)
docker compose down -v
```

---

### Option 2: Run Locally (Without Docker)

#### 1️⃣ Install dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

#### 2️⃣ Start PostgreSQL and Redis

```bash
# Using Docker for dependencies only
docker run -d --name postgres -p 5432:5432 \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=transactions_db \
  postgres:15

docker run -d --name redis -p 6379:6379 redis:7
```

#### 3️⃣ Create `.env` file

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/transactions_db
REDIS_URL=redis://localhost:6379/0
```

#### 4️⃣ Start FastAPI server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 5️⃣ Start Celery worker (in another terminal)

```bash
source venv/bin/activate
celery -A app.worker.celery worker --loglevel=info
```

---

## 🧰 API Reference

### 🔹 Health Check

**Endpoint:** `GET /`

Check if the service is running.

```bash
curl http://localhost:8000/
```

**Response:**

```json
{
  "status": "HEALTHY",
  "current_time": "2025-10-29T10:30:00Z"
}
```

---

### 🔹 Receive Webhook

**Endpoint:** `POST /v1/webhooks/transactions`

Accepts transaction webhooks and queues them for processing.

**Request Body:**

```json
{
  "transaction_id": "txn_abc123def456",
  "source_account": "acc_user_789",
  "destination_account": "acc_merchant_456",
  "amount": 1500.5,
  "currency": "INR"
}
```

**Example Request:**

```bash
curl -X POST http://localhost:8000/v1/webhooks/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "txn_abc123def456",
    "source_account": "acc_user_789",
    "destination_account": "acc_merchant_456",
    "amount": 1500.50,
    "currency": "INR"
  }'
```

**Response:** `202 Accepted`

```json
{
  "status": "ACCEPTED",
  "message": "Transaction queued for processing"
}
```

**Notes:**

- Response time: <500ms
- Transaction will be processed after ~30 seconds
- Duplicate `transaction_id` will be ignored (idempotent)

---

### 🔹 Get Transaction Status

**Endpoint:** `GET /v1/transactions/{transaction_id}`

Retrieve the status of a transaction.

```bash
curl http://localhost:8000/v1/transactions/txn_abc123def456
```

**Response (Processing):**

```json
{
  "transaction_id": "txn_abc123def456",
  "source_account": "acc_user_789",
  "destination_account": "acc_merchant_456",
  "amount": 1500.5,
  "currency": "INR",
  "status": "PROCESSING",
  "created_at": "2025-10-29T10:30:00Z",
  "processed_at": null
}
```

**Response (Processed):**

```json
{
  "transaction_id": "txn_abc123def456",
  "source_account": "acc_user_789",
  "destination_account": "acc_merchant_456",
  "amount": 1500.5,
  "currency": "INR",
  "status": "PROCESSED",
  "created_at": "2025-10-29T10:30:00Z",
  "processed_at": "2025-10-29T10:30:30Z"
}
```

**Response (Not Found):** `404`

```json
{
  "detail": "Transaction not found"
}
```

---
