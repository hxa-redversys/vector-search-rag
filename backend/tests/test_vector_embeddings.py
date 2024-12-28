from src.embedding_service.vector_embeddings import MovieEmbeddingService
import os

def test_generate_embeddings():
    """Test that we can generate and store embeddings"""
    # Print current working directory and check if file exists
    test_input_path = 'data/processed/processed_movies.json'
    print(f"Current directory: {os.getcwd()}")
    print(f"Looking for file at: {os.path.abspath(test_input_path)}")
    print(f"File exists: {os.path.exists(test_input_path)}")
    
    # Ensure we have processed data
    assert os.path.exists(test_input_path), "Processed movie data not found"
    
    # Create embedding service
    embedding_service = MovieEmbeddingService()
    
    # Generate and store embeddings using test data path
    assert embedding_service.generate_embeddings(input_file=test_input_path) is True

def test_embedding_dimensions():
    """Test that embeddings have correct dimensions"""
    embedding_service = MovieEmbeddingService()
    
    # Generate a single test embedding
    test_text = "Test movie plot"
    embedding = embedding_service.model.encode(test_text)
    
    # MiniLM-L6-v2 should produce 384-dimensional embeddings
    assert len(embedding) == 384