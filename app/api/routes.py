from fastapi import APIRouter, HTTPException, Depends, Header
from typing import List, Optional
from app.models.transaction import Transaction, DisputeRequest, DisputeResponse
from app.services.dispute_service import DisputeService
import logging

router = APIRouter()
dispute_service = DisputeService()
logger = logging.getLogger(__name__)

# Simple auth check (would be more robust in production)
def verify_customer(customer_id: str, x_customer_id: Optional[str] = Header(None)):
    if not x_customer_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    if x_customer_id != customer_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this resource")
    return customer_id

@router.get("/transactions/{customer_id}", response_model=List[Transaction])
async def get_customer_transactions(customer_id: str, _: str = Depends(verify_customer)):
    """Get all transactions for a customer."""
    transactions = dispute_service.get_customer_transactions(customer_id)
    return transactions

@router.get("/transactions/{customer_id}/{transaction_id}", response_model=Transaction)
async def get_transaction(customer_id: str, transaction_id: str, _: str = Depends(verify_customer)):
    """Get a specific transaction."""
    transaction = dispute_service.get_transaction(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    if transaction['customer_id'] != customer_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this transaction")
    return transaction

@router.post("/disputes", response_model=DisputeResponse)
async def create_dispute(dispute_request: DisputeRequest, _: str = Depends(verify_customer)):
    """Create a new dispute for a transaction."""
    result = dispute_service.create_dispute(dispute_request)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/disputes/{customer_id}", response_model=List[DisputeResponse])
async def get_customer_disputes(customer_id: str, _: str = Depends(verify_customer)):
    """Get all disputes for a customer."""
    disputes = dispute_service.get_customer_disputes(customer_id)
    return disputes

@router.get("/disputes/{customer_id}/{dispute_id}", response_model=DisputeResponse)
async def get_dispute(customer_id: str, dispute_id: str, _: str = Depends(verify_customer)):
    """Get a specific dispute."""
    dispute = dispute_service.get_dispute(dispute_id)
    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")
    if dispute['customer_id'] != customer_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this dispute")
    return dispute