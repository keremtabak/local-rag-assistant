from rank_bm25 import BM25Okapi
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def hybrid_search(question, documents, embedding_model, top_k=3):
    """
    documents: [(id, filename, chunk, embedding), ...] listesi
    """
    if not documents:
        return []

    chunks = [doc[2] for doc in documents]
    embeddings = [doc[3] for doc in documents]
    
    # Eğer veritabanında embedding henüz hesaplanmamışsa (güvenlik önlemi)
    if embeddings[0] is None:
        embeddings = embedding_model.encode(chunks)
    else:
        embeddings = np.array(embeddings)

    # 1. BM25 (Anahtar Kelime) Araması
    tokenized_corpus = [chunk.lower().split(" ") for chunk in chunks]
    bm25 = BM25Okapi(tokenized_corpus)
    tokenized_query = question.lower().split(" ")
    bm25_scores = bm25.get_scores(tokenized_query)
    
    # BM25 skorlarını normalize et (0 ile 1 arasına çek)
    max_bm25 = max(bm25_scores) if len(bm25_scores) > 0 and max(bm25_scores) > 0 else 1.0
    normalized_bm25 = bm25_scores / max_bm25

    # 2. Vektör (Anlam) Benzerliği Araması
    question_embedding = embedding_model.encode(question)
    cosine_scores = cosine_similarity([question_embedding], embeddings)[0]

    # 3. Hibrit Skorlama (%50 BM25 + %50 Vektör)
    hybrid_scores = 0.5 * normalized_bm25 + 0.5 * cosine_scores

    # En yüksek skora sahip sonuçları sırala
    scored_results = list(zip(hybrid_scores, chunks))
    scored_results.sort(key=lambda x: x[0], reverse=True)

    # En iyi top_k sonucu döndür
    return [chunk for score, chunk in scored_results[:top_k]]