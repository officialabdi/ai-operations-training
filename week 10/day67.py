from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv("AS.txt")

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index = pc.Index("luigi-menu")

records = [
    {
        "id": "item-001",
        "values": [0.1] * 1536,
        "metadata": {"text": "margherita pizza", "price": 10.99, "category": "pizza" }
    },
    {
        "id": "item-002",
        "values": [0.2] * 1536,
        "metadata": {"text": "garlic bread", "price": 4.50, "category": "starter" }

    }
]

result = index.upsert(vectors=records)#
print(result)

query_result = index.query(
    vector=[0.1] * 1536,
    top_k=2,
    include_metadata=True
)

print(query_result)

from openai import OpenAI

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed(text):
    response = openai_client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding


menu_items = [
    {"id": "real-001", "text": "Margherita pizza with fresh mozzarella", "price": 10.99, "category": "pizza"},
    {"id": "real-002", "text": "Garlic bread with herb butter", "price": 4.50, "category": "starter"},
    {"id": "real-003", "text": "Tiramisu dessert with espresso", "price": 6.00, "category": "dessert"}
]

real_records = []
for item in menu_items:
    vector = embed(item["text"])
    real_records.append({
        "id": item["id"],
        "values": vector,
        "metadata": {"text": item["text"], "price": item["price"], "category": item["category"]}
    })

index.upsert(vectors=real_records)
print("real records upserted")

search_query = "something sweet to finish my meal"
search_vector = embed(search_query)

search_result = index.query(
    vector=search_vector,
    top_k=1,
    include_metadata=True
)

print(search_result)