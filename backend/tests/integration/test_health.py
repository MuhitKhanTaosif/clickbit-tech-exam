"""
Integration tests for health check endpoints.
"""
import pytest
from fastapi import status

class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_health_check(self, test_client):
        """Test basic health check."""
        response = test_client.get("/health/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data
        assert "environment" in data
    
    def test_health_detailed(self, test_client):
        """Test detailed health check."""
        response = test_client.get("/health/detailed")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
        assert "checks" in data
        assert "database" in data["checks"]
        assert "application" in data["checks"]
        assert "uptime_seconds" in data
        assert "memory_usage" in data
        assert "disk_usage" in data
    
    def test_health_full(self, test_client):
        """Test full health check."""
        response = test_client.get("/health/full")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
        assert "system_info" in data
        assert "application_info" in data
        assert "cpu_count" in data["system_info"]
        assert "platform" in data["system_info"]
    
    def test_health_database(self, test_client):
        """Test database health check."""
        response = test_client.get("/health/database")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
        assert "Database connection successful" in data["message"]
    
    def test_readiness_check(self, test_client):
        """Test readiness probe."""
        response = test_client.get("/health/ready")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "ready"
    
    def test_liveness_check(self, test_client):
        """Test liveness probe."""
        response = test_client.get("/health/live")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "alive"
    
    def test_metrics(self, test_client):
        """Test metrics endpoint."""
        response = test_client.get("/health/metrics")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "uptime_seconds" in data
        assert "memory" in data
        assert "disk" in data
        assert "application" in data
        assert data["memory"]["used_percentage"] >= 0
        assert data["disk"]["used_percentage"] >= 0

