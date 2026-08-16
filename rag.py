from sentence_transformers import SentenceTransformer
from database import get_documents
from sklearn.metrics.pairwise import cosine_similarity

from foundry_local_sdk import Configuration
from foundry_local_sdk import FoundryLocalManager


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

    context = "\n\n".join(
        chunk
        for score, chunk in results[:top_k]
    )

    return context


config = Configuration(
    app_name="local-rag-assistant",
    app_data_dir=r"D:\AI\foundry",
    model_cache_dir=r"D:\AI\models",
    logs_dir=r"D:\AI\logs"
)

manager = FoundryLocalManager(config)

client = None

for foundry_model in manager.catalog.list_models():
    if foundry_model.alias == "phi-4-mini":

        print("Phi-4 Mini yükleniyor...")

        foundry_model.load()

        client = foundry_model.get_chat_client()

        print("Phi-4 Mini hazır.")

        break


while True:

    question = input("\nSorunuzu girin (çıkmak için q): ")

    if question.lower() == "q":
        break

    context = retrieve(question)

    prompt = f"""
Aşağıdaki bağlama göre soruyu cevapla.

Bağlam:

{context}

Soru:

{question}
"""

    response = client.complete_chat(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print("\n=== CEVAP ===\n")
    print(response.choices[0].message.content)