from langchain_chroma import Chroma

from ..config import VECTOR_DB_DIR
from ..constants.settings import EMBEDDING_MODEL
from ..utils.logging_utils import get_logger


logger = get_logger("jain_ai.rag.vector_store")


def _resolve_embeddings_class():
    try:
        from langchain_huggingface import HuggingFaceEmbeddings

        return HuggingFaceEmbeddings
    except ImportError:
        try:
            from langchain_community.embeddings import HuggingFaceEmbeddings

            logger.warning(
                "Using deprecated langchain_community HuggingFaceEmbeddings fallback. "
                "Install langchain-huggingface to match the preferred setup."
            )
            return HuggingFaceEmbeddings
        except ImportError as exc:
            raise RuntimeError(
                "HuggingFace embeddings are unavailable. Install `langchain-huggingface` "
                "or provide the legacy `langchain-community` embedding package."
            ) from exc


def create_embeddings():
    embeddings_class = _resolve_embeddings_class()
    return embeddings_class(
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
