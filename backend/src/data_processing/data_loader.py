import json
import os
from datetime import datetime
from bson import ObjectId
from ..database.mongodb_client import get_mongodb_client

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

def load_sample_movies(limit=100):
    """
    Loads sample movies from MongoDB Atlas sample dataset
    Args:
        limit (int): Number of movies to load
    Returns:
        bool: Success status
    """
    client = get_mongodb_client()
    if not client:
        return False
    
    try:
        # Access the sample_mflix database
        sample_collection = client.sample_mflix.movies
        
        # Fetch movies
        movies = list(sample_collection.find().limit(limit))
        
        # Prepare output path
        output_path = os.path.join('data', 'raw', 'sample_movies.json')
        os.makedirs(os.path.join('data', 'raw'), exist_ok=True)
        
        # Save to file with custom serializer
        with open(output_path, 'w') as f:
            json.dump(movies, f, indent=2, default=json_serial)
        
        print(f"Successfully saved {len(movies)} movies to {output_path}")
        return True
        
    except Exception as e:
        print(f"Error loading sample data: {e}")
        return False