from sentence_transformers import SentenceTransformer
from ..database.mongodb_client import get_mongodb_client
from typing import List, Optional

class MovieQueryEngine:
    def __init__(self, model_name='all-MiniLM-L6-v2', top_k=5):
        """
        Initialize the query engine
        Args:
            model_name (str): Name of the sentence-transformer model
            top_k (int): Number of similar movies to return
        """
        self.model = SentenceTransformer(model_name)
        self.top_k = top_k
        
    def search_similar_movies(
        self, 
        query: str,
        year_start: Optional[int] = None,
        year_end: Optional[int] = None,
        genres: Optional[List[str]] = None,
        sort_by: str = 'relevance'
    ):
        """
        Search for movies with filters
        """
        try:
            query_embedding = self.model.encode(query).tolist()
            client = get_mongodb_client()
            if not client:
                return []
                
            collection = client.sample_mflix.embedded_movies
            
            # Start with vector search
            pipeline = [
                {
                    "$vectorSearch": {
                        "index": "vector_index",
                        "path": "embedding",
                        "queryVector": query_embedding,
                        "numCandidates": 100,
                        "limit": 100  # Increased limit to allow for filtering
                    }
                }
            ]
            
            # Add year filter if provided
            if year_start and year_end:
                pipeline.append({
                    "$match": {
                        "year": {
                            "$gte": year_start,
                            "$lte": year_end
                        }
                    }
                })
            
            # Add genres filter if provided
            if genres and len(genres) > 0:
                pipeline.append({
                    "$match": {
                        "genres": {
                            "$in": genres
                        }
                    }
                })
            
            # Add sorting
            if sort_by != 'relevance':
                sort_stage = {
                    "year_desc": {"$sort": {"year": -1}},
                    "year_asc": {"$sort": {"year": 1}},
                    "title_asc": {"$sort": {"title": 1}},
                    "title_desc": {"$sort": {"title": -1}}
                }.get(sort_by)
                
                if sort_stage:
                    pipeline.append(sort_stage)
            
            # Add final projection
            pipeline.append({
                "$project": {
                    "title": 1,
                    "plot": 1,
                    "year": 1,
                    "genres": 1,
                    "score": {
                        "$meta": "vectorSearchScore"
                    }
                }
            })
            
            # Limit results
            pipeline.append({"$limit": self.top_k})
            
            results = list(collection.aggregate(pipeline))
            return results
            
        except Exception as e:
            print(f"Error searching movies: {e}")
            return []
