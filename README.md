# Vector Search Movie Demo

This project is a small example of using **MongoDB vector search** with a FastAPI backend and a React frontend.  It queries the MongoDB sample_mflix movie dataset and returns a list of similar movies based on an embedding search.

## Requirements
- Python 3.8 or newer
- Node.js 18 or newer
- A MongoDB cluster with the sample movies dataset and a vector search index named `vector_index`

## Quick Start
1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/vector-search-rag.git
   cd vector-search-rag
   ```
2. **Backend setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r ../requirements.txt
   echo "MONGODB_URI=<your uri>" > .env
   python run.py
   ```
   The API will be available on `http://localhost:8000`.
3. **Frontend setup** (in another terminal)
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Visit `http://localhost:5173` to use the app.

## Running Tests
Tests live under `backend/tests`.  They are minimal and skipped if the environment lacks MongoDB access.  Run them with
```bash
pytest -q
```

## Project Layout
```
backend/  - FastAPI application
frontend/ - React interface
requirements.txt - Python dependencies
```
