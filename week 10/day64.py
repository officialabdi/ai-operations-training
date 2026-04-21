from openai import OpenAI
from dotenv import load_dotenv
import numpy as np

load_dotenv("AS.txt")

client = OpenAI()

response = client.embeddings.create(
    input="the best pizza in dublin",
    model="text-embedding-3-small"

)

embedding = response.data[0].embedding

print(f"Type: {type(embedding)}")
print(f"Length: {len(embedding)}")
print(f"First 5 values: {embedding[:5]}")


sentences = [
    "the best pizza in dublin",
    "great places to eat pizza in ireland",
    "how to fix a car engine"
]

embeddings = []
for sentence in sentences:
    result = client.embeddings.create(
        input=sentence,
        model="text-embedding-3-small"
    )
    embeddings.append(result.data[0].embedding)

def cosine_similarity(a, b):
    a = np.array(a)
    b= np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

sim_1_2 = cosine_similarity(embeddings[0], embeddings[1])
sim_1_3 = cosine_similarity(embeddings[0], embeddings[2])

print(f"Pizza vs Pizza Ireland: {sim_1_2:.4f}")
print(f"Pizza vs Car engine:    {sim_1_3:.4f}")
print("\n--- session summary ---")
print(f"embedding model: text-embedding-3-small")
print(f"vector dimensions: {len(embedding)}")
print(f"sentences compared: {len(sentences)}")