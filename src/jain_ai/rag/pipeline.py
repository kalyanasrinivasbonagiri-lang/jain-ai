import threading

from ..constants.settings import APP_NAME
from ..utils.logging_utils import get_logger
from .indexing import initialize_vector_resources
from .retrieval import build_context as build_context_from_state
from .retrieval import build_context_bundle as build_context_bundle_from_state


logger = get_logger(APP_NAME.lower().replace(" ", "_"))


class RAGPipeline:
    def __init__(self):
        self.initialized = False
        self.embeddings = None
        self.db = None
        self.docs = []
        self.vector_store_ready = False
        self.last_init_error = None
        self._lock = threading.Lock()

    def initialize(self):
        if self.initialized:
            return

        with self._lock:
            if self.initialized:
                return

            logger.info("Initializing RAG resources")
            try:
                (
                    self.embeddings,
                    self.db,
                    self.docs,
                    self.vector_store_ready,
                    self.last_init_error,
                ) = initialize_vector_resources()
            except Exception as exc:
                logger.exception("Embedding setup failed, using keyword-only retrieval: %s", exc)
                self.last_init_error = str(exc)
            finally:
                self.initialized = True

    def build_context(self, query, source_docs=None):
        self.initialize()
        active_db = self.db if source_docs is None and self.vector_store_ready else None
        return build_context_from_state(query, self.docs, db=active_db, source_docs=source_docs)

    def build_context_bundle(self, query, source_docs=None):
        self.initialize()
        active_db = self.db if source_docs is None and self.vector_store_ready else None
        return build_context_bundle_from_state(query, self.docs, db=active_db, source_docs=source_docs)


_rag_pipeline = RAGPipeline()


def get_rag_pipeline():
    return _rag_pipeline
