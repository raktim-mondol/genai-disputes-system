import json
import random
import uuid
from datetime import datetime, timedelta
import os

# Australian merchants
MERCHANTS = [
    "Woolworths", "Coles", "Bunnings", "Kmart", "JB Hi-Fi", 
    "Dan Murphy's", "Officeworks", "Chemist Warehouse", "Myer",
    "David Jones", "Harvey Norman", "Aldi", "IGA", "Target",
    "Westfield", "7-Eleven", "BP", "Shell", "Caltex",
    "McDonald's", "KFC", "Hungry Jack's", "Subway", "Domino's",
    "Uber", "Uber Eats", "Deliveroo", "Menulog", "Netflix",
    "Spotify", "Stan", "Telstra", "Optus", "Vodafone",
    "Commonwealth Bank", "NAB", "ANZ", "Westpac", "Bendigo Bank"
]

# Transaction categories
CATEGORIES = [
    "Groceries", "Retail", "Dining", "Entertainment", "Transport",
    "Utilities", "Health", "Education", "Travel", "Services"
]

# Transaction types
TRANSACTION_TYPES = ["PURCHASE", "PAYMENT", "TRANSFER", "WITHDRAWAL", "REFUND"]

# Payment methods
PAYMENT_METHODS = ["CARD", "DIRECT_DEBIT", "BPAY", "OSKO", "PAYID", "CASH"]

def generate_card_number():
    """Generate a fake card number that follows Australian format."""
    prefix = random.choice(["4", "5", "6"])  # Visa, Mastercard, or other
    if prefix == "4":  # Visa
        return f"4{random.randint(1000, 9999):04d} {random.randint(1000, 9999):04d} {random.randint(1000, 9999):04d} {random.randint(1000, 9999):04d}"
    elif prefix == "5":  # Mastercard
        return f"5{random.randint(100, 999):03d} {random.randint(1000, 9999):04d} {random.randint(1000, 9999):04d} {random.randint(1000, 9999):04d}"
    else:  # Other
        return f"6{random.randint(100, 999):03d} {random.randint(1000, 9999):04d} {random.randint(1000, 9999):04d} {random.randint(1000, 9999):04d}"

def generate_bsb_account():
    """Generate a fake BSB and account number."""
    bsb = f"{random.randint(100, 999):03d}-{random.randint(100, 999):03d}"
    account = f"{random.randint(10000000, 99999999):08d}"
    return f"BSB: {bsb}, Account: {account}"

def generate_transaction(customer_id, is_fraudulent=False):
    """Generate a single transaction record."""
    transaction_date = datetime.now() - timedelta(days=random.randint(1, 30))
    
    # For fraudulent transactions, use different patterns
    if is_fraudulent:
        merchant = random.choice([
            "Unknown Online Store", "Foreign Exchange Service",
            "Crypto Trading Platform", "Unrecognized Merchant",
            "International Transfer", "Gaming Platform",
            "Digital Wallet Top-up", "Overseas Subscription"
        ])
        amount = random.uniform(100, 2000)
        category = random.choice(["Unknown", "International", "Digital"])
        transaction_type = random.choice(["PURCHASE", "TRANSFER"])
        payment_method = random.choice(["CARD", "DIRECT_DEBIT"])
        location = random.choice([
            "Unknown Location", "Overseas", "Foreign IP",
            "Different State", "Unusual Location"
        ])
    else:
        merchant = random.choice(MERCHANTS)
        amount = random.uniform(5, 500)
        category = random.choice(CATEGORIES)
        transaction_type = random.choice(TRANSACTION_TYPES)
        payment_method = random.choice(PAYMENT_METHODS)
        location = random.choice([
            "Sydney, NSW", "Melbourne, VIC", "Brisbane, QLD",
            "Perth, WA", "Adelaide, SA", "Hobart, TAS",
            "Darwin, NT", "Canberra, ACT"
        ])
    
    return {
        "transaction_id": str(uuid.uuid4()),
        "customer_id": customer_id,
        "date": transaction_date.strftime("%Y-%m-%d %H:%M:%S"),
        "merchant": merchant,
        "amount": round(amount, 2),
        "category": category,
        "transaction_type": transaction_type,
        "payment_method": payment_method,
        "card_number": generate_card_number() if payment_method == "CARD" else None,
        "account_details": generate_bsb_account() if payment_method in ["DIRECT_DEBIT", "TRANSFER"] else None,
        "location": location,
        "is_fraudulent": is_fraudulent
    }

def generate_customer_transactions(num_customers=10, transactions_per_customer=20, fraud_probability=0.1):
    """Generate transactions for multiple customers with some fraudulent transactions."""
    all_transactions = []
    
    for i in range(1, num_customers + 1):
        customer_id = f"CUST{i:06d}"
        
        # Generate regular transactions
        for _ in range(transactions_per_customer):
            is_fraudulent = random.random() < fraud_probability
            transaction = generate_transaction(customer_id, is_fraudulent)
            all_transactions.append(transaction)
    
    return all_transactions

def save_transactions_to_file(transactions, filename="synthetic_transactions.json"):
    """Save generated transactions to a JSON file."""
    directory = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
    os.makedirs(directory, exist_ok=True)
    
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w') as f:
        json.dump(transactions, f, indent=2)
    
    print(f"Generated {len(transactions)} transactions and saved to {filepath}")
    return filepath

def generate_data():
    """Main function to generate and save synthetic transaction data."""
    transactions = generate_customer_transactions(
        num_customers=10,
        transactions_per_customer=20,
        fraud_probability=0.1
    )
    return save_transactions_to_file(transactions)

if __name__ == "__main__":
    generate_data()