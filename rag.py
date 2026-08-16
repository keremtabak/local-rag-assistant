from sentence_transformers import SentenceTransformer
from database import get_documents
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded successfully")

documents = get_documents()

chunks = [document[2] for document in documents]

embeddings = model.encode(chunks)

print("Chunk Sayısı:", len(chunks))
print("Embedding Sayısı:", len(embeddings))

def retrieve(query, top_k=3):
    question_embedding = model.encode(query)

    results = []

    for i, embedding in enumerate(embeddings):
        score = cosine_similarity(
            [question_embedding],
            [embedding]
        )

        similarity = score[0][0]

        results.append(
            (similarity, chunks[i])
        )

    results.sort(reverse=True)

    return results[:top_k]


results = retrieve(
    "Bu proje ne geliştirecek?"
)

for score, chunk in results:
    print("Score:", score)
    print(chunk)
    print("-" * 50)