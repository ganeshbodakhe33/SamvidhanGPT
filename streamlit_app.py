import streamlit as st
import pickle
import time
from src.vector_db import load_index
from src.rag_pipeline import generate_answer

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="SamvidhanGPT",
    page_icon="📜",
    layout="wide"
)

# -----------------------------
# PREMIUM CSS (CHATGPT STYLE)
# -----------------------------
st.markdown("""
<style>
/* Global */
body {
    background-color: #0f172a;
    color: #e5e7eb;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

/* Chat container */
.block-container {
    max-width: 900px;
    margin: auto;
    padding-top: 2rem;
}

/* Chat bubbles */
.chat-bubble-user {
    background-color: #2563eb;
    color: white;
    padding: 12px 16px;
    border-radius: 12px;
    margin-bottom: 10px;
    max-width: 75%;
    margin-left: auto;
    font-size: 15px;
    line-height: 1.6;
}

.chat-bubble-bot {
    background-color: #1e293b;
    color: #e2e8f0;
    padding: 12px 16px;
    border-radius: 12px;
    margin-bottom: 10px;
    max-width: 75%;
    margin-right: auto;
    font-size: 15px;
    line-height: 1.6;
}

/* Typing text */
.typing {
    font-size: 15px;
    line-height: 1.7;
    letter-spacing: 0.2px;
    white-space: pre-wrap;
}

/* Input box */
.stChatInputContainer {
    border-top: 1px solid #334155;
}

/* Footer */
.footer {
    text-align: center;
    font-size: 12px;
    color: #94a3b8;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
<h1 style='text-align:center;'>📜 SamvidhanGPT</h1>
<p style='text-align:center; color:#94a3b8;'>
Understand the Indian Constitution with AI 🇮🇳
</p>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_resource
def load_resources():
    index = load_index("faiss_index.bin")
    with open("chunks.pkl", "rb") as f:
        chunks = pickle.load(f)
    return index, chunks

index, chunks = load_resources()

# -----------------------------
# SESSION STATE
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# TYPING EFFECT (SMOOTH)
# -----------------------------
def type_text(text, speed=0.002):
    placeholder = st.empty()
    typed = ""

    for char in text:
        typed += char
        placeholder.markdown(
            f"<div class='chat-bubble-bot typing'>{typed}▌</div>",
            unsafe_allow_html=True
        )
        time.sleep(speed)

    placeholder.markdown(
        f"<div class='chat-bubble-bot typing'>{typed}</div>",
        unsafe_allow_html=True
    )

# -----------------------------
# DISPLAY CHAT
# -----------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"<div class='chat-bubble-user'>👤 {msg['content']}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div class='chat-bubble-bot'>🤖 {msg['content']}</div>",
            unsafe_allow_html=True
        )

# -----------------------------
# INPUT
# -----------------------------
query = st.chat_input("Ask about Articles, Rights, Amendments...")

if query:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": query})

    # Display user message
    st.markdown(
        f"<div class='chat-bubble-user'>👤 {query}</div>",
        unsafe_allow_html=True
    )

    # Generate response
    with st.spinner("📜 Reading Constitution & thinking..."):
        answer = generate_answer(query, index, chunks)

    # Typing effect
    type_text(answer)

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": answer})

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.markdown("## 📘 About")
    st.markdown("""
    **SamvidhanGPT** is an AI assistant for the Constitution.

    🔹 RAG-based system  
    🔹 Vector search (FAISS)  
    🔹 LLM Powered 

    ---
    👨‍💻 **Author:** Ganesh Bodakhe
    """)

    st.markdown("## 💡 Try asking")
    st.markdown("""
    - What is Article 21?  
    - Explain Fundamental Rights  
    - What is DPSP?  
    """)

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("""
<div class="footer">
Made with ❤️ by Ganesh | SamvidhanGPT
</div>
""", unsafe_allow_html=True)