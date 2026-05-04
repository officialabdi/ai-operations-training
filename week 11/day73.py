from pinecone import Pinecone
from openai import OpenAI
from dotenv import load_dotenv
import os 

load_dotenv("AS.txt")

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("luigi-menu")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def keyword_score(text, query):
    query_words = query.lower().split()
    text_lower = text.lower()
    matches = sum(1 for word in query_words if word in text_lower)
    return matches / len(query_words)


def hybrid_search(query, alpha=0.7, top_k=5):

    vector = get_embedding(query)
    vector_results = index.query(
        vector=vector,
        top_k=top_k,
        include_metadata=True
    )
    
    blended = []
    for match in vector_results.matches:
        print(match.metadata)
        v_score = match.score
        text = match.metadata.get("text") or match.metadata.get("name") or ""
        k_score = keyword_score(text, query)
        final_score = (alpha * v_score) + ((1 - alpha) * k_score)
        blended.append({
            "id": match.id,
            "text": text,
            "vector_score": round(v_score, 4),
            "keyword_score": round(k_score, 4),
            "final_score": round(final_score, 4)
        })

    blended.sort(key=lambda x: x["final_score"], reverse=True)
    return blended

print("--- Alpha 0.9 (vector heavy) ---")
results = hybrid_search("garlic bread", alpha=0.9)
for r in results:
    print(f"Final: {r['final_score']} | Vector: {r['vector_score']} | Keyword: {r['keyword_score']}")
    print(f"  {r['text']}\n")

print("--- Alpha 0.1 (keyword heavy) ---")
results = hybrid_search("garlic bread", alpha=0.1)
for r in results:
    print(f"Final: {r['final_score']} | Vector: {r['vector_score']} | Keyword: {r['keyword_score']}")
    print(f"  {r['text']}\n")