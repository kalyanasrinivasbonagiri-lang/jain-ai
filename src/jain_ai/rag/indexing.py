import os
import shutil

from ..config import EMBEDDING_MODEL_PATH, PROCESSED_FILES_PATH, RAW_DATA_DIR, VECTOR_DB_DIR
from ..constants.settings import EMBEDDING_MODEL
from ..utils.logging_utils import get_logger
from .chunking import split_documents_with_ids
from .loaders import load_all_documents, load_new_documents, load_processed_files, save_processed_files
from .vector_store import create_embeddings, create_vector_store, get_processed_sources_from_db, load_vector_store


logger = get_logger("jain_ai.rag.indexing")


def load_indexed_embedding_model():
    if not os.path.exists(EMBEDDING_MODEL_PATH):
        return None

    try:
        with open(EMBEDDING_MODEL_PATH, "r", encoding="utf-8") as file_obj:
            return file_obj.read().strip() or None
    except OSError as exc:
        logger.warning("Could not read embedding model marker '%s': %s", EMBEDDING_MODEL_PATH, exc)
        return None


def save_indexed_embedding_model():
    try:
        with open(EMBEDDING_MODEL_PATH, "w", encoding="utf-8") as file_obj:
            file_obj.write(EMBEDDING_MODEL)
    except OSError as exc:
        logger.warning("Could not write embedding model marker '%s': %s", EMBEDDING_MODEL_PATH, exc)


def reset_vector_store():
    if os.path.isdir(VECTOR_DB_DIR):
        shutil.rmtree(VECTOR_DB_DIR)
    os.makedirs(VECTOR_DB_DIR, exist_ok=True)

    try:
        if os.path.exists(PROCESSED_FILES_PATH):
            os.remove(PROCESSED_FILES_PATH)
    except OSError as exc:
        logger.warning("Could not reset processed files tracker '%s': %s", PROCESSED_FILES_PATH, exc)


def initialize_vector_resources():
    all_documents = load_all_documents(RAW_DATA_DIR)
    docs, _ = split_documents_with_ids(all_documents)

    embeddings = create_embeddings()
    existing_db = os.path.isdir(VECTOR_DB_DIR) and any(os.scandir(VECTOR_DB_DIR))
    indexed_embedding_model = load_indexed_embedding_model()
    if existing_db and not indexed_embedding_model:
        logger.info("Existing vector DB has no embedding model marker. Rebuilding vector DB.")
        reset_vector_store()
        existing_db = False
    elif indexed_embedding_model and indexed_embedding_model != EMBEDDING_MODEL:
        logger.info(
            "Embedding model changed from '%s' to '%s'. Rebuilding vector DB.",
            indexed_embedding_model,
            EMBEDDING_MODEL,
        )
        reset_vector_store()
        existing_db = False

    processed_files = load_processed_files()

    if existing_db:
        db = load_vector_store(embeddings)
        known_sources = get_processed_sources_from_db(db)
        if known_sources - processed_files:
            processed_files.update(known_sources)
            save_processed_files(processed_files)

        new_documents, _ = load_new_documents(RAW_DATA_DIR, processed_files)
        split_docs, chunk_ids = split_documents_with_ids(new_documents)
        if split_docs:
            db.add_documents(split_docs, ids=chunk_ids)
            logger.info(
                "Added %s chunks from %s new PDF(s)",
                len(split_docs),
                len(set(doc.metadata["source"] for doc in new_documents)),
            )
        else:
            logger.info("Existing vector DB is up to date")
    else:
        new_documents, processed_files = load_new_documents(RAW_DATA_DIR, processed_files)
        split_docs, chunk_ids = split_documents_with_ids(new_documents)
        if split_docs:
            db = create_vector_store(split_docs, embeddings, chunk_ids)
            save_indexed_embedding_model()
            logger.info(
                "Created vector DB with %s chunks from %s PDF(s)",
                len(split_docs),
                len(processed_files),
            )
        else:
            db = load_vector_store(embeddings)
            save_indexed_embedding_model()
            logger.info("Vector DB initialized without new documents")

    if existing_db:
        save_indexed_embedding_model()

    return embeddings, db, docs, True, None
