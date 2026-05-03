import os
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone


load_dotenv("AS.txt")

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("luigi-menu")

documents = [
    {"id": "item-001", "text": "cheesy pizza with tomato sauce", "metadata": {
        "name": "Cheesy Margherita",
        "category": "pizza",
        "price": 12,
        "available": True
    }},
    {"id": "item-002", "text": "tender and spicy chicken wings", "metadata": {
        "name": "Spicy Chicken Wings",
        "category": "sides",
        "price": 8,
        "available": True
    }},
    {"id": "item-003", "text": "milk, fresh cocoa and creamy shake", "metadata": {
        "name": "Chocolate Milkshake",
        "category": "drinks",
        "price": 5,
        "available": True
    }},
    {"id": "item-004", "text": "freshly baked choc chip cookies", "metadata": {
        "name": "Choc Chip Cookies",
        "category": "dessert",
        "price": 4,
        "available": True
    }},
    {"id": "item-005", "text": "personalised medium pizza with 2 toppings", "metadata": {
        "name": "Build Your Own Pizza",
        "category": "pizza",
        "price": 14,
        "available": True
    }},
    {"id": "item-006", "text": "made with fresh Irish potatoes", "metadata": {
        "name": "Irish Potato Wedges",
        "category": "sides",
        "price": 4,
        "available": True
    }},
    {"id": "item-007", "text": "buns, chicken patty and a slice of cottage cheese", "metadata": {
        "name": "Chicken Cottage Burger",
        "category": "burgers",
        "price": 11,
        "available": True
    }},
    {"id": "item-008", "text": "freshly baked brownies with molten chocolate in the middle", "metadata": {
        "name": "Molten Chocolate Brownie",
        "category": "dessert",
        "price": 5,
        "available": True
    }},
    {"id": "faq-001", "text": "We deliver within 5km of Dublin city centre", "metadata": {
        "name": "Delivery Policy",
        "category": "policy",
        "price": 0,
        "available": True
    }},
    {"id": "faq-002", "text": "Luigi's is open Monday to Sunday from 12pm to 11pm", "metadata": {
        "name": "Opening Hours",
        "category": "policy",
        "price": 0,
        "available": True
    }},
]
def build_knowledge_base(documents):
    for doc in documents:
        id = doc["id"]
        text = doc["text"]
        metadata = doc["metadata"]

        response = openai_client.embeddings.create(
            input=text,
            model="text-embedding-ada-002"
        )
        vector = response.data[0].embedding

        index.upsert(vectors=[(id, vector, metadata)])

        print(f"stored: {id}")

build_knowledge_base(documents)

query_text = "what food do you reccommend?"

response = openai_client.embeddings.create(
    input=query_text,
    model="text-embedding-ada-002"
)

query_vector = response.data[0].embedding

filter = {
    "$and": [
        {"category": {"$eq": "pizza"}},
        {"available": {"$eq": True}}
    ]
}

results = index.query(
    vector=query_vector,
    top_k=3,
    filter=filter,
    include_metadata=True
)

for match in results["matches"]:
    print(match["id"])
    print(match["score"])
    print(match["metadata"])
    print("---")