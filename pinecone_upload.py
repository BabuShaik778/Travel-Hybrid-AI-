# pinecone_upload.py
from openai import OpenAI
from tqdm import tqdm
from pinecone import Pinecone, ServerlessSpec
import json
from config import OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_INDEX_NAME

client = OpenAI(api_key=OPENAI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)

# Create index if not exists
if PINECONE_INDEX_NAME not in [i.name for i in pc.list_indexes()]:
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(PINECONE_INDEX_NAME)

with open("vietnam_travel_dataset.json", "r") as f:
    data = json.load(f)

vectors = []
for i, item in enumerate(tqdm(data, desc="Creating embeddings")):
    text = item["description"]
    embedding = client.embeddings.create(model="text-embedding-3-small", input=text).data[0].embedding
    vectors.append({
        "id": str(i),
        "values": embedding,
        "metadata": {"title": item["title"], "description": text}
    })

# Upload in batches
for i in range(0, len(vectors), 100):
    batch = vectors[i:i+100]
    index.upsert(vectors=batch)

print("✅ Embeddings uploaded successfully!")
