# app/aws_client.py
import boto3

def create_bedrock_client(config):
    """Create a universal boto3 client for AWS Bedrock."""
    return boto3.client(
        service_name=config["aws_service_name"],
        region_name=config["aws_region_name"],
        aws_access_key_id=config["aws_access_key_id"],
        aws_secret_access_key=config["aws_secret_access_key"]
    )
