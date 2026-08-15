from docx import Document

def read_txt_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
def read_docx_file(file_path):
    doc = Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

if __name__ == "__main__":
    content = read_docx_file("data/test.docx")
    print(content)