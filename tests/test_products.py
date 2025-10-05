import pytest
from fastapi.testclient import TestClient
from ..app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_get_products(client):
    """Test getting products list"""
    response = client.get("/products")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_filter_by_category(client):
    """Test filtering products by category"""
    response = client.get("/products?category=jackets")
    assert response.status_code == 200


def test_search_by_name(client):
    """Test searching products by name"""
    response = client.get("/products?name=Tech")
    assert response.status_code == 200


def test_product_validation(client):
    """Test product validation - invalid price"""
    invalid_product = {
        "name": "Invalid Product",
        "description": "Test product with invalid price",
        "price": -10.0,
        "category": "test",
        "sizes": "M"
    }

    response = client.post("/products", json=invalid_product)
    assert response.status_code == 422


def test_api_endpoints_exist(client):
    """Test that all API endpoints respond correctly"""
    endpoints = [
        ("/", 200),
        ("/health", 200),
        ("/docs", 200),
        ("/products", 200),
    ]

    for endpoint, expected_status in endpoints:
        response = client.get(endpoint)
        assert response.status_code == expected_status, f"Endpoint {endpoint} returned {response.status_code}, expected {expected_status}"


def test_health_check_content(client):
    """Test health check endpoint content"""
    response = client.get("/health")
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "VNE Techwear Store API"
    assert data["version"] == "1.0.0"


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    data = response.json()
    assert data["message"] == "VNE Techwear Store API"
    assert "docs" in data
    assert "health" in data
