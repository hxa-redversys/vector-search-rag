from fastapi import FastAPI, HTTPException, Request
from ..rag_engine.rag_pipeline import MovieRAGPipeline
from typing import Optional
from bson import ObjectId
from fastapi.encoders import ENCODERS_BY_TYPE
from fastapi.middleware.cors import CORSMiddleware
from ..utils.rate_limiter import RateLimiter

# Add custom encoder for ObjectId
ENCODERS_BY_TYPE[ObjectId] = str

app = FastAPI(title="Movie RAG API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize rate limiter
rate_limiter = RateLimiter(requests_per_minute=30)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Movie RAG API is running"}

@app.get("/search")
async def search_movies(
    request: Request,
    query: str,
    year_start: Optional[int] = None,
    year_end: Optional[int] = None,
    genres: Optional[str] = None,
    sort_by: str = 'relevance'
):
    """
    Search for movies with rate limiting
    """
    try:
        # Get client IP
        client_ip = request.client.host
        
        # Check rate limit
        rate_limiter.check_rate_limit(client_ip)
        
        pipeline = MovieRAGPipeline()
        genres_list = genres.split(',') if genres else []
        results = pipeline.get_movie_recommendations(
            query,
            year_start=year_start,
            year_end=year_end,
            genres=genres_list,
            sort_by=sort_by
        )
        return results
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))