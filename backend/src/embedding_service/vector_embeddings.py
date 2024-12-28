from sentence_transformers import SentenceTransformer
import json
import os
from ..database.mongodb_client import get_mongodb_client, create_vector_search_index

class MovieEmbeddingService:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initialize the embedding service with a specified model
        Args:
            model_name (str): Name of the sentence-transformer model to use
        """
        self.model = SentenceTransformer(model_name)
        
    def generate_embeddings(self, input_file='backend/data/processed/processed_movies.json'):
        """
        Generate embeddings for processed movie data and store in MongoDB
        Args:
            input_file (str): Path to processed movie data. 
            Default is production path, override for testing.
        Returns:
            bool: Success status
        """
        try:
            # Load processed movies
            with open(input_file, 'r') as f:
                movies = json.load(f)
            
            # Generate embeddings for each movie
            for movie in movies:
                text = movie['text_for_embedding']
                embedding = self.model.encode(text)
                movie['embedding'] = embedding.tolist()  # Convert numpy array to list for MongoDB storage
            
            # Ensure vector search index exists
            if not create_vector_search_index():
                return False
                
            # Store in MongoDB
            client = get_mongodb_client()
            if not client:
                return False
                
            collection = client.sample_mflix.embedded_movies  # Updated database and collection names
            
            # Clear existing data
            collection.delete_many({})
            
            # Insert movies with embeddings
            collection.insert_many(movies)
            
            print(f"Successfully generated and stored embeddings for {len(movies)} movies")
            return True
            
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return False