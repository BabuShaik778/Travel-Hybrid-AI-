# Travel-Hybrid-AI

An intelligent travel assistant combining OpenAI, Pinecone, and Neo4j to provide personalized, itinerary-style travel recommendations.

## Table of Contents
- About
- Features
- Tech Stack
- Installation and Usage
- Data Preparation
- Contributing
- License

## About
Travel-Hybrid-AI leverages AI embeddings and graph-based relationships to generate rich, context-aware travel recommendations. Users can ask questions about destinations, and the system responds with detailed itineraries, activity suggestions, and personalized insights.

## Features
- Generate day-wise travel itineraries for destinations
- Combine semantic vector search (Pinecone) with graph-based knowledge (Neo4j)
- Interactive command-line chat interface
- Easily extensible with new datasets and destinations

## Tech Stack
- AI: OpenAI GPT-4 (via openai Python SDK)
- Vector Database: Pinecone
- Graph Database: Neo4j
- Backend: Python 3.x
- Utilities: tqdm, python-dotenv

## Installation and Usage

1. Clone the repository and set up the virtual environment:
   git clone https://github.com/BabuShaik778/Travel-Hybrid-AI-.git
   cd Travel-Hybrid-AI

3. Create a virtual environment:
   python -m venv venv

4. Activate the virtual environment:
   Windows: venv\Scripts\activate
   macOS/Linux: source venv/bin/activate

5. Install dependencies:
   pip install -r requirements.txt

6. Configure API keys in config.py:
   OPENAI_API_KEY = "your_openai_api_key"
   PINECONE_API_KEY = "your_pinecone_api_key"
   PINECONE_INDEX_NAME = "travel-hybrid"
   NEO4J_URI = "bolt://localhost:7687"
   NEO4J_USER = "neo4j"
   NEO4J_PASSWORD = "your_neo4j_password"

7. Load data to Neo4j:
   python load_to_neo4j.py
   This will load your vietnam_travel_dataset.json into Neo4j as City and Activity nodes.

8. Upload embeddings to Pinecone:
   python pinecone_upload.py
   Uploads vector embeddings for each activity description to Pinecone for semantic search.

9. Start the Hybrid Chat:
   python hybrid_chat.py
   Enter your travel questions interactively.
   Type quit or exit to end the chat.

## Data Preparation
The system expects a JSON file named vietnam_travel_dataset.json with entries like:
[
  {
    "city": "Hanoi",
    "title": "Hoan Kiem Lake",
    "description": "A scenic lake in the heart of Hanoi with historic significance."
  }
]

## Contributing
1. Fork the repository
2. Create a feature branch:
   git checkout -b feature/AmazingFeature
3. Commit your changes:
   git commit -m "Add AmazingFeature"
4. Push to the branch:
   git push origin feature/AmazingFeature
5. Open a Pull Request
