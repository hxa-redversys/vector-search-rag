from pymongo import MongoClient
from bson import ObjectId
import os
from typing import Dict, Any, List
from datetime import datetime

def get_mongodb_client():
    """Get MongoDB client instance"""
    try:
        client = MongoClient(os.getenv('MONGODB_URI'))
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def serialize_mongodb_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Convert MongoDB document to JSON-serializable format"""
    if not doc:
        return doc
        
    serialized = {}
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            serialized[key] = str(value)
        elif isinstance(value, datetime):
            serialized[key] = value.isoformat()
        elif isinstance(value, list):
            serialized[key] = [serialize_mongodb_doc(item) if isinstance(item, dict) else item for item in value]
        elif isinstance(value, dict):
            serialized[key] = serialize_mongodb_doc(value)
        else:
            serialized[key] = value
    return serialized

class MongoDBClient:
    def __init__(self):
        self.client = get_mongodb_client()
        self.db = self.client.sample_mflix if self.client else None
        
    def find_similar_movies(self, query_vector: List[float], limit: int = 5) -> List[Dict]:
        """Find similar movies using vector search"""
        try:
            if not self.db:
                return []
                
            results = self.db.embedded_movies.aggregate([
                {
                    "$vectorSearch": {
                        "index": "vector_index",
                        "path": "embedding",
                        "queryVector": query_vector,
                        "numCandidates": 100,
                        "limit": limit
                    }
                }
            ])
            
            # Serialize before returning
            return [serialize_mongodb_doc(doc) for doc in results]
            
        except Exception as e:
            print(f"Error in vector search: {e}")
            return []
            
    def get_from_cache(self, query: str) -> Dict:
        """Get cached query result"""
        if not self.db:
            return None
            
        result = self.db.query_cache.find_one({"query": query})
        return serialize_mongodb_doc(result) if result else None
        
    def save_to_cache(self, query: str, result: Dict) -> None:
        """Save query result to cache"""
        if not self.db:
            return
            
        # Data is already serialized at this point
        self.db.query_cache.update_one(
            {"query": query},
            {"$set": {
                "result": result,
                "timestamp": datetime.utcnow()
            }},
            upsert=True
        ) 