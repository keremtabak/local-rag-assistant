import streamlit as st

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from database import get_documents
from database import clear_documents, insert_document

from ingest import read_file, chunk_text

from foundry_local_sdk import Configuration
from foundry_local_sdk import FoundryLocalManager


@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


@st.cache_resource
def load_chat_client():

    config = Configuration(
        app_name="local-rag-assistant",
        app_data_dir=r"D:\AI\foundry",
        model_cache_dir=r"D:\AI\models",
        logs_dir=r"D:\AI\logs"
    )

    manager = FoundryLocalManager(config)

    for model in manager.catalog.list_models():
        if model.alias == "phi-4-mini":

            model.load()

            return model.get_chat_client()

    return None


embedding_model = load_embedding_model()
client = load_chat_client()

st.title("🤖 Local RAG Assistant")

uploaded_file = st.file_uploader(
    "Dosya yükleyin",
    type=["txt", "pdf", "docx"]
)

if uploaded_file:

    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    clear_documents()

    text = read_file(uploaded_file.name)

    chunks = chunk_text(text)

    for chunk in chunks:
        insert_document(
            uploaded_file.name,
            chunk
        )

    st.success(
        f"{uploaded_file.name} başarıyla işlendi."
    )

question = st.text_input(
    "Sorunuzu girin:"
)

if question:

    documents = get_documents()

    chunks = [document[2] for document in documents]

    embeddings = embedding_model.encode(chunks)

    question_embedding = embedding_model.encode(question)

    results = []

    for i, embedding in enumerate(embeddings):

        score = cosine_similarity(
            [question_embedding],
            [embedding]
        )

        similarity = score[0][0]

        results.append(
            (similarity, chunks[i])
        )

    results.sort(reverse=True)

    context = "\n\n".join(
        chunk
        for score, chunk in results[:3]
    )

   prompt = f"""
Sen bir belge asistanısın.

Kurallar:

- Yalnızca verilen bağlamı kullan.
- Bağlamda cevap yoksa "Bu bilgi belgede bulunamadı." de.
- Kendi bilginle cevap üretme.

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

    st.subheader("Cevap")

    st.write(
        response.choices[0].message.content
    )

    with st.expander("Kullanılan Bağlam"):
        st.write(context)