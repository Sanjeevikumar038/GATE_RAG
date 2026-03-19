import streamlit as st
from rag_engine import ask_gate_question_stream

st.set_page_config(
    page_title="GATE AI Assistant",
    page_icon="\U0001F3AF",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional look
st.markdown("""
<style>
    :root {
        --chat-box-width: min(100%, 900px);
    }

    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        text-align: center;
        width: var(--chat-box-width);
        margin: 0 auto 2rem auto;
        border: 1px solid rgba(255,255,255,0.1);
    }

    .main-header h1 {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .main-header p {
        color: #e0e7ff;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }

    /* Chat container base */
    .stChatMessage {
        border-radius: 18px !important;
        padding: 0.75rem 1rem !important;
        width: var(--chat-box-width) !important;
        max-width: var(--chat-box-width) !important;
        margin: 0.5rem auto !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
        border: none !important;
    }

    /* User message - Right aligned, Blue */
    .stChatMessage[data-testid="user"] {
        background: linear-gradient(135deg, #0084ff 0%, #0066cc 100%) !important;
        margin-left: auto !important;
        margin-right: auto !important;
        border-radius: 18px 18px 4px 18px !important;
    }

    /* Assistant message - Left aligned, White */
    .stChatMessage[data-testid="assistant"] {
        background: rgba(255, 255, 255, 0.95) !important;
        margin-left: auto !important;
        margin-right: auto !important;
        border-radius: 18px 18px 18px 4px !important;
    }

    /* User text color */
    .stChatMessage[data-testid="user"] p,
    .stChatMessage[data-testid="user"] [data-testid="stMarkdownContainer"] {
        color: #ffffff !important;
    }

    /* Assistant text color */
    .stChatMessage[data-testid="assistant"] p,
    .stChatMessage[data-testid="assistant"] [data-testid="stMarkdownContainer"] {
        color: #1a1a1a !important;
    }

    /* Input box */
    .stChatInputContainer {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 0.5rem;
        width: var(--chat-box-width);
        max-width: var(--chat-box-width);
        margin: 0.5rem auto;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white !important;
        border-radius: 8px;
        font-weight: 600;
    }

    /* Source cards */
    .source-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #f5576c;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>\U0001F3AF GATE AI Assistant</h1>
    <p>CSE + Data Science & AI</p>
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
prompt = st.chat_input("Ask anything about GATE CSE/DA syllabus...")

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

        with st.spinner("\U0001F914 Thinking... Searching documents..."):
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
        with st.expander("\U0001F4DA View Retrieved Context Sources"):
            for i, src in enumerate(sources, 1):
                st.markdown(
                    f'<div class="source-card"><strong>\U0001F4C4 Source {i}</strong><br>{src}</div>',
                    unsafe_allow_html=True
                )

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": full_response})
