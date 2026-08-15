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

question = "Bu proje ne geliştirecek?"

question_embedding = model.encode(question)

print("Question Embedding Boyutu:", len(question_embedding))

score = cosine_similarity(
    [question_embedding],
    [embeddings[0]]
)

print("Similarity Score:", score[0][0])