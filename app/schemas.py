from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransactionCreate(BaseModel):
    transaction_id: str
    source_account: str
    destination_account: str
    amount: float
    currency: str

class TransactionResponse(TransactionCreate):
    status: str
    created_at: datetime
    processed_at: Optional[datetime]
