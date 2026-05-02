from openai import OpenAI
from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv("AS.txt")

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("luigi-menu")





document = """
Luigi's Pizzeria has been serving Dublin since 1987. We use only fresh ingredients sourced locally every morning. Our dough is hand-stretched and proved for 24 hours. We offer gluten-free bases on request. Our most popular pizza is the Margherita. We also serve calzone, pasta, and tiramisu. Delivery is available within 5km. Orders under 20 euro have a 2 euro delivery charge. We are open Monday to Sunday from 12pm to 11pm. Reservations are recommended on weekends.
"""

def fixed_chunk(text, chunk_size, overlap):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

chunks = fixed_chunk(document, 100, 20)


def sentence_chunk(text, max_size):
    sentences = text.split(". ")
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_size:
            current_chunk += sentence + ". "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

sentence_chunks = sentence_chunk(document, 100)


def embed_text(text):
    response = openai_client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

for i, chunk in enumerate(sentence_chunks):
    vector = embed_text(chunk)
    index.upsert(vectors=[{
        "id": f"day71-chunk-{i}",
        "values": vector,
        "metadata": {"text": chunk}

    }])
    print(f"uploaded chunk {i+1}: {chunk[:50]}...")


for i, chunk in enumerate(chunks):
    print(f"chunk {i+1}: {chunk}")
    print("---")
for i, chunk in enumerate(sentence_chunks):
    print(f"Chunk {i+1}: {chunk}")
    print("---")




