import os
from docx import Document
from pypdf import PdfReader

def read_txt_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def read_pdf_file(file_path):
    reader = PdfReader(file_path)
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

def read_docx_file(file_path):
    doc = Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()])

def read_file(file_path):
    if file_path.endswith(".txt"):
        return read_txt_file(file_path)
    elif file_path.endswith(".docx"):
        return read_docx_file(file_path)
    elif file_path.endswith(".pdf") or file_path.endswith(".pdf.pdf"):
        return read_pdf_file(file_path)
    raise ValueError(f"Desteklenmeyen dosya formatı: {file_path}")

def chunk_text(text, chunk_size=500, chunk_overlap=50):
    """Saf Python ile harici kütüphane gerektirmeyen metin parçalama fonksiyonu"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - chunk_overlap
    return chunks