import streamlit as st
from sentence_transformers import SentenceTransformer

from database import get_documents, clear_documents, insert_document
from ingest import read_file, chunk_text
from rag import hybrid_search

from foundry_local_sdk import Configuration
from foundry_local_sdk import FoundryLocalManager


@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


@st.cache_resource
def load_chat_client():
    config = Configuration(
        app_name="local-rag-assistant",
        app_data_dir=r"C:\Users\kerem\local-rag-assistant\ai_data\foundry",
        model_cache_dir=r"C:\Users\kerem\local-rag-assistant\ai_data\models",
        logs_dir=r"C:\Users\kerem\local-rag-assistant\ai_data\logs"
    )

    manager = FoundryLocalManager(config)

    for model in manager.catalog.list_models():
        if model.alias == "phi-4-mini":
            model.download()
            model.load()
            return model.get_chat_client()

    return None


embedding_model = load_embedding_model()
client = load_chat_client()

st.set_page_config(
    page_title="Local RAG Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Local RAG Assistant")
st.write("Belgelerinizi yükleyin ve hibrit arama gücüyle yerel yapay zeka modelinizle sohbet edin.")

# Sidebar: Belge Yönetimi
with st.sidebar:
    st.header("📁 Belge Yönetimi")
    uploaded_file = st.file_uploader(
        "Desteklenen formatlar: txt, pdf, docx",
        type=["txt", "pdf", "docx"]
    )

    if uploaded_file:
        file_path = uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        clear_documents()
        text = read_file(file_path)
        chunks = chunk_text(text)

        with st.spinner("Parçalar vektörleştiriliyor ve veritabanına kaydediliyor..."):
            for chunk in chunks:
                # Embedding'i yükleme anında 1 kez hesaplayıp kaydediyoruz!
                embedding = embedding_model.encode(chunk)
                insert_document(file_path, chunk, embedding)

        st.success(f"{uploaded_file.name} başarıyla işlendi ve önbelleklendi!")

    st.markdown("---")
    if st.button("Sohbet Geçmişini Temizle"):
        st.session_state.messages = []
        st.rerun()

# Sohbet Geçmişi Başlatma
if "messages" not in st.session_state:
    st.session_state.messages = []

# Geçmiş mesajları ekranda göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("📄 Kaynak Parçalar (Citations)"):
                for idx, src in enumerate(message["sources"], 1):
                    st.markdown(f"**Kaynak {idx}:**\n> {src}")

# Kullanıcıdan Girdi Al
if question := st.chat_input("Belgeleriniz hakkında bir soru sorun..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Hibrit arama yapılıyor ve yanıt üretiliyor..."):
            documents = get_documents()
            
            if not documents:
                response_text = "Lütfen önce sol menüden bir belge yükleyin."
                sources = []
            else:
                # Hibrit arama ile en iyi 3 parçayı anında bul
                top_chunks = hybrid_search(question, documents, embedding_model, top_k=3)
                context = "\n\n".join(top_chunks)
                sources = top_chunks

                prompt = f"""
Sen profesyonel bir kurumsal belge asistanısın.

Kurallar:
- Yalnızca verilen bağlamı (context) kullan.
- Bağlamda cevap yoksa "Bu bilgi belgede bulunamadı." de.
- Kendi harici bilginle cevap üretme.

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
                response_text = response.choices[0].message.content

            st.markdown(response_text)
            
            if sources:
                with st.expander("📄 Kaynak Parçalar (Citations)"):
                    for idx, src in enumerate(sources, 1):
                        st.markdown(f"**Kaynak {idx}:**\n> {src}")

    st.session_state.messages.append({
        "role": "assistant", 
        "content": response_text,
        "sources": sources if 'sources' in locals() else []
    })