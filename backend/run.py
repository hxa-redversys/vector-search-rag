import uvicorn

if __name__ == "__main__":
    uvicorn.run("src.api.movie_api:app", host="0.0.0.0", port=8000, reload=True) 