import sqlite3
import numpy as np

DB_PATH = "db/rag.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            chunk TEXT,
            embedding BLOB
        )
    """)
    conn.commit()
    conn.close()

def insert_document(filename, chunk, embedding):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Numpy dizisini binary (BLOB) formata çevirerek kaydediyoruz
    embedding_blob = embedding.tobytes()
    cursor.execute("""
        INSERT INTO documents (filename, chunk, embedding)
        VALUES (?, ?, ?)
    """, (filename, chunk, embedding_blob))
    conn.commit()
    conn.close()

def get_documents():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, filename, chunk, embedding FROM documents")
    rows = cursor.fetchall()
    conn.close()
    
    # Blob verilerini tekrar numpy array'e dönüştürüyoruz
    documents = []
    for row in rows:
        doc_id, filename, chunk, emb_blob = row
        embedding = np.frombuffer(emb_blob, dtype=np.float32) if emb_blob else None
        documents.append((doc_id, filename, chunk, embedding))
    return documents

def clear_documents():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM documents")
    conn.commit()
    conn.close()