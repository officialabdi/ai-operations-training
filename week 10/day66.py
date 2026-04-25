from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os 

load_dotenv("AS.txt")

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

print("CONNECTED TO PINECONE")

pc.create_index(
    name="luigi-menu",
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region="us-east-1")
    
)
print("index created: luigi-menu")
