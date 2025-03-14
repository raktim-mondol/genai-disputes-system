from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from app.api.routes import router
from app.config import Config
from app.utils.data_generator import generate_data

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=Config.API_TITLE,
    description=Config.API_DESCRIPTION,
    version=Config.API_VERSION,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

# Generate synthetic data if it doesn't exist
@app.on_event("startup")
async def startup_event():
    data_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), Config.DATA_FILE)
    if not os.path.exists(data_file):
        logger.info("Generating synthetic transaction data")
        generate_data()
    else:
        logger.info(f"Using existing data file: {data_file}")

@app.get("/")
async def root():
    return {
        "message": "Gen AI Disputes System API",
        "version": Config.API_VERSION,
        "docs_url": "/docs"
    }