from src.data_processing.data_loader import load_sample_movies

def test_load_sample_movies():
    """Test that we can load sample movies from MongoDB"""
    assert load_sample_movies(limit=10) is True