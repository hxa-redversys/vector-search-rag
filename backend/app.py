import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv()

# Initialize app and model
app = FastAPI(title="Movie Search API")

# Use a lightweight dummy model when running tests to avoid network downloads
if os.getenv("TESTING") == "1":
    class DummyModel:
        def encode(self, text):
            return [0.0] * 384

    model = DummyModel()
else:
    model = SentenceTransformer("all-MiniLM-L6-v2")

# Mongo connection
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI) if MONGODB_URI else None


def get_movies(query: str, limit: int = 5,
               year_start: Optional[int] = None,
               year_end: Optional[int] = None,
               genres: Optional[List[str]] = None) -> List[dict]:
    if not client:
        raise RuntimeError("MongoDB not configured")
    embedding = model.encode(query).tolist()
    collection = client.sample_mflix.embedded_movies
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": embedding,
                "numCandidates": 100,
                "limit": limit
            }
        }
    ]
    match = {}
    if year_start and year_end:
        match["year"] = {"$gte": year_start, "$lte": year_end}
    if genres:
        match["genres"] = {"$in": genres}
    if match:
        pipeline.append({"$match": match})
    pipeline.append({
        "$project": {
            "title": 1,
            "plot": 1,
            "year": 1,
            "genres": 1,
            "score": {"$meta": "vectorSearchScore"}
        }
    })
    return list(collection.aggregate(pipeline))


class MovieResponse(BaseModel):
    title: str
    plot: Optional[str] = None
    year: Optional[int] = None
    genres: List[str] = []


@app.get("/")
def read_root():
    return {"status": "ok"}


@app.get("/search")
def search(query: str,
           year_start: Optional[int] = None,
           year_end: Optional[int] = None,
           genres: Optional[str] = None,
           limit: int = 5):
    try:
        genre_list = genres.split(',') if genres else None
        movies = get_movies(query, limit, year_start, year_end, genre_list)
        # Convert ObjectId to string for JSON
        for m in movies:
            m["_id"] = str(m["_id"])
        return {"movies": movies}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
