import os
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

load_dotenv("AS.txt")

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("luigi-menu")

menu_items = [

    {"id": "item-001", "text": "margherita pizza", "category": "pizza", "price": 10.99},
    {"id": "item-002", "text": "garlic bread", "category": "starter", "price": 4.50},
    {"id": "real-001", "text": "Margherita pizza with fresh mozzarella", "category": "pizza", "price": 10.99},
    {"id": "real-002", "text": "Garlic bread with herb butter", "category": "starter", "price": 4.50},
    {"id": "real-003", "text": "Tiramisu dessert with espresso", "category": "dessert", "price": 6.00},
]

def search_with_threshold(query, top_k, threshold=0.1):
    response = openai_client.embeddings.create(
        input=query,
        model="text-embedding-ada-002"
    )
    query_vector = response.data[0].embedding

    results = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True
    )
    
    filtered = []
    for match in results.matches:
        if match.score >= threshold:
            filtered.append(match)

    if len(filtered) == 0:
            print("no strong match found")
    else:  
            return filtered

    

def keyword_search(query, items):
    query_words = query.lower().split()
    results = []
    for item in items:
        item_text = item["text"].lower()
        if any(word in item_text for word in query_words):
            results.append(item)
    return results
    

def semantic_search(query):
    response = openai_client.embeddings.create(
        input=query,
        model="text-embedding-ada-002"
    )
    query_vector = response.data[0].embedding

    results = index.query(
        vector=query_vector,
        top_k=5,
        include_metadata=True
    )
    return results.matches

query = "something light and vegetarian"



print("\n--- THRESHOLD SEARCH RESULTS ---")
threshold_results = search_with_threshold(query,top_k=5, threshold=0.1)
if threshold_results:
    for match in threshold_results:
        print(f"  Score: {round(match.score, 4)} | {match.metadata.get('text', 'no text')}")


print("=" * 50)
print(f"QUERY: '{query}'")
print("=" * 50)

print("\n--- KEYWORD SEARCH RESULTS ---")
kw_results = keyword_search(query, menu_items)
if kw_results:
    for item in kw_results:
        print(f"  {item['text']} | {item['category']} | €{item['price']}")
else:
    print("  No results found.")

print("\n--- SEMANTIC SEARCH RESULTS ---")
sem_results = semantic_search(query)
if sem_results:
    for match in sem_results:
        print(f"  Score: {round(match.score, 4)} | {match.metadata.get('text', 'no text')} | €{match.metadata.get('price', '?')}")
else:
    print("  No results found.")