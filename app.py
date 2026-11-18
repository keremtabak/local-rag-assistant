import os
import streamlit as st
import ollama
from ingest import read_file, chunk_text
from database import init_db, get_connection, insert_document
from rag import hybrid_search

# Sayfa Konfigürasyonu
st.set_page_config(page_title="Local RAG Assistant", page_icon="🤖", layout="wide")

# Veritabanını Başlat
init_db()

st.title("🤖 Local RAG Assistant")
st.markdown("Belgelerinizi yükleyin ve hibrit arama gücüyle yerel **Qwen** modelinizle sohbet edin.")

# --- SOL MENÜ: Belge Yönetimi ---
st.sidebar.header("📁 Belge Yönetimi")
st.sidebar.text("Desteklenen formatlar: txt, pdf, docx")

uploaded_file = st.sidebar.file_uploader("Bir belge yükleyin", type=["txt", "pdf", "docx"])

if uploaded_file is not None:
    # Geçici klasöre kaydetme
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", uploaded_file.name)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Veritabanında daha önce işlenmiş mi kontrol et
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM documents WHERE filename = ?", (uploaded_file.name,))
    exists = cursor.fetchone()[0]
    conn.close()
    
    if exists == 0:
        with st.spinner("Belge okunuyor, parçalanıyor ve önbellekleniyor..."):
            try:
                # 1. Dosyayı oku
                text = read_file(file_path)
                # 2. Saf Python ile parçala (chunking)
                chunks = chunk_text(text)
                
                # 3. Parçaları ve embedding'leri veritabanına kaydet
                for chunk in chunks:
                    insert_document(uploaded_file.name, chunk)
                
                st.sidebar.success(f"{uploaded_file.name} başarıyla işlendi ve önbelleklendi!")
            except Exception as e:
                st.sidebar.error(f"Hata oluştu: {e}")
    else:
        st.sidebar.info(f"{uploaded_file.name} zaten veritabanında mevcut.")

# Sohbet Geçmişini Temizleme Butonu
if st.sidebar.button("Sohbet Geçmişini Temizle"):
    st.session_state.messages = []
    st.rerun()

# --- SOHBET ARAYÜZÜ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekranda göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("📌 Kaynak Parçalar (Citations)"):
                for i, src in enumerate(message["sources"]):
                    st.markdown(f"**Kaynak {i+1}:**\n{src}")

# Kullanıcıdan girdi al
query = st.chat_input("Belgeleriniz hakkında bir soru sorun...")

if query:
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Qwen belgede arama yapıyor ve yanıt hazırlıyor..."):
            try:
                # 1. Hibrit Arama ile en alakalı kaynak parçalarını bul
                relevant_chunks = hybrid_search(query, top_k=3)
                
                if not relevant_chunks:
                    response_text = "Bu bilgi belgede bulunamadı."
                    relevant_chunks = []
                else:
                    # 2. Bağlamı oluştur
                    context = "\n\n".join([f"Kaynak {i+1}:\n{chunk}" for i, chunk in enumerate(relevant_chunks)])
                    
                    prompt = f"""Aşağıdaki bağlamı kullanarak kullanıcı sorusunu profesyonel ve detaylı bir şekilde yanıtla. Eğer bilgi bağlamda kesinlikle yoksa "Bu bilgi belgede bulunamadı." de, asla uydurma.

Bağlam:
{context}

Kullanıcı Sorusu: {query}
Yanıt:"""

                    # 3. Ollama üzerinden Qwen modeline bağlan
                    response = ollama.chat(
                        model='qwen2.5:7b',
                        messages=[
                            {'role': 'system', 'content': 'Sen uzman bir teknik analist ve yapay zeka asistanısın. PDF içeriklerini ve akademik makaleleri derinlemesine analiz edersin.'},
                            {'role': 'user', 'content': prompt}
                        ]
                    )
                    response_text = response['message']['content']

                # Yanıtı ekrana bas
                st.markdown(response_text)
                
                if relevant_chunks:
                    with st.expander("📌 Kaynak Parçalar (Citations)"):
                        for i, src in enumerate(relevant_chunks):
                            st.markdown(f"**Kaynak {i+1}:**\n{src}")

                # Asistan mesajını geçmişe kaydet
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response_text,
                    "sources": relevant_chunks if relevant_chunks else []
                })

            except Exception as e:
                error_msg = f"Bir hata oluştu: {e}. Lütfen Ollama uygulamasının açık olduğundan emin ol."
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})