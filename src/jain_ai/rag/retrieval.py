import re
from difflib import SequenceMatcher

from ..constants.routing import COMMON_QUERY_WORDS
from ..constants.settings import KEYWORD_LIMIT, SIMILARITY_K
from ..utils.logging_utils import get_logger


logger = get_logger("jain_ai.rag.retrieval")


BRANCH_ALIASES = {
    "cse": {"cse", "computer science"},
    "ctis": {"ctis"},
    "ai": {"ai", "artificial intelligence"},
    "iot": {"iot", "internet of things"},
}


def similar(left, right):
    if abs(len(left) - len(right)) > 2:
        return False
    return SequenceMatcher(None, left, right).ratio() >= 0.78


def extract_query_branch(query):
    normalized = query.lower()

    for branch_key, aliases in BRANCH_ALIASES.items():
        for alias in aliases:
            pattern = rf"\b{re.escape(alias)}\b"
            if re.search(pattern, normalized):
                return branch_key

    return None


def extract_branch_line(content):
    match = re.search(r"branch\s*/\s*school\s*:\s*(.+)", content, re.IGNORECASE)
    if not match:
        return ""
    return match.group(1).strip().lower()


def branch_match_score(query, chunk):
    branch_key = extract_query_branch(query)
    if not branch_key:
        return 0

    branch_line = extract_branch_line(chunk.page_content)
    if not branch_line:
        return 0

    if branch_key == "cse":
        if "cse and cse star" in branch_line or re.fullmatch(r"cse", branch_line):
            return 120
        if re.search(r"\bcse\b", branch_line):
            return 60
        return 0

    aliases = BRANCH_ALIASES.get(branch_key, {branch_key})
    for alias in aliases:
        if re.search(rf"\b{re.escape(alias)}\b", branch_line):
            return 100

    return 0


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
        score = branch_match_score(query, chunk)

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
    ranked_chunks = []

    for index, chunk in enumerate(retrieved):
        ranked_chunks.append((100 - index + branch_match_score(query, chunk), chunk))

    for index, chunk in enumerate(keyword_hits):
        ranked_chunks.append((60 - index + branch_match_score(query, chunk), chunk))

    ranked_chunks.sort(key=lambda item: item[0], reverse=True)

    for _, chunk in ranked_chunks:
        content = chunk.page_content.strip()
        if content and content not in seen:
            seen.add(content)
            combined.append(content)

    return "\n\n".join(combined[:6])
