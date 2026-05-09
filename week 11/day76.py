import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv("AS.txt")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(os.path.join(BASE_DIR, "luigi_menu.csv"))
print("--- RAW DATA ---")
print(df)
print(f"\nshape: {df.shape}")

df = df.dropna(subset=["item"])
df["item"] = df["item"].str.strip()
df["description"] = df["description"].str.strip()
df =  df.reset_index(drop=True)

print("\n=== cleaned data ===")
print(df)
print(f"\nshape: {df.shape}")

chunks = []
for _, row in df.iterrows():
    chunk = f"{row['item']}: {row['description']}"
    chunks.append(chunk)

print("\n== chunks ===")
for chunk in chunks:
    print("-", chunk)


from openai import OpenAI

client = OpenAI()

print("\n=== embedding chunks ===")
embeddings = []
for chunk in chunks:
    response = client.embeddings.create(
        input=chunk,
        model="text-embedding-ada-002"
    )
    vector = response.data[0].embedding
    embeddings.append({"text": chunk, "vector": vector})
    print(f"embedded: {chunk[:40]}...")
print(f"\ntotal embeddings created: {len(embeddings)}")


from pinecone import Pinecone

pc = Pinecone()
index = pc.Index("luigi-menu")

print("\n=== UPSERTING TO PINECONE ===")
vectors_to_upsert = []
for i, item in enumerate(embeddings):
    vector_id = chunks[i].split(":")[0].strip().replace(" ", "-")
    vectors_to_upsert.append({
        "id": vector_id,
        "values": item["vector"],
        "metadata": {"text": item["text"]}
    })

index.upsert(vectors=vectors_to_upsert)
print(f"✓ Upserted {len(vectors_to_upsert)} vectors to Pinecone")
print("IDs stored:", [v["id"] for v in vectors_to_upsert])



print("\n=== VERIFICATION SEARCH ===")
test_query = "something with cheese"
query_response = client.embeddings.create(
    input=test_query,
    model="text-embedding-ada-002"
)
query_vector = query_response.data[0].embedding

results = index.query(vector=query_vector, top_k=8, include_metadata=True)
print(f"Query: '{test_query}'")
print("Top results:")
for match in results["matches"]:
    print(f"  - {match['id']} (score: {match['score']:.4f})")
    print(f"    {match['metadata'].get('text', 'No text metadata')}")
