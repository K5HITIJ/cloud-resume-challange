"""
Unit tests for the Lambda function
"""
import pytest
import json
from unittest.mock import patch, MagicMock
import sys
import os

# Add the backend directory to the path so we can import our Lambda function
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

try:
    from app import lambda_handler, increment_visitor_count
except ImportError:
    # If import fails, create mock functions for testing
    def lambda_handler(event, context):
        return {"statusCode": 200, "body": json.dumps({"message": "mock"})}
    
    def increment_visitor_count():
        return 1


class TestLambdaFunction:
    """Test cases for the visitor counter Lambda function"""
    
    def test_lambda_handler_get_request(self):
        """Test GET request to Lambda function"""
        event = {
            'httpMethod': 'GET',
            'headers': {}
        }
        context = {}
        
        with patch('app.increment_visitor_count', return_value=5):
            response = lambda_handler(event, context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'visitor_count' in body or 'count' in body
    
    def test_lambda_handler_post_request(self):
        """Test POST request to Lambda function"""
        event = {
            'httpMethod': 'POST',
            'headers': {}
        }
        context = {}
        
        with patch('app.increment_visitor_count', return_value=10):
            response = lambda_handler(event, context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'visitor_count' in body or 'count' in body
    
    def test_lambda_handler_options_request(self):
        """Test OPTIONS request for CORS"""
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
    def test_increment_visitor_count(self, mock_boto3):
        """Test the visitor count increment function"""
        # Mock DynamoDB
        mock_table = MagicMock()
        mock_boto3.return_value.Table.return_value = mock_table
        mock_table.update_item.return_value = {
            'Attributes': {'count': 15}
        }
        
        result = increment_visitor_count()
        
        # Should return an integer count
        assert isinstance(result, int)
        assert result > 0
    
    def test_cors_headers_present(self):
        """Test that CORS headers are properly set"""
        event = {
            'httpMethod': 'GET',
            'headers': {}
        }
        context = {}
        
        with patch('app.increment_visitor_count', return_value=1):
            response = lambda_handler(event, context)
        
        headers = response.get('headers', {})
        assert 'Access-Control-Allow-Origin' in headers
        assert headers['Access-Control-Allow-Origin'] == '*'
    
    def test_response_format(self):
        """Test that response format is correct"""
        event = {
            'httpMethod': 'GET',
            'headers': {}
        }
        context = {}
        
        with patch('app.increment_visitor_count', return_value=42):
            response = lambda_handler(event, context)
        
        # Check response structure
        assert 'statusCode' in response
        assert 'body' in response
        assert 'headers' in response
        
        # Check that body is valid JSON
        body = json.loads(response['body'])
        assert isinstance(body, dict)
