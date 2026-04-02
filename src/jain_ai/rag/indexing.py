import os

from ..config import RAW_DATA_DIR, VECTOR_DB_DIR
from ..utils.logging_utils import get_logger
from .chunking import split_documents_with_ids
from .loaders import load_all_pdfs, load_new_pdfs, load_processed_files, save_processed_files
from .vector_store import create_embeddings, create_vector_store, get_processed_sources_from_db, load_vector_store


logger = get_logger("jain_ai.rag.indexing")


def initialize_vector_resources(openai_api_key):
    all_documents = load_all_pdfs(RAW_DATA_DIR)
    docs, _ = split_documents_with_ids(all_documents)

    if not openai_api_key:
        logger.warning("OPENAI_API_KEY not found. Running in keyword-only retrieval mode.")
        return None, None, docs, False, None

    embeddings = create_embeddings(openai_api_key)
    processed_files = load_processed_files()
    existing_db = os.path.isdir(VECTOR_DB_DIR) and any(os.scandir(VECTOR_DB_DIR))

    if existing_db:
        db = load_vector_store(embeddings)
        known_sources = get_processed_sources_from_db(db)
        if known_sources - processed_files:
            processed_files.update(known_sources)
            save_processed_files(processed_files)

        new_documents, _ = load_new_pdfs(RAW_DATA_DIR, processed_files)
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
        new_documents, processed_files = load_new_pdfs(RAW_DATA_DIR, processed_files)
        split_docs, chunk_ids = split_documents_with_ids(new_documents)
        if split_docs:
            db = create_vector_store(split_docs, embeddings, chunk_ids)
            logger.info(
                "Created vector DB with %s chunks from %s PDF(s)",
                len(split_docs),
                len(processed_files),
            )
        else:
            db = load_vector_store(embeddings)
            logger.info("Vector DB initialized without new documents")

    return embeddings, db, docs, True, None
