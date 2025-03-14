import unittest
import json
import os
from unittest.mock import patch, MagicMock
from app.services.dispute_service import DisputeService
from app.models.transaction import DisputeRequest

class TestDisputeService(unittest.TestCase):
    
    def setUp(self):
        # Create a mock for the OpenAI service
        self.openai_patcher = patch('app.services.dispute_service.OpenAIService')
        self.mock_openai = self.openai_patcher.start()
        
        # Mock the analyze_dispute method
        self.mock_openai.return_value.analyze_dispute.return_value = {
            "analysis": "This appears to be a fraudulent transaction",
            "fraud_likelihood": "HIGH",
            "recommended_actions": ["Block card", "Contact customer"]
        }
        
        # Create test transactions
        self.test_transactions = [
            {
                "transaction_id": "test-transaction-1",
                "customer_id": "CUST000001",
                "date": "2023-01-01 12:00:00",
                "merchant": "Test Merchant",
                "amount": 100.0,
                "category": "Retail",
                "transaction_type": "PURCHASE",
                "payment_method": "CARD",
                "card_number": "4111 1111 1111 1111",
                "location": "Sydney, NSW",
                "is_fraudulent": True
            }
        ]
        
        # Create a temporary file with test transactions
        self.temp_file = "test_transactions.json"
        with open(self.temp_file, 'w') as f:
            json.dump(self.test_transactions, f)
        
        # Mock the Config.DATA_FILE to use our test file
        self.config_patcher = patch('app.services.dispute_service.Config')
        self.mock_config = self.config_patcher.start()
        self.mock_config.DATA_FILE = self.temp_file
        self.mock_config.DISPUTE_TIME_LIMIT_DAYS = 60
        self.mock_config.MAX_DISPUTE_AMOUNT = 10000.0
        
        # Create the dispute service
        self.dispute_service = DisputeService()
        
    def tearDown(self):
        # Stop the patchers
        self.openai_patcher.stop()
        self.config_patcher.stop()
        
        # Remove the temporary file
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
    
    def test_get_customer_transactions(self):
        """Test getting transactions for a customer."""
        transactions = self.dispute_service.get_customer_transactions("CUST000001")
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]["transaction_id"], "test-transaction-1")
    
    def test_get_transaction(self):
        """Test getting a specific transaction."""
        transaction = self.dispute_service.get_transaction("test-transaction-1")
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction["merchant"], "Test Merchant")
    
    def test_create_dispute(self):
        """Test creating a dispute."""
        dispute_request = DisputeRequest(
            customer_id="CUST000001",
            transaction_id="test-transaction-1",
            reason="Unauthorized transaction",
            description="I did not make this purchase"
        )
        
        result = self.dispute_service.create_dispute(dispute_request)
        
        self.assertIn("dispute_id", result)
        self.assertEqual(result["transaction_id"], "test-transaction-1")
        self.assertEqual(result["status"], "UNDER_REVIEW")
        self.assertEqual(result["customer_id"], "CUST000001")
        
        # Check that the OpenAI service was called
        self.mock_openai.return_value.analyze_dispute.assert_called_once()
        
        # Check that the dispute was stored
        disputes = self.dispute_service.get_customer_disputes("CUST000001")
        self.assertEqual(len(disputes), 1)
        self.assertEqual(disputes[0]["transaction_id"], "test-transaction-1")

if __name__ == '__main__':
    unittest.main()