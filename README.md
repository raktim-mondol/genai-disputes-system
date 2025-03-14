# Gen AI Disputes System

A prototype system for handling unauthorized transaction disputes using Generative AI.

## Overview

This system provides a streamlined capability for customers to lodge disputes for unauthorized transactions. It uses OpenAI's API to analyze disputes and provide recommendations based on Australian banking regulations.

## Features

- Synthetic transaction data generation
- API endpoints for viewing transactions and creating disputes
- AI-powered dispute analysis
- Compliance with Australian banking regulations

## Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. Clone the repository
```bash
git clone https://github.com/raktim-mondol/genai-disputes-system.git
cd genai-disputes-system
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create a `.env` file based on `.env.example` and add your OpenAI API key

### Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

API documentation is available at http://localhost:8000/docs

## API Endpoints

- `GET /api/transactions/{customer_id}` - Get all transactions for a customer
- `GET /api/transactions/{customer_id}/{transaction_id}` - Get a specific transaction
- `POST /api/disputes` - Create a new dispute
- `GET /api/disputes/{customer_id}` - Get all disputes for a customer
- `GET /api/disputes/{customer_id}/{dispute_id}` - Get a specific dispute

## Deployment

This application is designed to be deployed on AWS. Recommended services:

- AWS Lambda for the API
- Amazon S3 for static files
- Amazon DynamoDB for data storage
- AWS Secrets Manager for API keys

## Security Considerations

- This is a prototype and should not be used with real customer data without additional security measures
- In production, implement proper authentication and authorization
- Encrypt sensitive data at rest and in transit
- Follow AWS security best practices

## Australian Banking Regulations

This system is designed with consideration for:

- ePayments Code
- Banking Code of Practice
- Privacy Act 1988
- Anti-Money Laundering and Counter-Terrorism Financing Act 2006