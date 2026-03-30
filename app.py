# LangChain imports
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from flask import Flask, render_template, request
from groq import Groq
from difflib import SequenceMatcher
import os
import re

app = Flask(__name__)

# ==============================
# 🔑 Groq Setup
# ==============================
client = Groq(api_key=os.getenv("GROQ_API_KEY", "your_groq_api_key_here"))

# ==============================
# 📄 Load and Process PDF (RAG)
# ==============================
loader = PyMuPDFLoader("C:/Users/kalya/Desktop/DEMO JAIN AI/Jain_University_Kanakapura_Advanced.pdf")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

docs = splitter.split_documents(documents)

embeddings = None
db = None

# ==============================
# 💾 Chroma DB (Persistent)
# ==============================
try:
    embeddings = HuggingFaceEmbeddings()

    if os.path.exists("chroma_db"):
        db = Chroma(
            persist_directory="chroma_db",
            embedding_function=embeddings
        )
    else:
        db = Chroma.from_documents(
            docs,
            embeddings,
            persist_directory="chroma_db"
        )
except Exception as exc:
    print(f"Embedding setup failed, using keyword-only retrieval: {exc}")

# ==============================
# 💬 Chat History
# ==============================
chat_history = []

# ==============================
# 🧠 System Prompt
# ==============================
system_prompt = """
You are Jain AI, a helpful academic assistant for Jain University students.

Your role:
- Answer student questions using the provided context first.
- Explain topics in clear, simple, study-friendly language.
- Help with summaries, concept explanations, revision notes, and practice questions.
- Keep answers relevant to academics, university information, syllabus topics, and study material.

Behavior rules:
- If the context contains the answer, use it and stay faithful to it.
- If the context is incomplete, say that clearly instead of guessing.
- Do not invent facts, policies, dates, fees, rankings, or course details.
- If the user asks something outside the available context, politely say you need more source material.
- When useful, format answers with short headings or bullet points.
- Keep the tone friendly, supportive, and easy for students to understand.

Answer style:
- For direct questions, give a short clear answer first.
- For concept questions, explain step by step in simple words.
- For summaries, highlight the most important points only.
- For exam help, provide concise revision-ready notes.
- For practice requests, generate useful questions and model answers based on the context.

Always prioritize accuracy, clarity, and usefulness for the student.
- Never say information is missing when it appears in the provided context.
- For factual questions, give the exact answer in the first sentence.
"""


def keyword_search(query, chunks, limit=3):
    """Fallback retrieval for exact facts and minor-typo queries."""
    keywords = set(re.findall(r"\w+", query.lower()))
    keywords = {word for word in keywords if len(word) > 2}

    scored_chunks = []
    for chunk in chunks:
        content = chunk.page_content.lower()
        content_words = set(re.findall(r"\w+", content))
        score = 0

        for word in keywords:
            if word in content:
                score += 3
                continue

            if any(similar(word, candidate) for candidate in content_words):
                score += 1

        if score:
            scored_chunks.append((score, chunk))

    scored_chunks.sort(key=lambda item: item[0], reverse=True)
    return [chunk for _, chunk in scored_chunks[:limit]]


def similar(left, right):
    if abs(len(left) - len(right)) > 2:
        return False
    return SequenceMatcher(None, left, right).ratio() >= 0.78


def build_context(query):
    retrieved = db.similarity_search(query, k=4) if db else []
    keyword_hits = keyword_search(query, docs, limit=3)

    combined = []
    seen = set()

    for chunk in retrieved + keyword_hits:
        content = chunk.page_content.strip()
        if content and content not in seen:
            seen.add(content)
            combined.append(content)

    return "\n\n".join(combined[:5])


# ==============================
# 🚀 Main Route
# ==============================
@app.route("/", methods=["GET", "POST"])
def home():
    global chat_history

    if request.method == "POST":
        user_input = request.form.get("query")
        file = request.files.get("file")

        # Store user message
        chat_history.append(("user", user_input))

        # 🔍 RAG Retrieval
        context = build_context(user_input)

        # 🧠 Final Prompt
        final_prompt = f"""
{system_prompt}

Context:
{context}

Question:
{user_input}

Answer clearly using the context above. If the answer is present, state the exact value.
"""

        # 🤖 Groq Response
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": final_prompt}
            ]
        )

        bot_reply = response.choices[0].message.content

        # Store bot reply
        chat_history.append(("bot", bot_reply))

    return render_template("index.html", chat_history=chat_history)


if __name__ == "__main__":
    app.run(debug=True)
