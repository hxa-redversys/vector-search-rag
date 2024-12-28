# Movie Search with AI Recommendations

## What is This?
A smart movie search application that helps users find movies and get AI-powered recommendations. Think of it as having a knowledgeable movie expert who understands what you're looking for and provides personalized suggestions.

## Key Features
- **Smart Search**: Understands the meaning behind your search, not just keywords
- **AI Recommendations**: Gets personalized movie suggestions from an AI assistant
- **Easy Filtering**: Filter by year, genre, and more
- **Dark Mode**: Comfortable viewing in any lighting
- **Search History**: Keeps track of your previous searches
- **Works Offline**: Basic features work without internet

## How It Works
1. **You Search**: Type anything like "movies similar to Inception" or "funny movies about time travel"
2. **AI Processing**: 
   - The app understands your request
   - Searches through a movie database
   - Uses AI to generate personalized recommendations
3. **You Get**: 
   - A written response from the AI about your search
   - A list of relevant movies
   - Details about each movie (plot, year, genres)

## Technical Overview

### Built With
- **Frontend**: React + Material-UI
- **Backend**: FastAPI + MongoDB
- **AI**: Fireworks AI (Mixtral-8x7b)
- **Search**: MongoDB Vector Search

### Core Functionality
- **Intelligent Search**: Vector-based search using MongoDB for semantic understanding
- **AI Recommendations**: Powered by Fireworks AI (Mixtral-8x7b) for contextual movie recommendations
- **Advanced Filtering**: Year range, genres, and custom sorting options
- **Dark Mode**: System-aware theme with persistent user preference

### Technical Implementation
- **Frontend**: React with Material-UI
- **Backend**: FastAPI with MongoDB
- **Vector Search**: Sentence transformers for embedding generation
- **Caching**: Query results caching for improved performance
- **Error Handling**: Comprehensive error boundaries and network status monitoring

## Getting Started

### Prerequisites
- Node.js 16+
- Python 3.8+
- MongoDB Atlas account
- Fireworks AI API key

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/vector-search-rag.git
   cd vector-search-rag
   ```

2. **Set Up Environment Variables**
   Create `.env` files in both frontend and backend directories:

   Backend `.env`:
   ```bash
   MONGODB_URI=your_mongodb_connection_string
   FIREWORKS_API_KEY=your_fireworks_api_key
   ```

   Frontend `.env`:
   ```bash
   VITE_API_URL=http://localhost:8000
   ```

3. **Install Backend Dependencies**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Install Frontend Dependencies**
   ```bash
   cd frontend
   npm install
   ```

5. **Set Up MongoDB**
   - Create a MongoDB Atlas account
   - Create a new cluster
   - Load the sample movie dataset
   - Create a vector search index named "vector_index" on the "embedding" field

6. **Start the Application**

   Start the backend:
   ```bash
   cd backend
   uvicorn src.main:app --reload
   ```

   Start the frontend (in a new terminal):
   ```bash
   cd frontend
   npm run dev
   ```

7. **Access the Application**
   Open your browser and navigate to:
   ```
   http://localhost:5173
   ```

### Troubleshooting

Common issues and solutions:

1. **MongoDB Connection Issues**
   - Ensure your IP is whitelisted in MongoDB Atlas
   - Verify connection string is correct
   - Check network connectivity

2. **Backend Startup Issues**
   - Confirm all environment variables are set
   - Verify Python version (3.8+ required)
   - Check if all dependencies are installed

3. **Frontend Startup Issues**
   - Clear npm cache: `npm cache clean --force`
   - Delete node_modules and reinstall: `rm -rf node_modules && npm install`
   - Verify Node.js version (16+ required)

## Architectural Components

### Application Components

1. **Frontend (React Application)**
   - **Purpose**: User interface and interaction
   - **Key Functions**:
     - Handles user input and search queries
     - Manages application state
     - Renders search results and recommendations
     - Provides filtering and sorting interface
     - Manages dark mode and user preferences
   - **Key Technologies**: React, Material-UI, LocalStorage

2. **Backend API (FastAPI)**
   - **Purpose**: Request handling and business logic
   - **Key Functions**:
     - Processes incoming search requests
     - Manages rate limiting
     - Coordinates between database and AI model
     - Handles error cases and responses
   - **Key Technologies**: FastAPI, Python, Pydantic

3. **Vector Search (MongoDB)**
   - **Purpose**: Semantic search functionality
   - **Key Functions**:
     - Stores movie data and embeddings
     - Performs vector similarity searches
     - Handles complex query filtering
     - Manages data indexing
   - **Key Technologies**: MongoDB Atlas, Vector Search Index

4. **RAG Pipeline**
   - **Purpose**: AI-powered recommendation generation
   - **Key Functions**:
     - Generates embeddings for queries
     - Retrieves relevant movie context
     - Processes AI model responses
     - Formats recommendations
   - **Key Technologies**: SentenceTransformers, Fireworks AI

### Data Flow

1. **Search Request Flow**
```
User Query → Frontend → FastAPI Backend → MongoDB Vector Search → RAG Pipeline → AI Model → Response
```

2. **Data Processing Flow**
```
Query → Embedding Generation → Vector Search → Context Retrieval → AI Processing → Formatted Results
```

3. **Caching Flow**
```
Query → Cache Check → (If Hit) Return Cached Result
                   → (If Miss) Process New Search → Cache Result
```

## Project Structure

### Directory Layout
```
vector-search-rag/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── theme/
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
│
└── backend/
    ├── src/
    │   ├── api/
    │   ├── database/
    │   ├── rag_engine/
    │   └── utils/
    ├── requirements.txt
    └── .env
```

### Critical Files Overview

#### Frontend Files

1. **Components**
```
src/components/
├── ErrorBoundary.jsx       # Global error handling component
├── LoadingState.jsx        # Loading skeletons and states
├── NetworkStatus.jsx       # Network connectivity monitor
└── SearchFilters.jsx       # Advanced search filters UI
```

2. **Hooks and Utilities**
```
src/hooks/
├── useFilterPreferences.js # Filter state management
└── useSearchHistory.js     # Search history management

src/theme/
└── theme.js               # Material-UI theme configuration
```

3. **Core Files**
```
src/
├── App.jsx                # Main application component
└── main.jsx              # Application entry point
```

#### Backend Files

1. **API Layer**
```
src/api/
├── movie_api.py          # FastAPI endpoints and route handlers
└── __init__.py
```

2. **Database Layer**
```
src/database/
├── mongodb_client.py      # MongoDB connection and configuration
└── __init__.py
```

3. **RAG Engine**
```
src/rag_engine/
├── rag_pipeline.py        # Main RAG implementation
├── query_engine.py        # Vector search implementation
└── __init__.py
```

4. **Utilities**
```
src/utils/
├── rate_limiter.py        # Rate limiting implementation
└── __init__.py
```

## Performance Features
- Query result caching
- Rate limiting protection
- Optimized loading states
- Error boundary implementation
- Network status monitoring

## Limitations
- Results limited to movies in the MongoDB sample dataset
- Rate limiting applies to prevent API abuse
- Requires internet connection for AI recommendations

## Contributing
Feel free to submit issues and enhancement requests.

## License
[MIT License](LICENSE)