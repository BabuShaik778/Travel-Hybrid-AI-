# hybrid_chat.py
from openai import OpenAI
from pinecone import Pinecone
from neo4j import GraphDatabase
from config import (
    OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_INDEX_NAME,
    NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
)

client = OpenAI(api_key=OPENAI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def get_graph_context(destination):
    with driver.session() as session:
        query = f"""
        MATCH (c:City {{name: '{destination}'}})-[:HAS_ACTIVITY]->(a:Activity)
        RETURN c.name AS city, a.name AS activity LIMIT 5
        """
        results = session.run(query)
        return [f"{r['city']} - {r['activity']}" for r in results]

def get_vector_context(query_text):
    query_embedding = client.embeddings.create(
        model="text-embedding-3-small", input=query_text
    ).data[0].embedding
    results = index.query(vector=query_embedding, top_k=3, include_metadata=True)
    return [match["metadata"]["description"] for match in results["matches"]]

def generate_response(user_input):
    vector_context = get_vector_context(user_input)
    graph_context = get_graph_context("Vietnam")
    prompt = f"""
You are an expert travel planner. Use the data below to create a detailed, human-like answer.

User Question: {user_input}

Vector Context (Semantic Matches):
{vector_context}

Graph Context (City-Activity Relationships):
{graph_context}

Answer clearly, with an engaging tone, structured by days if it's an itinerary.
"""
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

if __name__ == "__main__":
    print("🌐 Welcome to the Hybrid AI Travel Chat!")
    while True:
        user_input = input("\nEnter your travel question (or 'quit'): ")
        if user_input.lower() in ["quit", "exit"]:
            break
        response = generate_response(user_input)
        print("\n🧳 AI Response:\n", response)
