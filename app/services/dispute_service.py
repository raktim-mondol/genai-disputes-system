import json
import uuid
from datetime import datetime, timedelta
import os
import logging
from app.services.openai_service import OpenAIService
from app.config import Config

logger = logging.getLogger(__name__)

class DisputeService:
    def __init__(self):
        self.openai_service = OpenAIService()
        self.transactions = self._load_transactions()
        self.disputes = {}  # In-memory storage for disputes (would be a database in production)
        
    def _load_transactions(self):
        """Load transactions from the data file."""
        try:
            with open(Config.DATA_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading transactions: {str(e)}")
            return []
    
    def get_customer_transactions(self, customer_id):
        """Get all transactions for a specific customer."""
        return [t for t in self.transactions if t['customer_id'] == customer_id]
    
    def get_transaction(self, transaction_id):
        """Get a specific transaction by ID."""
        for transaction in self.transactions:
            if transaction['transaction_id'] == transaction_id:
                return transaction
        return None
    
    def create_dispute(self, dispute_request):
        """Create a new dispute for a transaction."""
        # Get the transaction
        transaction = self.get_transaction(dispute_request.transaction_id)
        if not transaction:
            return {"error": "Transaction not found"}
        
        # Check if transaction belongs to customer
        if transaction['customer_id'] != dispute_request.customer_id:
            return {"error": "Transaction does not belong to this customer"}
        
        # Check if transaction is within dispute time limit
        transaction_date = datetime.strptime(transaction['date'], "%Y-%m-%d %H:%M:%S")
        days_since_transaction = (datetime.now() - transaction_date).days
        if days_since_transaction > Config.DISPUTE_TIME_LIMIT_DAYS:
            return {
                "error": f"Transaction is outside the {Config.DISPUTE_TIME_LIMIT_DAYS}-day dispute window",
                "days_since_transaction": days_since_transaction
            }
        
        # Check if amount is within limits
        if transaction['amount'] > Config.MAX_DISPUTE_AMOUNT:
            return {
                "error": f"Transaction amount exceeds maximum dispute limit of ${Config.MAX_DISPUTE_AMOUNT}",
                "transaction_amount": transaction['amount']
            }
        
        # Use OpenAI to analyze the dispute
        ai_analysis = self.openai_service.analyze_dispute(transaction, dispute_request)
        
        # Create dispute record
        dispute_id = str(uuid.uuid4())
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Determine estimated resolution time based on AI analysis
        if ai_analysis.get("fraud_likelihood") == "HIGH":
            estimated_days = 5
        elif ai_analysis.get("fraud_likelihood") == "MEDIUM":
            estimated_days = 10
        else:
            estimated_days = 21
            
        estimated_resolution = (datetime.now() + timedelta(days=estimated_days)).strftime("%Y-%m-%d")
        
        # Generate reference number
        reference_number = f"DSP-{dispute_id[:8].upper()}"
        
        # Create dispute record
        dispute = {
            "dispute_id": dispute_id,
            "transaction_id": dispute_request.transaction_id,
            "customer_id": dispute_request.customer_id,
            "reason": dispute_request.reason,
            "description": dispute_request.description,
            "contact_phone": dispute_request.contact_phone,
            "contact_email": dispute_request.contact_email,
            "status": "UNDER_REVIEW",
            "created_at": created_at,
            "estimated_resolution_time": estimated_resolution,
            "reference_number": reference_number,
            "ai_analysis": ai_analysis
        }
        
        # Store dispute
        self.disputes[dispute_id] = dispute
        
        # Return response
        return {
            "dispute_id": dispute_id,
            "transaction_id": dispute_request.transaction_id,
            "customer_id": dispute_request.customer_id,
            "status": "UNDER_REVIEW",
            "created_at": created_at,
            "estimated_resolution_time": estimated_resolution,
            "next_steps": ai_analysis.get("recommended_actions", ["Your dispute is being reviewed"]),
            "reference_number": reference_number,
            "ai_assessment": ai_analysis.get("analysis", "Analysis in progress")
        }
    
    def get_dispute(self, dispute_id):
        """Get a specific dispute by ID."""
        return self.disputes.get(dispute_id)
    
    def get_customer_disputes(self, customer_id):
        """Get all disputes for a specific customer."""
        return [d for d in self.disputes.values() if d['customer_id'] == customer_id]