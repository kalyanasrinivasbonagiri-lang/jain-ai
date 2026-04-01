import base64
import io
import os
import re
from difflib import SequenceMatcher
import fitz
from flask import Flask, render_template, request
from groq import Groq
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from PIL import Image


def candidate_roots():
    here = os.path.dirname(os.path.abspath(__file__))
    roots = []
    current = here
    for _ in range(5):
        roots.append(current)
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    roots.append(os.getcwd())
    return list(dict.fromkeys(roots))


def first_existing_path(*relative_paths):
    for root in candidate_roots():
        for relative_path in relative_paths:
            full_path = os.path.join(root, relative_path)
            if os.path.exists(full_path):
                return full_path
    return os.path.join(candidate_roots()[0], relative_paths[0])


TEMPLATE_DIR = first_existing_path("templates", os.path.join("src", "jain_ai_assistant", "templates"))
DATA_FOLDER = first_existing_path("data", os.path.join("data", "raw", "academics"))
VECTOR_DB_DIR = first_existing_path("chroma_db_openai", os.path.join("storage", "vector_db"))
PROCESSED_FILES_PATH = os.path.join(candidate_roots()[0], "processed_files.txt")

app = Flask(__name__, template_folder=TEMPLATE_DIR)

# ==============================
# Groq Setup
# ==============================
client = Groq()
TEXT_MODEL = "openai/gpt-oss-120b"
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

# ==============================
# Load and Process PDFs (RAG)
# ==============================
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

embeddings = None
db = None
docs = []


def list_pdf_files(folder_path):
    """Return all PDF filenames from the configured data folder."""
    if not os.path.isdir(folder_path):
        print(f"Data folder not found: {folder_path}")
        return []

    try:
        pdf_files = [
            file_name for file_name in os.listdir(folder_path)
            if file_name.lower().endswith(".pdf")
        ]
    except OSError as exc:
        print(f"Could not read data folder '{folder_path}': {exc}")
        return []

    if not pdf_files:
        print(f"No PDF files found in: {folder_path}")

    return sorted(pdf_files)


def load_processed_files():
    """Read the processed file tracker safely."""
    if not os.path.exists(PROCESSED_FILES_PATH):
        return set()

    try:
        with open(PROCESSED_FILES_PATH, "r", encoding="utf-8") as file_obj:
            return {line.strip() for line in file_obj if line.strip()}
    except OSError as exc:
        print(f"Could not read processed files tracker '{PROCESSED_FILES_PATH}': {exc}")
        return set()


def save_processed_files(processed_files):
    """Write the deduplicated set of processed files to disk."""
    try:
        with open(PROCESSED_FILES_PATH, "w", encoding="utf-8") as file_obj:
            for filename in sorted(processed_files):
                file_obj.write(filename + "\n")
    except OSError as exc:
        print(f"Could not write processed files tracker '{PROCESSED_FILES_PATH}': {exc}")


def load_pdfs_by_name(folder_path, file_names):
    """Load the requested PDFs and attach metadata used by retrieval and tracing."""
    loaded_docs = []

    for file_name in sorted(file_names):
        full_path = os.path.join(folder_path, file_name)

        try:
            loader = PyMuPDFLoader(full_path)
            file_docs = loader.load()
        except Exception as exc:
            print(f"Skipping unreadable PDF '{file_name}': {exc}")
            continue

        for index, doc in enumerate(file_docs):
            doc.metadata["source"] = file_name
            doc.metadata["file_path"] = full_path
            doc.metadata["page_number"] = doc.metadata.get("page", index)

        loaded_docs.extend(file_docs)

    return loaded_docs


def load_new_pdfs(folder_path, processed_files):
    """Load only PDFs that have not already been processed."""
    all_pdf_files = list_pdf_files(folder_path)
    new_pdf_files = [file_name for file_name in all_pdf_files if file_name not in processed_files]

    if not new_pdf_files:
        return [], processed_files

    new_docs = load_pdfs_by_name(folder_path, new_pdf_files)
    successfully_loaded_files = {doc.metadata["source"] for doc in new_docs}

    if successfully_loaded_files:
        processed_files = set(processed_files)
        processed_files.update(successfully_loaded_files)
        save_processed_files(processed_files)

    failed_files = set(new_pdf_files) - successfully_loaded_files
    for file_name in sorted(failed_files):
        print(f"PDF was not marked as processed because it could not be loaded: {file_name}")

    return new_docs, processed_files


def load_all_pdfs(folder_path):
    """Load all PDFs so keyword fallback can search the full document set."""
    return load_pdfs_by_name(folder_path, list_pdf_files(folder_path))


def split_documents_with_ids(documents_to_split):
    """Split documents and assign deterministic chunk ids to avoid duplicates."""
    if not documents_to_split:
        return [], []

    split_docs = splitter.split_documents(documents_to_split)
    chunk_counts = {}
    chunk_ids = []

    for doc in split_docs:
        source = doc.metadata.get("source", "unknown")
        page_number = doc.metadata.get("page_number", doc.metadata.get("page", 0))
        chunk_key = f"{source}:{page_number}"
        chunk_index = chunk_counts.get(chunk_key, 0)
        chunk_counts[chunk_key] = chunk_index + 1

        doc.metadata["chunk_index"] = chunk_index
        chunk_ids.append(f"{source}:{page_number}:{chunk_index}")

    return split_docs, chunk_ids


def get_processed_sources_from_db(vector_store):
    """Recover processed sources from Chroma metadata if the tracker is missing or stale."""
    try:
        payload = vector_store.get(include=["metadatas"])
    except Exception as exc:
        print(f"Could not inspect existing vector DB metadata: {exc}")
        return set()

    metadatas = payload.get("metadatas") or []
    return {
        metadata.get("source") for metadata in metadatas
        if metadata and metadata.get("source")
    }


# ==============================
# Chroma DB (Persistent)
# ==============================
try:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    processed_files = load_processed_files()
    existing_db = os.path.isdir(VECTOR_DB_DIR) and any(os.scandir(VECTOR_DB_DIR))

    if existing_db:
        db = Chroma(
            persist_directory=VECTOR_DB_DIR,
            embedding_function=embeddings,
        )

        known_sources = get_processed_sources_from_db(db)
        if known_sources - processed_files:
            processed_files.update(known_sources)
            save_processed_files(processed_files)

        new_documents, processed_files = load_new_pdfs(DATA_FOLDER, processed_files)
        split_docs, chunk_ids = split_documents_with_ids(new_documents)

        if split_docs:
            db.add_documents(split_docs, ids=chunk_ids)
            print(
                f"Added {len(split_docs)} chunks from "
                f"{len(set(doc.metadata['source'] for doc in new_documents))} new PDF(s)."
            )
        else:
            print("No new PDFs detected. Existing vector DB is up to date.")
    else:
        all_documents, processed_files = load_new_pdfs(DATA_FOLDER, processed_files)
        split_docs, chunk_ids = split_documents_with_ids(all_documents)

        if split_docs:
            db = Chroma.from_documents(
                split_docs,
                embeddings,
                ids=chunk_ids,
                persist_directory=VECTOR_DB_DIR,
            )
            print(f"Created vector DB with {len(split_docs)} chunks from {len(processed_files)} PDF(s).")
        else:
            print("Vector DB was not created because there were no readable PDFs to ingest.")

    all_documents = load_all_pdfs(DATA_FOLDER)
    docs, _ = split_documents_with_ids(all_documents)
except Exception as exc:
    print(f"Embedding setup failed, using keyword-only retrieval: {exc}")
    all_documents = load_all_pdfs(DATA_FOLDER)
    docs, _ = split_documents_with_ids(all_documents)

# ==============================
# Chat History
# ==============================
chat_history = []

# ==============================
# Prompts and Routing
# ==============================
RAG_SYSTEM_PROMPT = """
You are Jain AI, a helpful academic assistant for Jain University students.

Rules:
- Use the provided context as your primary source for Jain University answers.
- If the exact answer is in the context, state it in the first sentence.
- Do not say information is missing when the answer appears in the context.
- Do not invent facts, fees, packages, rankings, policies, or dates.
- If the context does not contain the answer, clearly say the source material does not include it.
- Keep the answer concise, clear, and student-friendly.
- If the question is general or conversational, answer naturally without relying on the context.
- Always maintain a helpful and approachable tone.
Format:
- First line: direct answer
- Then: short explanation if needed, using only the context.
"""

GENERAL_SYSTEM_PROMPT = """
You are Jain AI.

Rules:
- Answer general questions clearly and naturally.
- Do not invent specific Jain University facts unless source context is provided.
- If you are unsure about a factual claim, say that you are not certain.
- Keep the response helpful and concise.
"""

FILE_SYSTEM_PROMPT = """
You are Jain AI handling uploaded files.

Rules:
- Use only the extracted text from the uploaded file.
- If the answer is present in the extracted text, give the exact answer in the first sentence.
- If the extracted text does not contain the answer, say that the uploaded file does not include it.
- Do not invent text that was not extracted.
- Keep the answer concise and relevant to the user's question about the file.
"""

GENERAL_CHAT_PATTERNS = {
    "hi", "hii", "hello", "hey", "yo", "hola", "good morning", "good afternoon",
    "good evening", "how are you", "what's up", "whats up", "who are you",
    "tell me a joke", "joke", "motivate me", "thank you", "thanks", "bye",
}

COMMON_QUERY_WORDS = {
    "the", "and", "for", "with", "that", "this", "from", "have", "your", "about",
    "what", "when", "where", "which", "who", "whom", "whose", "why", "how", "can",
    "could", "would", "should", "give", "tell", "say", "show", "find", "need",
    "please", "into", "onto", "does", "did", "been", "being", "name", "details",
    "submitted", "submission", "labactivity", "activity", "lab", "assignment", "pdf",
    "file", "document", "prof", "professor", "sir", "madam", "my", "me", "i",
}

RAG_HINTS = {
    "jain", "university", "campus", "admission", "fees", "course", "courses",
    "syllabus", "placement", "placements", "hostel", "department", "faculty",
    "semester", "exam", "academics", "academic", "notes", "pdf", "document",
    "research", "bengaluru", "bangalore", "kanakapura", "program", "programs",
    "package", "recruiter", "recruiters", "curriculum", "prof", "professor",
    "submitted", "submission", "lab", "assignment", "faculty", "teacher",
}

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
PDF_EXTENSIONS = {".pdf"}


def keyword_search(query, chunks, limit=3):
    """Fallback retrieval for exact facts and minor-typo queries."""
    keywords = set(re.findall(r"\w+", query.lower()))
    keywords = {
        word for word in keywords
        if len(word) > 2 and word not in COMMON_QUERY_WORDS
    }

    if not keywords:
        keywords = {
            word for word in re.findall(r"\w+", query.lower())
            if len(word) > 2
        }

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


def build_context(query, source_docs=None):
    active_docs = source_docs or docs
    retrieved = db.similarity_search(query, k=4) if db and source_docs is None else []
    keyword_hits = keyword_search(query, active_docs, limit=3)

    combined = []
    seen = set()

    for chunk in retrieved + keyword_hits:
        content = chunk.page_content.strip()
        if content and content not in seen:
            seen.add(content)
            combined.append(content)

    return "\n\n".join(combined[:5])


def is_general_chat(query):
    normalized = " ".join(re.findall(r"\w+", query.lower())).strip()

    if not normalized:
        return True

    if normalized in GENERAL_CHAT_PATTERNS:
        return True

    if any(phrase in normalized for phrase in GENERAL_CHAT_PATTERNS):
        return True

    return not any(word in normalized for word in RAG_HINTS)


def is_university_query(query):
    normalized = " ".join(re.findall(r"\w+", query.lower())).strip()
    return any(word in normalized for word in RAG_HINTS)


def call_text_model(system_prompt, user_prompt, temperature=0.1):
    response = client.chat.completions.create(
        model=TEXT_MODEL,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content


def image_bytes_to_data_url(image_bytes, mime_type):
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def run_vision_ocr(image_bytes, mime_type):
    response = client.chat.completions.create(
        model=VISION_MODEL,
        temperature=0.0,
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract all readable text from the image exactly as it appears. "
                    "Return plain text only. If no text is visible, say 'NO_TEXT_FOUND'."
                ),
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract the text from this image."},
                    {
                        "type": "image_url",
                        "image_url": {"url": image_bytes_to_data_url(image_bytes, mime_type)},
                    },
                ],
            },
        ],
    )
    return response.choices[0].message.content.strip()


def pdf_page_to_png_bytes(page):
    pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    return pixmap.tobytes("png")


def extract_text_from_pdf_bytes(pdf_bytes):
    pdf = fitz.open(stream=pdf_bytes, filetype="pdf")
    direct_text = "\n".join(page.get_text("text") for page in pdf).strip()
    if len(re.sub(r"\s+", "", direct_text)) >= 80:
        return direct_text

    ocr_pages = []
    for page in pdf[:3]:
        ocr_text = run_vision_ocr(pdf_page_to_png_bytes(page), "image/png")
        if ocr_text and ocr_text != "NO_TEXT_FOUND":
            ocr_pages.append(ocr_text)

    return "\n\n".join(ocr_pages).strip()


def extract_text_from_image_bytes(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    image_format = (image.format or "PNG").lower()
    mime_type = f"image/{'jpeg' if image_format == 'jpg' else image_format}"
    return run_vision_ocr(image_bytes, mime_type)


def extract_uploaded_text(file_storage):
    if not file_storage or not file_storage.filename:
        return "", ""

    filename = file_storage.filename
    extension = os.path.splitext(filename.lower())[1]
    file_bytes = file_storage.read()

    if extension in PDF_EXTENSIONS:
        return extract_text_from_pdf_bytes(file_bytes), filename

    if extension in IMAGE_EXTENSIONS:
        return extract_text_from_image_bytes(file_bytes), filename

    return "", filename


def direct_fact_answer(query, context):
    normalized = query.lower()
    compact_context = re.sub(r"\s+", " ", context)

    if ("prof" in normalized or "professor" in normalized or "faculty" in normalized) and (
        "name" in normalized or "submitted" in normalized or "submit" in normalized
    ):
        match = re.search(r"submitted to\s*[:\-]?\s*(prof\.?\s*[A-Za-z .]+)", compact_context, re.IGNORECASE)
        if match:
            return f"The professor name is {match.group(1).strip()}."

    if (
        ("my name" in normalized or "who submitted" in normalized or "submitted by" in normalized)
        or ("name" in normalized and "pdf" in normalized)
    ):
        match = re.search(r"submitted by\s*[:\-]?\s*([A-Za-z .]+)", compact_context, re.IGNORECASE)
        if match:
            return f"The submitted name is {match.group(1).strip()}."

    if "highest package" in normalized or ("package" in normalized and "highest" in normalized):
        match = re.search(r"highest package[^.:\n]*?(\d+\s*LPA)", compact_context, re.IGNORECASE)
        if match:
            value = re.sub(r"\s+", " ", match.group(1).upper()).strip()
            return f"The highest package is {value}."

    if "average package" in normalized or ("package" in normalized and "average" in normalized):
        match = re.search(r"average packages?[^.:\n]*?(\d+\s*LPA\s*[–-]\s*\d+\s*LPA)", compact_context, re.IGNORECASE)
        if match:
            return f"The average package range is {match.group(1).replace('–', '-')}."

    return None


def answer_from_context(query, context, system_prompt):
    if not context.strip():
        return "I could not find the answer in the available source material."

    fact_answer = direct_fact_answer(query, context)
    if fact_answer:
        return fact_answer

    prompt = f"""
Context:
{context}

Question:
{query}

Answer using only the context above. If the answer is present, state the exact value in the first sentence.
If the answer is not present, say that the available source material does not contain it.
"""
    return call_text_model(system_prompt, prompt, temperature=0.0)


def route_request(user_input, uploaded_filename):
    if uploaded_filename:
        return "upload"
    if is_university_query(user_input):
        return "rag"
    return "general"


# ==============================
# Main Route
# ==============================
@app.route("/", methods=["GET", "POST"])
def home():
    global chat_history

    if request.method == "POST":
        user_input = (request.form.get("query") or "").strip()
        file = request.files.get("file")

        if not user_input and not (file and file.filename):
            return render_template("index.html", chat_history=chat_history)

        user_message = user_input or f"Analyze uploaded file: {file.filename}"
        chat_history.append(("user", user_message))

        try:
            route = route_request(user_input, file.filename if file else "")

            if route == "upload":
                extracted_text, filename = extract_uploaded_text(file)
                if not extracted_text or extracted_text == "NO_TEXT_FOUND":
                    bot_reply = f"I could not extract readable text from `{filename}`."
                else:
                    question = user_input or "Summarize this file."
                    bot_reply = answer_from_context(question, extracted_text[:12000], FILE_SYSTEM_PROMPT)
            elif route == "rag":
                context = build_context(user_input)
                bot_reply = answer_from_context(user_input, context, RAG_SYSTEM_PROMPT)
            else:
                bot_reply = call_text_model(GENERAL_SYSTEM_PROMPT, user_input, temperature=0.2)
        except Exception as exc:
            print(f"Request handling failed: {exc}")
            bot_reply = (
                "I ran into a temporary problem while processing that request. "
                "Please try again in a moment."
            )

        chat_history.append(("bot", bot_reply))

    return render_template("index.html", chat_history=chat_history)


if __name__ == "__main__":
    app.run(debug=True)