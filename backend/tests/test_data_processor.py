from src.data_processing.data_processor import process_movies
import os
import json

def test_process_movies():
    """Test that we can process movie data"""
    # First ensure we have some raw data to process
    assert os.path.exists('data/raw/sample_movies.json'), "Raw movie data not found"
    
    # Process the movies
    assert process_movies() is True
    
    # Verify the processed file exists and contains valid data
    assert os.path.exists('data/processed/processed_movies.json')
    
    # Check the processed data
    with open('data/processed/processed_movies.json', 'r') as f:
        processed_movies = json.load(f)
    
    assert len(processed_movies) > 0
    assert all('text_for_embedding' in movie for movie in processed_movies)