from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from ..config import VECTOR_DB_DIR
from ..constants.settings import EMBEDDING_MODEL
from ..utils.logging_utils import get_logger


logger = get_logger("jain_ai.rag.vector_store")


def create_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"local_files_only": True},
    )


def load_vector_store(embeddings):
    return Chroma(
        persist_directory=VECTOR_DB_DIR,
        embedding_function=embeddings,
    )


def create_vector_store(split_docs, embeddings, chunk_ids):
    return Chroma.from_documents(
        split_docs,
        embeddings,
        ids=chunk_ids,
        persist_directory=VECTOR_DB_DIR,
    )


def get_processed_sources_from_db(vector_store):
    try:
        payload = vector_store.get(include=["metadatas"])
    except Exception as exc:
        logger.warning("Could not inspect existing vector DB metadata: %s", exc)
        return set()

    metadatas = payload.get("metadatas") or []
    return {
        metadata.get("source") for metadata in metadatas
        if metadata and metadata.get("source")
    }
