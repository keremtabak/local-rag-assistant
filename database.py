import sqlite3


def create_connection():
    connection = sqlite3.connect("db/rag.db")
    return connection


def create_table():
    connection = create_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            chunk_text TEXT
        )
    """)

    connection.commit()
    connection.close()

def insert_document(file_name, chunk_text):
    connection = create_connection()

    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO documents (file_name, chunk_text) VALUES (?, ?)",
        (file_name, chunk_text)
    )

    connection.commit()
    connection.close()
def get_documents():
    connection = create_connection()

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM documents")

    rows = cursor.fetchall()

    connection.close()

    return rows
if __name__ == "__main__":
    create_table()

    documents = get_documents()

    print(documents)