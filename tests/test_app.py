import json
import pytest
import boto3
from moto import mock_dynamodb
import os
import sys

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import lambda_handler, get_visitor_count, increment_visitor_count

@mock_dynamodb
class TestVisitorCounter:
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Set environment variable
        os.environ['DYNAMODB_TABLE'] = 'test-visitor-counter'
        
        # Create mock DynamoDB table
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = self.dynamodb.create_table(
            TableName='test-visitor-counter',
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                }
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        
        # Recreate the app's table reference with the mock
        import app
        app.table = self.table

    def test_get_visitor_count_new_table(self):
        """Test getting visitor count when no record exists."""
        count = get_visitor_count()
        assert count == 0

    def test_increment_visitor_count_new_table(self):
        """Test incrementing visitor count when no record exists."""
        count = increment_visitor_count()
        assert count == 1

    def test_increment_visitor_count_existing_record(self):
        """Test incrementing visitor count when record exists."""
        # First increment
        count1 = increment_visitor_count()
        assert count1 == 1
        
        # Second increment
        count2 = increment_visitor_count()
        assert count2 == 2

    def test_lambda_handler_get_method(self):
        """Test Lambda handler with GET method."""
        event = {
            'httpMethod': 'GET'
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'count' in body
        assert body['count'] == 0

    def test_lambda_handler_post_method(self):
        """Test Lambda handler with POST method."""
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

    def test_lambda_handler_invalid_method(self):
        """Test Lambda handler with invalid HTTP method."""
        event = {
            'httpMethod': 'DELETE'
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 405
        body = json.loads(response['body'])
        assert 'error' in body

    def test_cors_headers_present(self):
        """Test that CORS headers are present in response."""
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
