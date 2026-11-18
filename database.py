import sqlite3
import os

DB_PATH = "db/rag.db"

def get_connection():
    """Veritabanı bağlantısını döndürür ve db klasörünün varlığını garanti eder"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    """Veritabanı ve tabloları oluşturur"""
    conn = get_connection()
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

def insert_document(filename, chunk):
    """Belge parçasını veritabanına kaydeder"""
    from sentence_transformers import SentenceTransformer
    # Embedding modelini yüklüyoruz
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(chunk)
    embedding_blob = embedding.tobytes()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO documents (filename, chunk, embedding)
        VALUES (?, ?, ?)
    """, (filename, chunk, embedding_blob))
    conn.commit()
    conn.close()