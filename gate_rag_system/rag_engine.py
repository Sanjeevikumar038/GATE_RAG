import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from groq import Groq
from utils import extract_text_from_pdf, chunk_text

# ======================
# CONFIG
# ======================

DATA_FOLDER = "data"
MODEL_NAME = "llama-3.1-8b-instant"

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ======================
# LOAD ALL PDF TEXT
# ======================

print("📚 Loading PDFs...")

all_text = ""

for root, dirs, files in os.walk(DATA_FOLDER):
    for file in files:
        if file.lower().endswith(".pdf"):
            path = os.path.join(root, file)
            print("Loaded:", path)
            all_text += extract_text_from_pdf(path) + "\n"

chunks = chunk_text(all_text)

if len(chunks) == 0:
    raise Exception("No chunks created. Check PDF text extraction.")

print("Total chunks:", len(chunks))

# ======================
# EMBEDDINGS + FAISS
# ======================

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = embed_model.encode(chunks)

dim = embeddings.shape[1]

index = faiss.IndexFlatL2(dim)
index.add(np.array(embeddings).astype("float32"))

print("✅ Vector DB ready")

# ======================
# RETRIEVAL
# ======================

def retrieve(query, k=4):

    q_vec = embed_model.encode([query])
    D, I = index.search(np.array(q_vec).astype("float32"), k)

    results = []
    for idx in I[0]:
        if idx < len(chunks):
            results.append(chunks[idx][:1200])

    return results

# ======================
# GROQ STREAM
# ======================

def stream_answer(prompt):

    completion = groq_client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=800,
        stream=True
    )

    for chunk in completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# ======================
# MAIN FUNCTION
# ======================

def ask_gate_question_stream(query, chat_history):

    if query.lower().strip() in ["hi", "hello", "hey"]:
        def greet():
            yield "Hello 👋 I am your GATE AI assistant. Ask about syllabus, previous papers or mock tests."
        return greet(), []

    context_chunks = retrieve(query)

    context_text = "\n\n".join(context_chunks)

    prompt = f"""
You are an intelligent GATE exam mentor.

Use ONLY the given context to answer.

Rules:
- Answer clearly like ChatGPT
- If answer not in context say politely
- Do not hallucinate

Context:
{context_text}

Question:
{query}

Answer:
"""

    return stream_answer(prompt), context_chunks