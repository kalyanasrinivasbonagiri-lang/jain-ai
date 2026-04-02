from dataclasses import dataclass


@dataclass
class RetrievalStatus:
    vector_store_ready: bool
    documents_loaded: int
