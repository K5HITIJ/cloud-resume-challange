"""
Unit tests for the Lambda function
"""
import pytest
import json
import os
from unittest.mock import patch, MagicMock

# Set AWS environment variables for testing
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'


class TestLambdaFunction:
    """Test cases for the visitor counter Lambda function"""
    
    @patch('boto3.resource')
    def test_lambda_handler_get_request(self, mock_boto3):
        """Test GET request to Lambda function"""
        # Mock DynamoDB table
        mock_table = MagicMock()
        mock_boto3.return_value.Table.return_value = mock_table
        mock_table.update_item.return_value = {
            'Attributes': {'count': 5}
        }
        
        # Import after mocking
        import sys
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))
        from app import lambda_handler
        
        event = {
            'httpMethod': 'GET',
            'headers': {}
        }
        context = {}
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'visitor_count' in body or 'count' in body
    
    @patch('boto3.resource')
    def test_lambda_handler_post_request(self, mock_boto3):
        """Test POST request to Lambda function"""
        # Mock DynamoDB table
        mock_table = MagicMock()
        mock_boto3.return_value.Table.return_value = mock_table
        mock_table.update_item.return_value = {
            'Attributes': {'count': 10}
        }
        
        # Import after mocking
        import sys
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))
        from app import lambda_handler
        
        event = {
            'httpMethod': 'POST',
            'headers': {}
        }
        context = {}
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'visitor_count' in body or 'count' in body
    
    @patch('boto3.resource')
    def test_lambda_handler_options_request(self, mock_boto3):
        """Test OPTIONS request for CORS"""
        # Import after mocking
        import sys
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))
        from app import lambda_handler
        
        event = {
            'httpMethod': 'OPTIONS',
            'headers': {}
        }
        context = {}
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 200
        assert 'Access-Control-Allow-Origin' in response['headers']
        assert 'Access-Control-Allow-Methods' in response['headers']
    
    @patch('boto3.resource')
    def test_cors_headers_present(self, mock_boto3):
        """Test that CORS headers are properly set"""
        # Mock DynamoDB table
        mock_table = MagicMock()
        mock_boto3.return_value.Table.return_value = mock_table
        mock_table.update_item.return_value = {
            'Attributes': {'count': 1}
        }
        
        # Import after mocking
        import sys
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))
        from app import lambda_handler
        
        event = {
            'httpMethod': 'GET',
            'headers': {}
        }
        context = {}
        
        response = lambda_handler(event, context)
        
        headers = response.get('headers', {})
        assert 'Access-Control-Allow-Origin' in headers
        assert headers['Access-Control-Allow-Origin'] == '*'
    
    @patch('boto3.resource')
    def test_response_format(self, mock_boto3):
        """Test that response format is correct"""
        # Mock DynamoDB table
        mock_table = MagicMock()
        mock_boto3.return_value.Table.return_value = mock_table
        mock_table.update_item.return_value = {
            'Attributes': {'count': 42}
        }
        
        # Import after mocking
        import sys
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))
        from app import lambda_handler
        
        event = {
            'httpMethod': 'GET',
            'headers': {}
        }
        context = {}
        
        response = lambda_handler(event, context)
        
        # Check response structure
        assert 'statusCode' in response
        assert 'body' in response
        assert 'headers' in response
        
        # Check that body is valid JSON
        body = json.loads(response['body'])
        assert isinstance(body, dict)
    
    def test_basic_functionality(self):
        """Test basic test functionality without AWS dependencies"""
        # Simple test to ensure pytest is working
        assert True
        assert 1 + 1 == 2
        
        # Test JSON handling
        test_data = {"test": "value"}
        json_str = json.dumps(test_data)
        parsed = json.loads(json_str)
        assert parsed == test_data
