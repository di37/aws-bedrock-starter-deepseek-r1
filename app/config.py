import os
from dotenv import load_dotenv

def load_config():
    """Load environment variables from .env file"""
    load_dotenv()
    
    return {
        "aws_service_name": os.getenv("AWS_SERVICE_NAME"),
        "aws_region_name": os.getenv("AWS_REGION_NAME"),
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "model_id": "us.deepseek.r1-v1:0"
    }