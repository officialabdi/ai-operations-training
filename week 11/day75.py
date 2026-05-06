import os
import time
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

load_dotenv("AS.txt")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("luigi-menu")


embedding_cache = {}

def get_embedding(text):
    if text in embedding_cache:
        print(f"[cache hit] '{text}'")
        return list(embedding_cache[text])
    print(f"[api_call] '{text}'")
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    vector = list(response.data[0].embedding)
    embedding_cache[text] = vector
    return vector

phrase = "vegetarian pasta"

get_embedding(phrase) 
get_embedding(phrase)  

test_vector = get_embedding("grilled chicken sandwich")

index.upsert(
    vectors=[{
        "id": "lunch-001",
        "values": test_vector,
        "metadata": {"item": "grilled chicken sandwich", "category": "lunch"}

    }],
    namespace="lunch"
)

print("upserted into lunch namespace")

query_vector = get_embedding("chicken lunch option")

results = index.query(
    vector=query_vector,
    top_k=3,
    namespace="lunch",
    include_metadata=True
)

print("namespace query results:")
for match in results["matches"]:
    print(f"   {match['metadata']['item']} - score: {match['score']:.4f}")


menu_items = [
    "pepperoni pizza",
    "margherita pizza",
    "caesar salad",
    "garlic bread",
    "tiramisu"
]

batch = []

for i, item in enumerate(menu_items):
    vector = get_embedding(item)
    batch.append({
        "id": f"menu-{i:03d}",
        "values": vector,
        "metadata": {"item": item}

    })
index.upsert(vectors=batch, namespace="dinner")
print(f"batch upserted: {len(batch)} items in one request")

query_vector = get_embedding("pizza")


start = time.time()
results_high = index.query(vector=query_vector, top_k=10, namespace="dinner", include_metadata=True)
end = time.time()
print(f"top_k=10 — {len(results_high['matches'])} results — {end - start:.4f}s")

start = time.time()
results_low = index.query(vector=query_vector, top_k=2, namespace="dinner", include_metadata=True)
end = time.time()
print(f"top_k=2  — {len(results_low['matches'])} results — {end - start:.4f}s")

print(f"Closest match: {results_low['matches'][0]['metadata']['item']}")


def timed_search(query_text, namespace, top_k=3):
    vector = get_embedding(query_text)
    
    start = time.time()
    results = index.query(
        vector=vector,
        top_k=top_k,
        namespace=namespace,
        include_metadata=True
    )
    end = time.time()
    
    duration = end - start
    print(f"[SEARCH] '{query_text}' | namespace: {namespace} | top_k: {top_k} | time: {duration:.4f}s")
    
    return results
timed_search("pasta dish", "dinner")
timed_search("something with cheese", "dinner")
timed_search("chicken lunch option", "lunch")