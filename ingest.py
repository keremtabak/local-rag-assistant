from docx import Document
from pypdf import PdfReader
from database import insert_document

def read_txt_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
def read_pdf_file(file_path):
    reader = PdfReader(file_path)
    return "\n".join([page.extract_text() for page in reader.pages])
def read_docx_file(file_path):
    doc = Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])
def read_file(file_path):
    if file_path.endswith(".txt"):
        return read_txt_file(file_path)

    if file_path.endswith(".docx"):
        return read_docx_file(file_path)

    if file_path.endswith(".pdf") or file_path.endswith(".pdf.pdf"):
        return read_pdf_file(file_path)
def chunk_text(text, chunk_size=500):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks    
if __name__ == "__main__":
    text = read_file("data/sample.txt")

    chunks = chunk_text(text, 500)

    for chunk in chunks:
        insert_document(
        "sample.txt",
        chunk
    )

    print("Chunk inserted successfully")