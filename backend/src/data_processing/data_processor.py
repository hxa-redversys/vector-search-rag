import json
import os

def process_movies(input_file='data/raw/sample_movies.json', output_file='data/processed/processed_movies.json'):
    """
    Process movie data to prepare it for vector embeddings
    Args:
        input_file (str): Path to raw movie data
        output_file (str): Path to save processed data
    Returns:
        bool: Success status
    """
    try:
        # Read the raw movie data
        with open(input_file, 'r') as f:
            movies = json.load(f)
        
        # Process each movie
        processed_movies = []
        for movie in movies:
            processed_movie = {
                'id': movie['_id'],
                'title': movie.get('title', ''),
                'plot': movie.get('plot', ''),
                'year': movie.get('year', ''),
                'genres': movie.get('genres', []),
                # Combine plot and other fields for rich text representation
                'text_for_embedding': f"{movie.get('title', '')} {movie.get('plot', '')} {' '.join(movie.get('genres', []))}"
            }
            processed_movies.append(processed_movie)
        
        # Create processed directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Save processed data
        with open(output_file, 'w') as f:
            json.dump(processed_movies, f, indent=2)
            
        print(f"Successfully processed {len(processed_movies)} movies")
        return True
        
    except Exception as e:
        print(f"Error processing movies: {e}")
        return False