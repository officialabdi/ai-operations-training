from openai import OpenAI
from dotenv import load_dotenv
import numpy as np 

load_dotenv("AS.txt")

client = OpenAI()

def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def cosine_similarity(vec_a, vec_b):
    a = np.array(vec_a)
    b = np.array(vec_b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
text_1 = "pepperoni pizza"
text_2 = "cheesy italian pizza"
text_3 = "car insurance quote"

vec_1 = get_embedding(text_1)
vec_2 = get_embedding(text_2)
vec_3 = get_embedding(text_3)

print(f"vector length: {len(vec_1)}")
print(f"first 5 numbers of vec_1: {vec_1[:5]}")

score_1_2 = cosine_similarity(vec_1, vec_2)
score_1_3 = cosine_similarity(vec_1, vec_3)

print(f"\nSimilarity: '{text_1}' vs '{text_2}': {score_1_2:.4f}")
print(f"Similarity: '{text_1}' vs '{text_3}': {score_1_3:.4f}")