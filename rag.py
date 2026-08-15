from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded successfully")

embedding = model.encode(
    "Bu benim ilk embedding testimdir."
)

print(len(embedding))