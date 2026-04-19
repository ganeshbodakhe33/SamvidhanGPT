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
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# 🔥 ULTRA-PREMIUM CSS STYLING
# -----------------------------
st.markdown("""
<style>
/* 1. IMPORT PREMIUM FONTS */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* 2. GLOBAL OVERRIDES */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    background-color: #0B1120; /* Deep rich navy/black */
    color: #F1F5F9;
}

/* Hide default Streamlit header and footer for a clean app look */
header[data-testid="stHeader"] { display: none; }
footer[data-testid="stFooter"] { display: none; }

/* 3. CUSTOM SCROLLBAR */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: #0B1120;
}
::-webkit-scrollbar-thumb {
    background: #1E293B;
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: #334155;
}

/* 4. MAIN CONTAINER SPACING */
.block-container {
    max-width: 1000px !important;
    margin: auto;
    padding-top: 2rem !important;
    padding-bottom: 5rem !important;
}

/* 5. HEADER DESIGN (GLASSMORPHISM & GRADIENTS) */
.custom-header {
    text-align: center;
    padding: 30px 20px;
    margin-bottom: 40px;
    background: rgba(30, 41, 59, 0.4);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 24px;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    animation: fadeInDown 0.8s ease-out;
}

.custom-header h1 {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 10px;
    background: linear-gradient(135deg, #38BDF8 0%, #34D399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
}

.custom-header p {
    color: #94A3B8;
    font-size: 16px;
    font-weight: 400;
    margin: 0;
    letter-spacing: 0.5px;
}

/* 6. CHAT ROW ANIMATIONS & LAYOUT */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}

.chat-row {
    display: flex;
    margin: 24px 0;
    align-items: flex-end;
    animation: fadeInUp 0.4s ease-out forwards;
}

.chat-row.user {
    justify-content: flex-end;
    flex-direction: row-reverse;
}

.chat-row.bot {
    justify-content: flex-start;
}

/* 7. AVATAR DESIGN */
.avatar {
    margin: 0 16px;
    font-size: 22px;
    height: 44px;
    width: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    flex-shrink: 0;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    transition: transform 0.2s ease;
}

.chat-row:hover .avatar {
    transform: scale(1.05);
}

.user .avatar {
    background: linear-gradient(135deg, #1E3A8A, #2563EB);
    border: 2px solid #3B82F6;
}

.bot .avatar {
    background: linear-gradient(135deg, #0F172A, #1E293B);
    border: 2px solid #334155;
}

/* 8. MESSAGE BUBBLES */
.bubble {
    padding: 16px 24px;
    border-radius: 20px;
    max-width: 75%;
    font-size: 16px;
    line-height: 1.7;
    position: relative;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    word-wrap: break-word;
}

/* USER BUBBLE */
.user .bubble {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
    color: #FFFFFF;
    border-bottom-right-radius: 4px; /* iOS style flat corner */
    border: 1px solid #3B82F6;
}

/* BOT BUBBLE */
.bot .bubble {
    background: #1E293B;
    color: #E2E8F0;
    border-bottom-left-radius: 4px; /* iOS style flat corner */
    border: 1px solid #334155;
}

/* 9. TYPING ANIMATION (BLINKING CURSOR) */
@keyframes blink {
    0%, 100% { opacity: 1; text-shadow: 0 0 8px #38BDF8; }
    50% { opacity: 0; }
}

.typing-cursor {
    display: inline-block;
    color: #38BDF8;
    animation: blink 1s step-end infinite;
    font-weight: 800;
    margin-left: 2px;
}

.typing {
    white-space: pre-wrap;
}

/* 10. OVERRIDE STREAMLIT CHAT INPUT */
div[data-testid="stChatInput"] {
    background-color: #0F172A !important;
    border: 1px solid #334155 !important;
    border-radius: 16px !important;
    padding: 2px !important;
    box-shadow: 0 -10px 40px rgba(11, 17, 32, 0.8) !important;
}
div[data-testid="stChatInput"]:focus-within {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3), 0 -10px 40px rgba(11, 17, 32, 0.8) !important;
}
div[data-testid="stChatInput"] textarea {
    color: #F1F5F9 !important;
}

/* 11. SIDEBAR & FOOTER STYLING */
section[data-testid="stSidebar"] {
    background-color: #090E17 !important;
    border-right: 1px solid #1E293B !important;
}
.sidebar-box {
    background: #1E293B;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #334155;
    margin-bottom: 20px;
    font-size: 14px;
    color: #94A3B8;
}
.sidebar-box ul {
    padding-left: 20px;
    margin-top: 10px;
}
.sidebar-box li {
    margin-bottom: 8px;
}

.custom-footer {
    text-align: center;
    color: #475569;
    font-size: 13px;
    margin-top: 60px;
    padding: 20px 0;
    border-top: 1px solid #1E293B;
}

/* RESPONSIVE DESIGN */
@media (max-width: 768px) {
    .bubble { max-width: 85%; font-size: 15px; padding: 14px 18px; }
    .custom-header h1 { font-size: 32px; }
    .avatar { height: 36px; width: 36px; font-size: 18px; margin: 0 10px; }
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
<div class="custom-header">
    <h1>📜 SamvidhanGPT</h1>
    <p>Understand the Indian Constitution with cutting-edge AI 🇮🇳</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA (Cached)
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
# 🔥 PERFECT STREAMING FIX (POLISHED)
# -----------------------------
def stream_response(text):
    placeholder = st.empty()
    output = ""

    # Streaming Loop with Blinking Cursor
    for char in text:
        output += char
        placeholder.markdown(f"""
        <div class="chat-row bot">
            <div class="avatar">🤖</div>
            <div class="bubble typing">{output}<span class="typing-cursor">▌</span></div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.003) # Streaming speed

    # Final output without the cursor
    placeholder.markdown(f"""
    <div class="chat-row bot">
        <div class="avatar">🤖</div>
        <div class="bubble typing">{output}</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# DISPLAY CHAT HISTORY
# -----------------------------
for msg in st.session_state.messages:
    role = "user" if msg["role"] == "user" else "bot"
    avatar = "👤" if role == "user" else "🤖"

    st.markdown(f"""
    <div class="chat-row {role}">
        <div class="avatar">{avatar}</div>
        <div class="bubble">{msg['content']}</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# INPUT & LOGIC
# -----------------------------
query = st.chat_input("Ask about Articles, Rights, Amendments...")

if query:
    # 1. DISPLAY USER MESSAGE IMMEDIATELY
    st.session_state.messages.append({"role": "user", "content": query})

    st.markdown(f"""
    <div class="chat-row user">
        <div class="avatar">👤</div>
        <div class="bubble">{query}</div>
    </div>
    """, unsafe_allow_html=True)

    # 2. GENERATE RESPONSE
    with st.spinner("📜 Searching the Constitution..."):
        answer = generate_answer(query, index, chunks)

    # 3. STREAM THE RESPONSE
    stream_response(answer)

    # 4. SAVE TO SESSION STATE
    st.session_state.messages.append({"role": "assistant", "content": answer})

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.markdown("## 📘 SamvidhanGPT")
    
    st.markdown("""
    <div class="sidebar-box">
        <b>Engine Specifications:</b>
        <ul>
            <li>🔹 Vector DB: <b>FAISS</b></li>
            <li>🔹 Architecture: <b>RAG</b></li>
            <li>🔹 Speed: <b>Ultra-fast</b></li>
        </ul>
        <hr style="border-color: #334155; margin: 15px 0;">
        👨‍💻 Built by <b>Ganesh Bodakhe</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 💡 Suggested Queries")
    st.markdown("""
    <div class="sidebar-box" style="background: transparent; border: none; padding: 0;">
        <ul style="color: #60A5FA; list-style-type: square;">
            <li>What is Article 21?</li>
            <li>Explain Fundamental Rights</li>
            <li>What is DPSP?</li>
            <li>How is the President elected?</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.write("") # Spacer
    if st.button("🧹 Clear Chat History", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.rerun()

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("""
<div class="custom-footer">
    SamvidhanGPT • Advanced Legal RAG System • Built by Ganesh 🚀
</div>
""", unsafe_allow_html=True)