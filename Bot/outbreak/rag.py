import boto3
import json
import logging
from typing import Dict, Any

from outbreak.models import RAGRequestPayload, RAGResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BedrockRAGClient:
    """
    A client to interact with Amazon Bedrock for making Retrieval-Augmented Generation (RAG) requests.
    """

    def __init__(self, region_name: str):
        """
        Initialize the BedrockRAGClient.

        Args:
            region_name (str): AWS region where the Bedrock service is hosted.
        """
        self.client = boto3.client('bedrock-runtime', region_name=region_name)

    def make_rag_request(self, model_id: str, rag_request_payload: RAGRequestPayload) -> Dict[str, Any]:
        """
        Make a RAG request to the specified model in Amazon Bedrock.

        Args:
            model_id (str): Identifier of the model to use for the RAG request.
            rag_request_payload (RAGRequestPayload): Payload containing the RAG request input and parameters.

        Returns:
            Dict[str, Any]: The response from the Bedrock model.

        Raises:
            Exception: If an error occurs during the request.
        """
        try:
            # Make the request to the Bedrock endpoint
            response = self.client.invoke_model(
                modelId=model_id,
                body=rag_request_payload.to_json()
            )

            # Parse and return the response
            response_payload = RAGResponse.from_json(response['body'].read())
            for chat_response in response_payload.content:
                logger.info(json.loads(chat_response.text))
            return response_payload

        except Exception as e:
            raise Exception(f"An error occurred during the RAG request: {e}")