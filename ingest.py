from docx import Document
from pypdf import PdfReader

def read_txt_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
def read_pdf_file(file_path):
    reader = PdfReader(file_path)
    return "\n".join([page.extract_text() for page in reader.pages])
def read_docx_file(file_path):
    doc = Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

if __name__ == "__main__":
    content = read_pdf_file("data/test.pdf.pdf")
    print(content)