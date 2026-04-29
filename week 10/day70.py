import os
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

load_dotenv("AS.txt")

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("luigi-menu")








documents = [
    {"id": "item-001", "text": "cheesy pizza with tomato sauce", "metadata": {"category": "menu", "text": "cheesy pizza with tomato sauce"}},
    {"id": "item-002", "text": "tender and spicy chicken wings", "metadata": {"category": "menu", "text": "tender and spicy chicken wings"}},
    {"id": "item-003", "text": "milk, fresh cocoa and creamy shake", "metadata": {"category": "drinks", "text": "milk, fresh cocoa and creamy shake"}},
    {"id": "item-004", "text": "freshly baked choc chip cookies", "metadata": {"category": "sides", "text": "freshly baked choc chip cookies"}},
    {"id": "item-005", "text": "personalised medium pizza with 2 toppings", "metadata": {"category": "menu", "text": "personalised medium pizza with 2 toppings"}},
    {"id": "item-006", "text": "made with fresh Irish potatoes", "metadata": {"category": "sides", "text": "made with fresh Irish potatoes"}},
    {"id": "item-007", "text": "buns, chicken patty and a slice of cottage cheese", "metadata": {"category": "menu", "text": "buns, chicken patty and a slice of cottage cheese"}},
    {"id": "item-008", "text": "freshly baked brownies with molten chocolate in the middle", "metadata": {"category": "dessert", "text": "freshly baked brownies with molten chocolate in the middle"}},
    {"id": "faq-001", "text": "We deliver within 5km of Dublin city centre", "metadata": {"category": "policy", "text": "We deliver within 5km of Dublin city centre"}},
    {"id": "faq-002", "text": "Luigi's is open Monday to Sunday from 12pm to 11pm", "metadata": {"category": "policy", "text": "Luigi's is open Monday to Sunday from 12pm to 11pm"}},
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

def search_knowledge_base(query, threshold=0.75):
    response = openai_client.embeddings.create(
        input=query,
        model="text-embedding-ada-002"
    )
    query_vector = response.data[0].embedding

    results = index.query(
        vector=query_vector,
        top_k=3,
        include_metadata=True
    )
    
    found = False
    for match in results.matches:
        if match.score >= threshold:
            print(f"Score: {match.score:.2f} | {match.metadata['text']}")
            found = True

    if not found:
        print("No relevant results found")


print("luigis knowledge base - type 'quit' to exit")
while True:
    query = input("\nyou:")
    if query.lower() == "quit":
        break
    search_knowledge_base(query)
        