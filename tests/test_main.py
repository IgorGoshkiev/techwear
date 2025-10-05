from fastapi.testclient import TestClient
from ..app.main import app


client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "VNE Techwear Store API"
    assert "docs" in data
    assert "health" in data


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "VNE Techwear Store API"


def test_docs_available():
    """Test that API documentation is available"""
    response = client.get("/docs")
    assert response.status_code == 200
