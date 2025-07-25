import json
import pytest
import boto3
import os
import sys
from unittest.mock import patch, MagicMock

# Set AWS environment variables for testing
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
os.environ['DYNAMODB_TABLE'] = 'test-visitor-counter'

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import lambda_handler, get_visitor_count, increment_visitor_count

class TestVisitorCounter:
    
    @patch('boto3.resource')
    def setup_method(self, mock_boto3):
        """Set up test fixtures before each test method."""
        # Set environment variable
        os.environ['DYNAMODB_TABLE'] = 'test-visitor-counter'
        
        # Mock DynamoDB table
        self.mock_table = MagicMock()
        mock_boto3.return_value.Table.return_value = self.mock_table
        
        # Set up default return values
        self.mock_table.get_item.return_value = {}
        self.mock_table.update_item.return_value = {'Attributes': {'count': 1}}

    @patch('boto3.resource')
    def test_get_visitor_count_new_table(self, mock_boto3):
        """Test getting visitor count when no record exists."""
        # Mock table response for no existing record
        mock_table = MagicMock()
        mock_boto3.return_value.Table.return_value = mock_table
        mock_table.get_item.return_value = {}
        
        count = get_visitor_count()
        assert count == 0

    @patch('boto3.resource')
    def test_increment_visitor_count_new_table(self, mock_boto3):
        """Test incrementing visitor count when no record exists."""
        # Mock table response
        mock_table = MagicMock()
        mock_boto3.return_value.Table.return_value = mock_table
        mock_table.update_item.return_value = {'Attributes': {'count': 1}}
        
        count = increment_visitor_count()
        assert count == 1

    @patch('boto3.resource')
    def test_increment_visitor_count_existing_record(self, mock_boto3):
        """Test incrementing visitor count when record exists."""
        # Mock table response
        mock_table = MagicMock()
        mock_boto3.return_value.Table.return_value = mock_table
        mock_table.update_item.side_effect = [
            {'Attributes': {'count': 1}},
            {'Attributes': {'count': 2}}
        ]
        
        # First increment
        count1 = increment_visitor_count()
        assert count1 == 1
        
        # Second increment
        count2 = increment_visitor_count()
        assert count2 == 2

    @patch('boto3.resource')
    def test_lambda_handler_get_method(self, mock_boto3):
        """Test Lambda handler with GET method."""
        # Mock table response
        mock_table = MagicMock()
        mock_boto3.return_value.Table.return_value = mock_table
        mock_table.get_item.return_value = {}
        
        event = {
            'httpMethod': 'GET'
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'count' in body
        assert body['count'] == 0

    @patch('boto3.resource')
    def test_lambda_handler_post_method(self, mock_boto3):
        """Test Lambda handler with POST method."""
        # Mock table response
        mock_table = MagicMock()
        mock_boto3.return_value.Table.return_value = mock_table
        mock_table.update_item.return_value = {'Attributes': {'count': 1}}
        
        event = {
            'httpMethod': 'POST'
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'count' in body
        assert body['count'] == 1

    def test_lambda_handler_options_method(self):
        """Test Lambda handler with OPTIONS method (CORS preflight)."""
        event = {
            'httpMethod': 'OPTIONS'
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200
        assert 'Access-Control-Allow-Origin' in response['headers']
        assert response['headers']['Access-Control-Allow-Origin'] == '*'

    @patch('boto3.resource')
    def test_lambda_handler_invalid_method(self, mock_boto3):
        """Test Lambda handler with invalid HTTP method."""
        event = {
            'httpMethod': 'DELETE'
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 405
        body = json.loads(response['body'])
        assert 'error' in body

    @patch('boto3.resource')
    def test_cors_headers_present(self, mock_boto3):
        """Test that CORS headers are present in response."""
        # Mock table response
        mock_table = MagicMock()
        mock_boto3.return_value.Table.return_value = mock_table
        mock_table.get_item.return_value = {}
        
        event = {
            'httpMethod': 'GET'
        }
        
        response = lambda_handler(event, None)
        
        headers = response['headers']
        assert 'Access-Control-Allow-Origin' in headers
        assert 'Access-Control-Allow-Headers' in headers
        assert 'Access-Control-Allow-Methods' in headers

if __name__ == '__main__':
    pytest.main([__file__])
