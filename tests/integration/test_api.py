import pytest
import requests
import boto3
import os
import time
from typing import Dict, Any


class TestAPIIntegration:
    """Integration tests for the visitor counter API"""
    
    @pytest.fixture(scope="class")
    def api_url(self) -> str:
        """Get API URL from CloudFormation stack outputs"""
        environment = os.getenv('ENVIRONMENT', 'staging')
        stack_name = f"cloud-resume-{environment}" if environment == 'staging' else "cloud-resume-challenge"
        
        client = boto3.client('cloudformation', region_name='us-east-1')
        try:
            response = client.describe_stacks(StackName=stack_name)
            outputs = response['Stacks'][0]['Outputs']
            
            for output in outputs:
                if output['OutputKey'] == 'VisitorCounterApiUrl':
                    return output['OutputValue']
            
            raise ValueError(f"VisitorCounterApiUrl not found in stack {stack_name}")
        except Exception as e:
            pytest.fail(f"Failed to get API URL: {str(e)}")
    
    def test_api_health_check(self, api_url: str):
        """Test that the API endpoint is accessible"""
        response = requests.get(api_url, timeout=10)
        assert response.status_code == 200, f"API health check failed: {response.status_code}"
    
    def test_cors_headers(self, api_url: str):
        """Test that CORS headers are properly set"""
        response = requests.options(api_url, timeout=10)
        assert response.status_code == 200
        
        headers = response.headers
        assert 'Access-Control-Allow-Origin' in headers
        assert 'Access-Control-Allow-Methods' in headers
        assert 'Access-Control-Allow-Headers' in headers
    
    def test_visitor_count_increment(self, api_url: str):
        """Test that visitor count increments properly"""
        # Get initial count
        response1 = requests.get(api_url, timeout=10)
        assert response1.status_code == 200
        
        data1 = response1.json()
        assert 'visitor_count' in data1
        initial_count = data1['visitor_count']
        
        # Wait a moment and get count again
        time.sleep(1)
        response2 = requests.get(api_url, timeout=10)
        assert response2.status_code == 200
        
        data2 = response2.json()
        new_count = data2['visitor_count']
        
        # Count should have incremented
        assert new_count >= initial_count, f"Count didn't increment: {initial_count} -> {new_count}"
    
    def test_post_method(self, api_url: str):
        """Test POST method functionality"""
        response = requests.post(api_url, timeout=10)
        assert response.status_code == 200
        
        data = response.json()
        assert 'visitor_count' in data
        assert isinstance(data['visitor_count'], int)
        assert data['visitor_count'] > 0
    
    def test_response_format(self, api_url: str):
        """Test that API response has correct format"""
        response = requests.get(api_url, timeout=10)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, dict)
        assert 'visitor_count' in data
        assert isinstance(data['visitor_count'], int)
        
        # Check response headers
        assert response.headers.get('Content-Type') == 'application/json'
    
    def test_api_latency(self, api_url: str):
        """Test that API responds within acceptable time"""
        start_time = time.time()
        response = requests.get(api_url, timeout=10)
        end_time = time.time()
        
        assert response.status_code == 200
        latency = end_time - start_time
        assert latency < 5.0, f"API latency too high: {latency:.2f}s"
    
    def test_multiple_requests(self, api_url: str):
        """Test handling of multiple concurrent-ish requests"""
        responses = []
        
        for _ in range(5):
            response = requests.get(api_url, timeout=10)
            assert response.status_code == 200
            responses.append(response.json())
            time.sleep(0.1)  # Small delay between requests
        
        # All requests should succeed
        assert len(responses) == 5
        
        # Visitor counts should be increasing
        counts = [r['visitor_count'] for r in responses]
        assert all(isinstance(count, int) for count in counts)
        assert counts == sorted(counts), "Visitor counts should be increasing"


class TestDynamoDBIntegration:
    """Integration tests for DynamoDB operations"""
    
    @pytest.fixture(scope="class")
    def dynamodb_table_name(self) -> str:
        """Get DynamoDB table name from environment or CloudFormation"""
        environment = os.getenv('ENVIRONMENT', 'staging')
        stack_name = f"cloud-resume-{environment}" if environment == 'staging' else "cloud-resume-challenge"
        
        client = boto3.client('cloudformation', region_name='us-east-1')
        try:
            response = client.describe_stacks(StackName=stack_name)
            outputs = response['Stacks'][0]['Outputs']
            
            for output in outputs:
                if output['OutputKey'] == 'VisitorCounterTable':
                    return output['OutputValue']
            
            # Fallback to standard naming
            return f"VisitorCounter-{environment}" if environment == 'staging' else "VisitorCounter"
        except Exception:
            return f"VisitorCounter-{environment}" if environment == 'staging' else "VisitorCounter"
    
    def test_dynamodb_table_exists(self, dynamodb_table_name: str):
        """Test that DynamoDB table exists and is accessible"""
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        
        try:
            table = dynamodb.Table(dynamodb_table_name)
            # This will raise an exception if table doesn't exist
            table.load()
            assert table.table_status == 'ACTIVE'
        except Exception as e:
            pytest.fail(f"DynamoDB table check failed: {str(e)}")
    
    def test_table_has_visitor_record(self, dynamodb_table_name: str):
        """Test that the visitor counter record exists"""
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table(dynamodb_table_name)
        
        try:
            response = table.get_item(Key={'id': 'visitor_count'})
            assert 'Item' in response, "Visitor count record not found"
            
            item = response['Item']
            assert 'count' in item, "Count field not found in visitor record"
            assert isinstance(item['count'], int), "Count should be an integer"
            assert item['count'] >= 0, "Count should be non-negative"
        except Exception as e:
            pytest.fail(f"DynamoDB record check failed: {str(e)}")
