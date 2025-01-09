import unittest
from unittest.mock import patch, MagicMock
import sync_knowledge_base
from botocore.exceptions import ClientError

class TestLambdaHandler(unittest.TestCase):

    @patch('boto3.client')
    def test_lambda_handler_success(self, mock_boto_client):
        # Mock environment variables
        mock_env = {
            'DATASOURCEID': 'test-datasource-id',
            'KNOWLEDGEBASEID': 'test-knowledgebase-id'
        }

        with patch.dict('os.environ', mock_env):
            # Mock Bedrock client response
            mock_bedrock_client = MagicMock()
            mock_bedrock_client.start_ingestion_job.return_value = {
                'JobId': 'test-job-id',
                'Status': 'InProgress'
            }
            mock_boto_client.return_value = mock_bedrock_client

            # Create test event and context
            test_event = {}
            test_context = {}

            # Call Lambda function
            response = sync_knowledge_base.lambda_handler(test_event, test_context)

            # Assert response
            self.assertEqual(response['statusCode'], 200)
            self.assertIn("Ingestion job started successfully", response['body'])

    @patch('boto3.client')
    def test_lambda_handler_missing_env_vars(self, mock_boto_client):
        # Mock environment variables (missing DATASOURCEID)
        mock_env = {
            'KNOWLEDGEBASEID': 'test-knowledgebase-id'
        }

        with patch.dict('os.environ', mock_env):
            # Create test event and context
            test_event = {}
            test_context = {}

            # Call Lambda function
            response = sync_knowledge_base.lambda_handler(test_event, test_context)

            # Assert response
            self.assertEqual(response['statusCode'], 500)
            self.assertIn("Missing required environment variables", response['body'])

    @patch('boto3.client')
    def test_lambda_handler_client_error(self, mock_boto_client):
        # Mock environment variables
        mock_env = {
            'DATASOURCEID': 'test-datasource-id',
            'KNOWLEDGEBASEID': 'test-knowledgebase-id'
        }

        with patch.dict('os.environ', mock_env):
            # Mock Bedrock client to throw a ClientError
            mock_bedrock_client = MagicMock()
            mock_bedrock_client.start_ingestion_job.side_effect = ClientError({"Error": {"Message": "Failed to start ingestion job due to AWS ClientError"}}, "ingestion")
            mock_boto_client.return_value = mock_bedrock_client

            # Create test event and context
            test_event = {}
            test_context = {}

            # Call Lambda function
            response = sync_knowledge_base.lambda_handler(test_event, test_context)

            # Assert response
            self.assertEqual(response['statusCode'], 500)
            self.assertIn("Failed to start ingestion job due to AWS ClientError", response['body'])


if __name__ == "__main__":
    unittest.main()
