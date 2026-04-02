import re
from difflib import SequenceMatcher

from ..constants.routing import COMMON_QUERY_WORDS
from ..constants.settings import KEYWORD_LIMIT, SIMILARITY_K
from ..utils.logging_utils import get_logger


logger = get_logger("jain_ai.rag.retrieval")


def similar(left, right):
    if abs(len(left) - len(right)) > 2:
        return False
    return SequenceMatcher(None, left, right).ratio() >= 0.78


def keyword_search(query, chunks, limit=KEYWORD_LIMIT):
    keywords = set(re.findall(r"\w+", query.lower()))
    keywords = {
        word for word in keywords
        if len(word) > 2 and word not in COMMON_QUERY_WORDS
    }

    if not keywords:
        keywords = {word for word in re.findall(r"\w+", query.lower()) if len(word) > 2}

    scored_chunks = []
    for chunk in chunks:
        content = chunk.page_content.lower()
        content_words = set(re.findall(r"\w+", content))
        score = 0

        for word in keywords:
            if word in content:
                score += 3
            elif any(similar(word, candidate) for candidate in content_words):
                score += 1

        if score:
            scored_chunks.append((score, chunk))

    scored_chunks.sort(key=lambda item: item[0], reverse=True)
    return [chunk for _, chunk in scored_chunks[:limit]]


def build_context(query, docs, db=None, source_docs=None):
    active_docs = source_docs or docs
    retrieved = []

    if db is not None and source_docs is None:
        try:
            retrieved = db.similarity_search(query, k=SIMILARITY_K)
        except Exception as exc:
            logger.warning("Vector similarity search failed, falling back to keyword search: %s", exc)

    keyword_hits = keyword_search(query, active_docs, limit=KEYWORD_LIMIT)
    combined = []
    seen = set()

    for chunk in retrieved + keyword_hits:
        content = chunk.page_content.strip()
        if content and content not in seen:
            seen.add(content)
            combined.append(content)

    return "\n\n".join(combined[:5])
