from openai import OpenAI
from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv("AS.txt")

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("luigi-menu")

def get_embedding(text):
    response = openai_client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

margherita_vector = get_embedding("classic tomato and mozzarella pizza")
garlic_vector = get_embedding("toasted bread with garlic butter")



index.upsert(vectors=[
    {
        "id": "margherita-pizza",
        "values": margherita_vector,
        "metadata":{
            "name": "margherita pizza",
            "category": "pizza",
            "price": 10.50
        }
    },
    {
        "id": "garlic-bread",
        "values": garlic_vector,
        "metadata":{
            "name": "garlic bread",
            "category": "sides",
            "price": 4.00
        }
    }
])
print("upserted: margherita-pizza")
print("upserted: garlic bread")

index.upsert(vectors=[
    {
        "id": "margherita-pizza",
        "values": margherita_vector,
        "metadata": {
            "name": "margherita pizza",
            "category": "pizza",
            "price": 11.50
        }
    }
])



print("updated: margherita-pizza price to 11.50")


result = index.fetch(ids=["margherita-pizza"])
record = result.vectors["margherita-pizza"]
print(record.metadata["name"])
print(record.metadata["category"])
print(record.metadata["price"])

index.delete(ids=["garlic-bread"])
print("deleted: garlic-bread")

result = index.fetch(ids=["garlic-bread"])
print(result.vectors)

stats = index.describe_index_stats()
print(stats)

print("Total vectors:", stats["total_vector_count"])
print("Dimensions:", stats["dimension"])

index.update(id="margherita-pizza", set_metadata={"price": 12.00})
print("metadata updated: margherita-pizza price to 12.00")

result = index.fetch(ids=["margherita-pizza"])
record = result.vectors["margherita-pizza"]
print(record.metadata["name"])
print(record.metadata["price"])

