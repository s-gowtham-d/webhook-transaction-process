from celery import Celery
from datetime import datetime
import time
from app.database import SessionLocal
from app import models
from app.config import REDIS_URL

celery = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

@celery.task
def process_transaction(transaction_id: str):
    """Simulate delayed transaction processing"""
    print(f"Processing transaction {transaction_id}...")
    time.sleep(30)
    db = SessionLocal()
    try:
        txn = db.query(models.Transaction).filter_by(transaction_id=transaction_id).first()
        if txn:
            txn.status = "PROCESSED"
            txn.processed_at = datetime.utcnow()
            db.commit()
    finally:
        print(f"Finished processing transaction {transaction_id}.")
        db.close()
