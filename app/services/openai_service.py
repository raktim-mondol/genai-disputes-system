import openai
from app.config import Config
import logging
import json

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.api_key = Config.OPENAI_API_KEY
        self.model = Config.OPENAI_MODEL
        openai.api_key = self.api_key
        
    def analyze_dispute(self, transaction, dispute_request):
        """
        Analyze a dispute using OpenAI to determine likelihood of fraud and next steps.
        
        Args:
            transaction: The transaction being disputed
            dispute_request: The customer's dispute information
            
        Returns:
            dict: Analysis results including fraud likelihood and recommended actions
        """
        try:
            # Create a prompt for the AI
            prompt = self._create_dispute_analysis_prompt(transaction, dispute_request)
            
            # Call OpenAI API
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # Low temperature for more deterministic responses
                max_tokens=1000
            )
            
            # Extract and parse the response
            ai_response = response.choices[0].message.content
            
            try:
                # Try to parse as JSON
                return json.loads(ai_response)
            except json.JSONDecodeError:
                # If not valid JSON, return as text
                logger.warning("AI response was not valid JSON, returning as text")
                return {
                    "analysis": ai_response,
                    "fraud_likelihood": "UNKNOWN",
                    "recommended_actions": ["Manual review required"]
                }
                
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {str(e)}")
            return {
                "analysis": "Error analyzing dispute",
                "fraud_likelihood": "ERROR",
                "recommended_actions": ["System error, please try again or contact support"]
            }
    
    def _get_system_prompt(self):
        """Return the system prompt that guides the AI's behavior."""
        return """
        You are an AI assistant specialized in analyzing banking disputes for unauthorized transactions in Australia.
        Your role is to analyze transaction details and customer dispute information to:
        
        1. Assess the likelihood that the transaction was fraudulent
        2. Recommend appropriate next steps based on Australian banking regulations
        3. Provide a clear analysis that helps both the customer and bank staff
        
        Your response should be in JSON format with the following structure:
        {
            "analysis": "Detailed analysis of the dispute",
            "fraud_likelihood": "HIGH/MEDIUM/LOW",
            "recommended_actions": ["Action 1", "Action 2", ...],
            "estimated_resolution_time": "X business days",
            "regulatory_considerations": "Relevant Australian banking regulations"
        }
        
        Follow these Australian banking guidelines:
        - Unauthorized transactions should be reported as soon as possible
        - The ePayments Code provides protections for customers
        - Banks must investigate and respond to disputes within 21 days for simple cases
        - Complex cases may take up to 45 days to resolve
        - Customers are generally not liable for unauthorized transactions unless they contributed to the loss
        
        Be factual, precise, and helpful while maintaining privacy and security.
        """
    
    def _create_dispute_analysis_prompt(self, transaction, dispute_request):
        """Create a detailed prompt for the AI based on transaction and dispute details."""
        return f"""
        Please analyze this disputed transaction and provide your assessment:
        
        TRANSACTION DETAILS:
        - Transaction ID: {transaction['transaction_id']}
        - Date: {transaction['date']}
        - Merchant: {transaction['merchant']}
        - Amount: ${transaction['amount']}
        - Category: {transaction['category']}
        - Transaction Type: {transaction['transaction_type']}
        - Payment Method: {transaction['payment_method']}
        - Location: {transaction['location']}
        
        CUSTOMER DISPUTE:
        - Customer ID: {dispute_request.customer_id}
        - Dispute Reason: {dispute_request.reason}
        - Customer Description: {dispute_request.description}
        
        Based on the transaction details and customer's dispute information, please:
        1. Analyze whether this transaction appears to be fraudulent
        2. Recommend next steps for resolution
        3. Provide estimated resolution timeframe
        4. Note any relevant Australian banking regulations
        
        Respond in the JSON format specified in your instructions.
        """