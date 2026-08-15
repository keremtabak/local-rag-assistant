from sentence_transformers import SentenceTransformer
from database import get_documents


model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded successfully")

documents = get_documents()

first_chunk = documents[0][2]

embedding = model.encode(first_chunk)

print(len(embedding))
print(embedding[:5])

print(first_chunk)