import os
from docx import Document
from pypdf import PdfReader
from database import insert_document, clear_documents, create_table
from langchain_text_splitters import RecursiveCharacterTextSplitter

def read_txt_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def read_pdf_file(file_path):
    reader = PdfReader(file_path)
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

def read_docx_file(file_path):
    doc = Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()])

def read_file(file_path):
    if file_path.endswith(".txt"):
        return read_txt_file(file_path)

    if file_path.endswith(".docx"):
        return read_docx_file(file_path)

    if file_path.endswith(".pdf") or file_path.endswith(".pdf.pdf"):
        return read_pdf_file(file_path)

def chunk_text(text, chunk_size=500, chunk_overlap=50):
    """
    Metni rastgele karakterle bölmek yerine paragraf, cümle ve kelime
    sınırlarına göre akıllıca parçalara ayırır (Recursive Chunking).
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_text(text)
    return chunks

if __name__ == "__main__":
    create_table()  # <--- Tabloların önce oluşması için bunu ekliyoruz
    clear_documents()

    sample_path = "data/sample.txt"
    if os.path.exists(sample_path):
        text = read_file(sample_path)
        chunks = chunk_text(text, 500, 50)

        for chunk in chunks:
            insert_document(
                "sample.txt",
                chunk
            )

        print("Chunk inserted successfully with Recursive Splitter")
    else:
        print(f"{sample_path} bulunamadı, ancak fonksiyonlar hazır.")