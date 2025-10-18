# load_to_neo4j.py
from neo4j import GraphDatabase
import json
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

with open("vietnam_travel_dataset.json", "r") as f:
    data = json.load(f)

with driver.session() as session:
    session.run("MATCH (n) DETACH DELETE n")  # clear old data
    for item in data:
        city = item.get("city", "Unknown")
        title = item["title"]
        session.run("""
            MERGE (c:City {name: $city})
            MERGE (a:Activity {name: $title})
            MERGE (c)-[:HAS_ACTIVITY]->(a)
        """, city=city, title=title)

print("✅ Neo4j graph data loaded successfully!")
