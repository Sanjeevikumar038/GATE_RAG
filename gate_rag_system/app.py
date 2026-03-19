import streamlit as st
from rag_engine import ask_gate_question_stream

st.set_page_config(
    page_title="GATE AI Assistant",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Enhanced Custom CSS for modern professional look
st.markdown("""
<style>
    :root {
        --chat-box-width: min(100%, 900px);
        --primary-gradient: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        --secondary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --accent-gradient: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
        --glass-bg: rgba(255, 255, 255, 0.1);
        --glass-border: rgba(255, 255, 255, 0.2);
    }

    /* Professional animated gradient background */
    .stApp {
        background: linear-gradient(-45deg, #1e3c72, #2a5298, #667eea, #764ba2);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        min-height: 100vh;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Modern header with glassmorphism */
    .main-header {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 12px 40px rgba(0,0,0,0.3);
        text-align: center;
        width: var(--chat-box-width);
        margin: 0 auto 2rem auto;
        position: relative;
        overflow: hidden;
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: var(--accent-gradient);
        opacity: 0.05;
    }

    .main-header h1 {
        color: #ffffff;
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
        position: relative;
        z-index: 2;
        letter-spacing: -1px;
    }

    .main-header p {
        color: #e0e7ff;
        font-size: 1.2rem;
        margin-top: 0.75rem;
        font-weight: 500;
        position: relative;
        z-index: 2;
        opacity: 0.9;
    }

    /* Enhanced chat messages */
    .stChatMessage {
        border-radius: 20px !important;
        padding: 1rem 1.25rem !important;
        width: var(--chat-box-width) !important;
        max-width: var(--chat-box-width) !important;
        margin: 0.75rem auto !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15) !important;
        border: none !important;
        backdrop-filter: blur(10px);
        position: relative;
    }

    .stChatMessage:hover {
        box-shadow: 0 6px 20px rgba(0,0,0,0.15) !important;
    }

    /* User message - Modern blue gradient */
    .stChatMessage[data-testid="user"] {
        background: var(--primary-gradient) !important;
        margin-left: auto !important;
        margin-right: auto !important;
        border-radius: 20px 20px 6px 20px !important;
        border: 1px solid rgba(255,255,255,0.1);
        position: relative;
    }

    .stChatMessage[data-testid="user"]::after {
        content: '';
        position: absolute;
        bottom: 0;
        right: 20px;
        width: 0;
        height: 0;
        border-left: 10px solid transparent;
        border-right: 10px solid transparent;
        border-top: 10px solid #667eea;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
    }

    /* Assistant message - Clean white with subtle shadow */
    .stChatMessage[data-testid="assistant"] {
        background: rgba(255, 255, 255, 0.98) !important;
        margin-left: auto !important;
        margin-right: auto !important;
        border-radius: 20px 20px 20px 6px !important;
        border: 1px solid rgba(255,255,255,0.8);
        position: relative;
    }

    .stChatMessage[data-testid="assistant"]::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 20px;
        width: 0;
        height: 0;
        border-left: 10px solid transparent;
        border-right: 10px solid transparent;
        border-top: 10px solid rgba(255, 255, 255, 0.98);
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    }

    /* Enhanced text colors */
    .stChatMessage[data-testid="user"] p,
    .stChatMessage[data-testid="user"] [data-testid="stMarkdownContainer"] {
        color: #ffffff !important;
        font-weight: 500;
        font-size: 1rem;
        line-height: 1.5;
    }

    .stChatMessage[data-testid="assistant"] p,
    .stChatMessage[data-testid="assistant"] [data-testid="stMarkdownContainer"] {
        color: #1a1a1a !important;
        font-weight: 400;
        font-size: 1rem;
        line-height: 1.6;
    }

    /* Modern input container */
    .stChatInputContainer {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 0.75rem;
        width: var(--chat-box-width);
        max-width: var(--chat-box-width);
        margin: 1rem auto;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        position: relative;
    }

    .stChatInputContainer:hover {
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        border-color: var(--glass-border);
    }

    .stChatInputContainer:focus-within {
        box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.3);
    }

    /* Enhanced expander */
    .streamlit-expanderHeader {
        background: var(--secondary-gradient) !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 1rem 1.25rem !important;
        border: none !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px);
    }

    .streamlit-expanderHeader:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.3) !important;
    }

    /* Professional source cards */
    .source-card {
        background: var(--glass-bg);
        backdrop-filter: blur(15px);
        border: 1px solid var(--glass-border);
        padding: 1.25rem;
        border-radius: 12px;
        margin: 0.75rem 0;
        border-left: 4px solid #4facfe;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }

    .source-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: var(--accent-gradient);
        opacity: 0.8;
    }

    .source-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }

    .source-card strong {
        color: #1a1a1a;
        font-weight: 600;
        display: block;
        margin-bottom: 0.5rem;
        font-size: 1rem;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb {
        background: var(--accent-gradient);
        border-radius: 4px;
        transition: background 0.3s ease;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-gradient);
    }

    /* Loading spinner enhancement */
    .stSpinner > div > div {
        border-color: #667eea transparent transparent transparent !important;
        border-width: 3px !important;
    }

    /* Typing indicator */
    .typing::after {
        content: '';
        animation: blink 1.2s infinite;
    }

    @keyframes blink {
        0%, 50% { opacity: 0; }
        51%, 100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# Modern Professional Header
st.markdown("""
<div class="main-header">
    <h1>🎓 GATE AI Assistant</h1>
    <p>Computer Science & Data Science & AI</p>
    <div style="margin-top: 1rem; opacity: 0.8;">
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Chat Memory
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Display Previous Messages
# -----------------------------
for message in st.session_state.messages:
    avatar = "\U0001F464" if message["role"] == "user" else "\U0001F916"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# -----------------------------
# User Input
# -----------------------------
prompt = st.chat_input("💬 Ask me about GATE syllabus, previous papers, or mock tests...")

if prompt:

    # Store user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user", avatar="\U0001F464"):
        st.markdown(prompt)

    # Display assistant response
    with st.chat_message("assistant", avatar="\U0001F916"):
        message_placeholder = st.empty()
        full_response = ""

        with st.spinner("🔍 Searching knowledge base..."):
            stream_generator, sources = ask_gate_question_stream(
                prompt,
                st.session_state.messages
            )

            for chunk in stream_generator:
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    # Show retrieved sources
    if sources:
        with st.expander("📚 **Source Documents** (Click to view references)"):
            for i, src in enumerate(sources, 1):
                st.markdown(
                    f'<div class="source-card">'
                    f'<strong>📄 Source {i}</strong><br>'
                    f'<div style="color: #666; font-size: 0.9em; margin-top: 0.5rem; line-height: 1.4;">{src[:300]}...</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": full_response})
