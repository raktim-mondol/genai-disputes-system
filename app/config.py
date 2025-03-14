import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # API settings
    API_TITLE = "Gen AI Disputes System"
    API_VERSION = "0.1.0"
    API_DESCRIPTION = "A prototype system for handling unauthorized transaction disputes using Gen AI"
    
    # OpenAI settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
    
    # Data settings
    DATA_FILE = os.getenv("DATA_FILE", "data/synthetic_transactions.json")
    
    # Security settings
    JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-key-change-in-production")
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION = 3600  # 1 hour
    
    # Australian Banking Regulations
    # These would be more comprehensive in a real system
    MAX_DISPUTE_AMOUNT = 10000.0  # Maximum amount that can be disputed through this system
    DISPUTE_TIME_LIMIT_DAYS = 60  # Number of days after transaction to allow disputes
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")