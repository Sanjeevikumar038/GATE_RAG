import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from groq import Groq
from utils import extract_text_from_pdf, chunk_text

# ======================
# CONFIG
# ======================

MODEL_NAME = "llama-3.1-8b-instant"

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ======================
# CORRECT CLOUD SAFE PATH
# ======================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, "data")

print("📚 Loading PDFs from:", DATA_FOLDER)

# ======================
# LOAD ALL PDF TEXT
# ======================

all_text = ""

for root, dirs, files in os.walk(DATA_FOLDER):
    for file in files:
        if file.lower().endswith(".pdf"):
            path = os.path.join(root, file)
            print("Loading:", path)

            try:
                text = extract_text_from_pdf(path)
                if text:
                    all_text += text + "\n"
            except Exception as e:
                print("⚠️ PDF error:", e)

chunks = chunk_text(all_text)

# ⭐ CRITICAL CLOUD FALLBACK
if len(chunks) == 0:
    print("⚠️ No text extracted. Using fallback chunk.")
    chunks = ["GATE syllabus includes OS, DBMS, CN, Algorithms, Data Structures, Mathematics."]

print("✅ Total chunks:", len(chunks))

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

    try:
        q_vec = embed_model.encode([query])
        D, I = index.search(np.array(q_vec).astype("float32"), k)

        results = []
        for idx in I[0]:
            if idx < len(chunks):
                results.append(chunks[idx][:1000])

        return results

    except:
        return chunks[:2]


# ======================
# GROQ STREAM
# ======================

def stream_answer(prompt):

    try:
        completion = groq_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=700,
            stream=True
        )

        for chunk in completion:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    except Exception as e:
        yield f"\n⚠️ AI Error: {str(e)}"


# ======================
# MAIN FUNCTION
# ======================

def ask_gate_question_stream(query, chat_history):

    query = query.strip()

    if query.lower() in ["hi", "hello", "hey"]:
        def greet():
            yield "Hello 👋 I am your GATE AI assistant. Ask about syllabus, previous papers, trends or mock tests."
        return greet(), []

    context_chunks = retrieve(query)

    context_text = "\n\n".join(context_chunks)

    prompt = f"""
You are a smart GATE exam mentor AI.

Use ONLY the context below.

If answer not found → politely say you don't have enough info.

Context:
{context_text}

User Question:
{query}

Answer clearly:
"""

    return stream_answer(prompt), context_chunks