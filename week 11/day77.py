from dotenv import load_dotenv
import os
from openai import OpenAI
from pinecone import Pinecone

load_dotenv("AS.txt")

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("luigi-menu")


documents = [
    { "text": "Margherita pizza is €10, made with tomato sauce and mozzarella. BBQ Chicken pizza is €13, topped with grilled chicken and red onion. Garlic bread is €4 and comes with a dipping sauce.", "doc_type": "menu" },
    { "text": "Luigis pizzaria is open from 1pm to 1am,it is located at 123 main street dublin 1, it does delivery to surrounding areas",  "doc_type": "faq"  },
    { "text": "If you are not satisfied with your purchase, you can return it within 2 hours  for a full refund.",  "doc_type": "policy" }
]

def fixed_chunk(text, chunk_size, overlap):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

chunks = fixed_chunk(documents[0]["text"], 100, 20)
print(chunks)

def prepare_chunks(documents):
    results = []
    for document in documents:
        chunks = fixed_chunk(document["text"], 200, 20)
        for i, chunk in enumerate(chunks):
            record = {
                "id": f"{document['doc_type']}_{i:03d}",
                "text": chunk,
                "doc_type": document["doc_type"],
                "chunk_index": i,
                "source": "luigis pizzeria"
            }
            results.append(record)
    return results
all_chunks = prepare_chunks(documents)
print(all_chunks)


def embed_and_upsert(chunks):
    vectors = []
    for chunk in chunks:
        response = openai_client.embeddings.create(
            input=chunk["text"],
            model="text-embedding-ada-002"
        )
        embedding = response.data[0].embedding
        vector = (
            chunk["id"],
            embedding,
            {
                "doc_type": chunk["doc_type"],
                "chunk_index": chunk["chunk_index"],
                "source": "luigis pizzeria",
                "text": chunk["text"]
            }
        )
        vectors.append(vector)
    index.upsert(vectors=vectors)
    print(f"Upserted {len(vectors)} vectors")
embed_and_upsert(all_chunks)

def search_knowledge_base(query, doc_type):
    response = openai_client.embeddings.create(
        input=query,
        model="text-embedding-ada-002"
    )
    query_vector = response.data[0].embedding

    results = index.query(
        vector=query_vector,
        top_k=3,
        include_metadata=True,
        filter={"doc_type": {"$eq": doc_type}}
   )

    for match in results.matches:
        print(f"Score: {match.score:.2f} | {match.metadata['text']}")
    
search_knowledge_base("what pizzas do you have", "menu")
search_knowledge_base("what time are you open", "faq")
search_knowledge_base("can I get a refund", "policy")