from src.rag_engine.query_engine import MovieQueryEngine

def test_movie_search():
    """Test that we can search for similar movies"""
    # Create query engine
    query_engine = MovieQueryEngine(top_k=3)
    
    # Test search
    query = "A sci-fi movie about virtual reality"
    results = query_engine.search_similar_movies(query)
    
    # Verify results
    assert isinstance(results, list)
    assert len(results) <= 3  # Should return at most top_k results
    
    if results:  # If we got any results
        # Check result structure
        first_result = results[0]
        assert 'title' in first_result
        assert 'plot' in first_result
        assert 'score' in first_result

def test_empty_query():
    """Test handling of empty query"""
    query_engine = MovieQueryEngine()
    results = query_engine.search_similar_movies("")
    assert isinstance(results, list)
    assert len(results) == 0