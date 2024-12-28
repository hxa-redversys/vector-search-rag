from fastapi.testclient import TestClient
from src.api.movie_api import app
import time

client = TestClient(app)

def test_complete_search_flow():
    """Test the complete flow from query to response"""
    # Test different types of queries
    test_cases = [
        {
            "query": "sci-fi movies about virtual reality",
            "expected_genres": ["Sci-Fi"]
        },
        {
            "query": "romantic comedies from the 90s",
            "expected_genres": ["Romance", "Comedy"]
        },
        {
            "query": "action movies with strong female leads",
            "expected_genres": ["Action"]
        }
    ]
    
    for test_case in test_cases:
        # Make the API request
        response = client.get(f"/search?query={test_case['query']}")
        
        # Check response structure and status
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "movies" in data
        assert len(data["movies"]) > 0
        
        # Check response content
        assert len(data["answer"]) > 0  # Should have a non-empty explanation
        
        # Check movie data structure
        first_movie = data["movies"][0]
        assert "title" in first_movie
        assert "plot" in first_movie
        assert "genres" in first_movie
        
        # Print results for manual verification
        print(f"\nQuery: {test_case['query']}")
        print(f"First movie: {first_movie['title']}")
        print(f"Answer snippet: {data['answer'][:100]}...")

def test_error_handling():
    """Test error handling in the complete flow"""
    test_cases = [
        {"query": "", "expected_status": 200},  # Empty query
        {"query": " ", "expected_status": 200},  # Whitespace query
        {"query": "a" * 1000, "expected_status": 200}  # Very long query
    ]
    
    for test_case in test_cases:
        response = client.get(f"/search?query={test_case['query']}")
        assert response.status_code == test_case["expected_status"]

def test_performance():
    """Test response times and caching"""
    query = "sci-fi movies about virtual reality"
    
    # First request (should hit API)
    start_time = time.time()
    response1 = client.get(f"/search?query={query}")
    first_request_time = time.time() - start_time
    
    # Second request (should hit cache)
    start_time = time.time()
    response2 = client.get(f"/search?query={query}")
    second_request_time = time.time() - start_time
    
    # Cache should make second request faster
    assert second_request_time < first_request_time
    print(f"\nFirst request time: {first_request_time:.2f}s")
    print(f"Cached request time: {second_request_time:.2f}s") 