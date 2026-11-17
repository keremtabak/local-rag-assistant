from sentence_transformers import SentenceTransformer
from database import get_documents
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi

from foundry_local_sdk import Configuration
from foundry_local_sdk import FoundryLocalManager

# 1. Modeli ve Verileri Yükle
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded successfully")

documents = get_documents()
chunks = [document[2] for document in documents]

embeddings = model.encode(chunks)

# BM25 için metinleri kelimelerine ayırıyoruz (Tokenization)
tokenized_chunks = [chunk.lower().split(" ") for chunk in chunks]
bm25 = BM25Okapi(tokenized_chunks)

print("Chunk Sayısı:", len(chunks))
print("Embedding Sayısı:", len(embeddings))

def hybrid_retrieve(query, top_k=3, alpha=0.5):
    """
    Hibrit Arama: Vektör Benzerliği (Cosine Similarity) ile 
    Kelime Tabanlı Aramayı (BM25) harmanlar.
    """
    # Vektör Arama Skorları
    question_embedding = model.encode(query)
    vector_scores = cosine_similarity([question_embedding], embeddings)[0]
    
    # BM25 Skorları
    tokenized_query = query.lower().split(" ")
    bm25_scores = bm25.get_scores(tokenized_query)
    
    # Skorları Normalize Et (0 ile 1 arasına çek)
    if max(vector_scores) > min(vector_scores):
        norm_vector = (vector_scores - min(vector_scores)) / (max(vector_scores) - min(vector_scores))
    else:
        norm_vector = vector_scores
        
    if max(bm25_scores) > min(bm25_scores):
        norm_bm25 = (bm25_scores - min(bm25_scores)) / (max(bm25_scores) - min(bm25_scores))
    else:
        norm_bm25 = bm25_scores

    # Hibrit Skor Hesaplama (Alpha ağırlıklı ortalama)
    hybrid_scores = alpha * norm_vector + (1 - alpha) * norm_bm25

    # Skorları ve chunk'ları eşleştir ve sırala
    results = sorted(zip(hybrid_scores, chunks), key=lambda x: x[0], reverse=True)

    # En iyi sonuçları birleştir
    context = "\n\n".join(chunk for score, chunk in results[:top_k])
    return context

# 2. Foundry Local SDK Yapılandırması (Yollar C:\ sürücüsüne uyarlandı)
config = Configuration(
    app_name="local-rag-assistant",
    app_data_dir=r"C:\Users\kerem\local-rag-assistant\ai_data\foundry",
    model_cache_dir=r"C:\Users\kerem\local-rag-assistant\ai_data\models",
    logs_dir=r"C:\Users\kerem\local-rag-assistant\ai_data\logs"
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

# 3. Sohbet Döngüsü
while True:
    question = input("\nSorunuzu girin (çıkmak için q): ")
    if question.lower() == "q":
        break

    # Hibrit arama ile bağlamı çek
    context = hybrid_retrieve(question)

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