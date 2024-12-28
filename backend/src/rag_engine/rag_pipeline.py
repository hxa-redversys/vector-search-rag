from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_fireworks import ChatFireworks
from ..database.mongodb_client import get_mongodb_client
from .query_engine import MovieQueryEngine
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, UTC
from typing import Optional, List

load_dotenv()

class MovieRAGPipeline:
    def __init__(self):
        """Initialize the RAG pipeline with vector store and LLM"""
        self.query_engine = MovieQueryEngine()
        self.llm = ChatFireworks(
            fireworks_api_key=os.getenv('FIREWORKS_API_KEY'),
            model="accounts/fireworks/models/mixtral-8x7b-instruct"
        )
        self.client = get_mongodb_client()
        self.cache_collection = self.client.sample_mflix.query_cache
        
        # Create TTL index for cache expiry (24 hours)
        self.cache_collection.create_index(
            "timestamp", 
            expireAfterSeconds=24*60*60
        )
        
        # Create prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are a helpful movie expert. Use the following movie information to answer the question.
            If you don't know the answer, just say you don't know.

            Context: {context}
            
            Question: {question}
            
            Answer: """
        )
        
    def get_from_cache(self, query):
        """Check if query result exists in cache"""
        cache_entry = self.cache_collection.find_one({
            "query": query,
            "timestamp": {"$gt": datetime.now(UTC) - timedelta(hours=24)}
        })
        return cache_entry.get("result") if cache_entry else None
        
    def save_to_cache(self, query, result):
        """Save query result to cache"""
        self.cache_collection.update_one(
            {"query": query},
            {
                "$set": {
                    "result": result,
                    "timestamp": datetime.utcnow()
                }
            },
            upsert=True
        )
        
    def get_movie_recommendations(
        self, 
        query: str,
        year_start: Optional[int] = None,
        year_end: Optional[int] = None,
        genres: Optional[List[str]] = None,
        sort_by: str = 'relevance'
    ):
        """Get movie recommendations based on user query with filters"""
        try:
            if not query.strip():
                return {
                    "answer": "I couldn't find any movies. Please provide a search query.",
                    "movies": []
                }
                
            # Create cache key that includes filters
            cache_key = f"{query}_{year_start}_{year_end}_{','.join(genres or [])}_{sort_by}"
            
            # Check cache first
            cached_result = self.get_from_cache(cache_key)
            if cached_result:
                print("Cache hit!")
                return cached_result
                
            # If not in cache, proceed with normal flow
            similar_movies = self.query_engine.search_similar_movies(
                query,
                year_start=year_start,
                year_end=year_end,
                genres=genres,
                sort_by=sort_by
            )
            
            if not similar_movies:
                return {
                    "answer": "I couldn't find any relevant movies. Please try a different query.",
                    "movies": []
                }
            
            # Format movies for context
            context = "\n".join([
                f"Title: {movie['title']}\nPlot: {movie['plot']}\nYear: {movie.get('year', 'N/A')}\nGenres: {', '.join(movie.get('genres', []))}\n"
                for movie in similar_movies
            ])
            
            # Generate response using LLM
            prompt = self.prompt_template.format(
                context=context,
                question=query
            )
            
            # Updated to use invoke instead of predict (fixes deprecation warning)
            response = self.llm.invoke(prompt).content
            
            result = {
                "answer": response,
                "movies": similar_movies
            }
            
            # Save to cache with the new cache key
            self.save_to_cache(cache_key, result)
            
            return result
            
        except Exception as e:
            print(f"Error in RAG pipeline: {e}")
            return {
                "answer": "Sorry, I encountered an error processing your request.",
                "movies": []
            }