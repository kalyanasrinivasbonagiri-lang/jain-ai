from .rag.pipeline import get_rag_pipeline


def initialize_extensions():
    return {"rag_pipeline": get_rag_pipeline()}
