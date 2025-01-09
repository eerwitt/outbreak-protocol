import os
import json
import boto3
import logging
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def start_ingestion(bedrock_client, data_source_id, knowledge_base_id):
    """
    Synchronize a data source with a knowledge base.

    Args:
        data_source_id (str): The ID of the data source to synchronize.
        knowledge_base_id (str): The ID of the knowledge base to synchronize with.
    """
    response = bedrock_client.start_ingestion_job(
        knowledgeBaseId=knowledge_base_id,
        dataSourceId=data_source_id
    )
    logger.info(f"Ingestion Job Response: {json.dumps(response)}")

def lambda_handler(event, context):
    """
    Lambda function to start an ingestion job for a Bedrock Knowledge Base.
    
    Args:
        event (dict): The event data triggering the Lambda function.
        context (LambdaContext): The runtime information of the Lambda function.
    
    Returns:
        dict: A response object with the status code and message.
    """
    logger.info("Lambda handler started.")
    logger.info(f"Received event: {json.dumps(event)} {json.dumps(context)}")

    # Retrieve environment variables
    data_source_id = os.getenv("DATASOURCEID")
    knowledge_base_id = os.getenv("KNOWLEDGEBASEID")

    if not data_source_id or not knowledge_base_id:
        logger.error("Environment variables 'DATASOURCEID' or 'KNOWLEDGEBASEID' are missing.")
        return {
            "statusCode": 500,
            "body": "Missing required environment variables: DATASOURCEID or KNOWLEDGEBASEID."
        }

    logger.info(f"Using Knowledge Base ID: {knowledge_base_id}")
    logger.info(f"Using Data Source ID: {data_source_id}")

    bedrock_client = boto3.client("bedrock-agent" )
    try:
        # Start ingestion job
        start_ingestion(bedrock_client, data_source_id, knowledge_base_id)

    except ClientError as e:
        logger.error(f"AWS ClientError occurred: {str(e)}")
        return {
            "statusCode": 500,
            "body": "Failed to start ingestion job due to AWS ClientError."
        }
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        return {
            "statusCode": 500,
            "body": "An unexpected error occurred."
        }

    return {
        "statusCode": 200,
        "body": "Ingestion job started successfully."
    }