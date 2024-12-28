from fastapi.testclient import TestClient
from src.api.movie_api import app

client = TestClient(app)

def test_root():
    """Test the health check endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_search_endpoint():
    """Test the movie search endpoint"""
    query = "Show me sci-fi movies about virtual reality"
    response = client.get(f"/search?query={query}")
    
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "movies" in data
    assert isinstance(data["movies"], list)

def test_search_empty_query():
    """Test search endpoint with empty query"""
    response = client.get("/search?query=")
    assert response.status_code == 200
    data = response.json()
    assert len(data["movies"]) == 0 