from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Transaction(BaseModel):
    transaction_id: str
    customer_id: str
    date: str
    merchant: str
    amount: float
    category: str
    transaction_type: str
    payment_method: str
    card_number: Optional[str] = None
    account_details: Optional[str] = None
    location: str
    is_fraudulent: bool = False

class DisputeRequest(BaseModel):
    customer_id: str
    transaction_id: str
    reason: str
    description: str
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None

class DisputeResponse(BaseModel):
    dispute_id: str
    transaction_id: str
    customer_id: str
    status: str
    created_at: str
    estimated_resolution_time: str
    next_steps: List[str]
    reference_number: str
    ai_assessment: str