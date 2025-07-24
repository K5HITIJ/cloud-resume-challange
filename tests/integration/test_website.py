import requests
import json
import pytest
import time

class TestWebsiteIntegration:
    """Integration tests for the live website"""
    
    def setup_class(self):
        """Setup test configuration"""
        self.website_url = "https://dlwihg4xkk5ga.cloudfront.net"
        self.api_url = "https://gyi4noddk5.execute-api.us-east-1.amazonaws.com/Prod/visitor-count"
    
    def test_website_accessibility(self):
        """Test that the website is accessible"""
        response = requests.get(self.website_url)
        assert response.status_code == 200
        assert "Kshitij Mishra" in response.text
        assert "DevOps Engineer" in response.text
    
    def test_visitor_counter_api_get(self):
        """Test GET endpoint for visitor counter"""
        response = requests.get(self.api_url)
        assert response.status_code == 200
        
        data = response.json()
        assert "count" in data
        assert "visitor_count" in data
        assert isinstance(data["count"], int)
        assert data["count"] >= 0
    
    def test_visitor_counter_api_post(self):
        """Test POST endpoint for visitor counter"""
        # Get current count
        get_response = requests.get(self.api_url)
        current_count = get_response.json()["count"]
        
        # Increment count
        post_response = requests.post(self.api_url)
        assert post_response.status_code == 200
        
        new_data = post_response.json()
        assert new_data["count"] == current_count + 1
    
    def test_cors_headers(self):
        """Test that CORS headers are properly set"""
        response = requests.options(self.api_url)
        assert response.status_code == 200
        
        headers = response.headers
        assert "Access-Control-Allow-Origin" in headers
        assert headers["Access-Control-Allow-Origin"] == "*"
    
    def test_website_performance(self):
        """Test website load time"""
        start_time = time.time()
        response = requests.get(self.website_url)
        load_time = time.time() - start_time
        
        assert response.status_code == 200
        assert load_time < 3.0  # Should load within 3 seconds
    
    def test_ssl_certificate(self):
        """Test that website uses HTTPS"""
        response = requests.get(self.website_url)
        assert response.url.startswith("https://")
    
    def test_visitor_counter_in_html(self):
        """Test that visitor counter element exists in HTML"""
        response = requests.get(self.website_url)
        assert "visitor-count" in response.text
        assert "Visitor Count:" in response.text
