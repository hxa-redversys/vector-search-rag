from src.rag_engine.rag_pipeline import MovieRAGPipeline
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import time

load_dotenv()

def test_rag_pipeline_initialization():
    """Test that we can initialize the RAG pipeline"""
    assert os.getenv('FIREWORKS_API_KEY'), "Fireworks API key not found"
    pipeline = MovieRAGPipeline()
    assert pipeline is not None
    assert pipeline.cache_collection is not None

def test_movie_recommendations():
    """Test getting movie recommendations"""
    pipeline = MovieRAGPipeline()
    
    # Test with a simple query
    query = "Show me sci-fi movies about virtual reality"
    
    # First request (should hit the API)
    start_time = time.time()
    response1 = pipeline.get_movie_recommendations(query)
    first_request_time = time.time() - start_time
    
    # Second request with same query (should hit cache)
    start_time = time.time()
    response2 = pipeline.get_movie_recommendations(query)
    second_request_time = time.time() - start_time
    
    # Verify responses
    assert isinstance(response1, dict)
    assert isinstance(response2, dict)
    assert response1 == response2  # Cached response should be identical
    
    # Second request should be faster (cached)
    assert second_request_time < first_request_time
    
    # Check response structure
    assert "answer" in response1
    assert "movies" in response1
    assert isinstance(response1["movies"], list)

def test_empty_query():
    """Test handling of empty query"""
    pipeline = MovieRAGPipeline()
    response = pipeline.get_movie_recommendations("")
    
    assert response["answer"].startswith("I couldn't find")
    assert len(response["movies"]) == 0

def test_cache_expiry():
    """Test that cache entries expire"""
    pipeline = MovieRAGPipeline()
    query = "Test cache expiry"
    
    # Store a result
    result = {
        "answer": "Test answer",
        "movies": []
    }
    pipeline.save_to_cache(query, result)
    
    # Verify it's in cache
    cached = pipeline.get_from_cache(query)
    assert cached == result