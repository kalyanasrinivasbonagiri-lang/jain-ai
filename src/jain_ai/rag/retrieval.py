import re
from difflib import SequenceMatcher
from pathlib import PurePosixPath, PureWindowsPath

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

FEE_TERMS = {"fee", "fees", "tuition", "per annum", "inr", "registration"}
PLACEMENT_TERMS = {"package", "ctc", "lpa", "placement", "placements", "salary", "recruiter"}
CREDIT_TERMS = {"credit", "credits", "semester", "program totals", "total program credits", "subjects"}
SPECIALIZATION_STOPWORDS = {
    "jain", "university", "how", "many", "what", "which", "does", "will", "get",
    "gets", "student", "students", "total", "credit", "credits", "program", "btech",
    "b", "tech", "bachelor", "technology", "computer", "science", "engineering",
    "cse", "department", "specialization", "course", "curriculum", "semester",
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


def detect_program_focus(query):
    normalized = re.sub(r"\s+", " ", query.lower()).strip()

    if any(term in normalized for term in ("aiml", "ai ml", "artificial intelligence and machine learning")):
        return "aiml"

    if re.search(r"\bcse\s*ai\b", normalized):
        return "ai"

    if (
        "artificial intelligence" in normalized
        and "machine learning" not in normalized
        and "aiml" not in normalized
    ):
        return "ai"

    return None


def tokenize_meaningful(text, stopwords=None):
    stopwords = stopwords or set()
    return {
        token for token in re.findall(r"[a-z0-9]+", (text or "").lower())
        if len(token) > 1 and token not in stopwords
    }


def extract_branch_line(content):
    match = re.search(r"branch\s*/\s*school\s*:\s*(.+)", content, re.IGNORECASE)
    if not match:
        return ""
    return match.group(1).strip().lower()


def extract_specialization_line(content):
    match = re.search(r"specialization\s*:\s*(.+)", content, re.IGNORECASE)
    if not match:
        return ""
    return match.group(1).strip().lower()


def is_academic_program_chunk(chunk):
    metadata = getattr(chunk, "metadata", {}) or {}
    source = (metadata.get("source") or "").lower().replace("\\", "/")
    content = chunk.page_content.lower()
    return source.startswith("academics/") and (
        "specialization:" in content or "program totals" in content or "_btech_" in source
    )


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


def specialization_overlap_score(query, chunk):
    if not is_academic_program_chunk(chunk):
        return 0

    query_tokens = tokenize_meaningful(query, SPECIALIZATION_STOPWORDS | COMMON_QUERY_WORDS)
    if not query_tokens:
        return 0

    metadata = getattr(chunk, "metadata", {}) or {}
    source = (metadata.get("source") or "").lower().replace("\\", "/")
    source_text = re.sub(r"[_\-/\.]+", " ", source)
    specialization_text = extract_specialization_line(chunk.page_content)
    candidate_tokens = tokenize_meaningful(
        f"{source_text} {specialization_text}",
        {"academics", "data", "raw", "2024", "2028", "2026", "2025", "btech"},
    )

    overlap = query_tokens & candidate_tokens
    if not overlap:
        return 0

    score = len(overlap) * 120
    if len(overlap) >= 2:
        score += 80
    return score


def program_focus_score(query, chunk):
    focus = detect_program_focus(query)
    if not focus:
        return 0

    content = chunk.page_content.lower()
    metadata = getattr(chunk, "metadata", {}) or {}
    source = (metadata.get("source") or "").lower().replace("\\", "/")
    score = 0

    if focus == "aiml":
        if any(term in content for term in ("artificial intelligence and machine learning", "aiml")):
            score += 220
        if any(term in source for term in ("aiml",)):
            score += 120
        if (
            "artificial intelligence" in content
            and "machine learning" not in content
            and "aiml" not in content
        ):
            score -= 140

    if focus == "ai":
        if (
            "artificial intelligence" in content
            and "machine learning" not in content
            and "aiml" not in content
        ):
            score += 220
        if re.search(r"(^|[_\-/])ai([_\-/]|$)", source):
            score += 120
        if any(term in content for term in ("artificial intelligence and machine learning", "aiml")):
            score -= 180
        if "branch / school" in content:
            score -= 100

    return score


def intent_match_score(query, chunk):
    normalized_query = query.lower()
    content = chunk.page_content.lower()
    score = 0

    asks_about_fees = any(term in normalized_query for term in FEE_TERMS)
    asks_about_placements = any(term in normalized_query for term in PLACEMENT_TERMS)
    asks_about_credits = any(term in normalized_query for term in CREDIT_TERMS)

    if asks_about_fees:
        if any(term in content for term in FEE_TERMS):
            score += 140
        if "branch / school" in content and not any(term in content for term in FEE_TERMS):
            score -= 80

    if asks_about_placements:
        if any(term in content for term in PLACEMENT_TERMS):
            score += 140
        if "branch / school" in content and not any(term in content for term in PLACEMENT_TERMS):
            score -= 80

    if asks_about_credits:
        if any(term in content for term in CREDIT_TERMS):
            score += 140
        if "branch / school" in content and not any(term in content for term in CREDIT_TERMS):
            score -= 80

    return score


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
        score = (
            branch_match_score(query, chunk)
            + intent_match_score(query, chunk)
            + program_focus_score(query, chunk)
            + specialization_overlap_score(query, chunk)
        )

        for word in keywords:
            if word in content:
                score += 3
            elif any(similar(word, candidate) for candidate in content_words):
                score += 1

        if score:
            scored_chunks.append((score, chunk))

    scored_chunks.sort(key=lambda item: item[0], reverse=True)
    return [chunk for _, chunk in scored_chunks[:limit]]


def split_source_path(source):
    if not source:
        return "unknown", "unknown"

    normalized = source.replace("\\", "/")
    path = PurePosixPath(normalized)
    folder = str(path.parent) if str(path.parent) not in ("", ".") else "root"
    return folder, path.name


def build_source_references(chunks):
    references = []
    seen = set()

    for chunk in chunks:
        metadata = getattr(chunk, "metadata", {}) or {}
        source = metadata.get("source") or metadata.get("file_path") or ""
        if not source:
            continue

        if ":" in source and "\\" in source:
            source = PureWindowsPath(source).name

        folder, file_name = split_source_path(source)
        key = (folder.lower(), file_name.lower())
        if key in seen:
            continue
        seen.add(key)
        references.append({"folder": folder, "file": file_name})

    return references


def build_context_bundle(query, docs, db=None, source_docs=None):
    active_docs = source_docs or docs
    retrieved = []
    normalized_query = query.lower()

    if db is not None and source_docs is None:
        try:
            retrieved = db.similarity_search(query, k=SIMILARITY_K)
        except Exception as exc:
            logger.warning("Vector similarity search failed, falling back to keyword search: %s", exc)

    keyword_hits = keyword_search(query, active_docs, limit=KEYWORD_LIMIT)
    combined = []
    selected_chunks = []
    seen = set()
    ranked_chunks = []

    for index, chunk in enumerate(retrieved):
        ranked_chunks.append((
            100 - index
            + branch_match_score(query, chunk)
            + intent_match_score(query, chunk)
            + program_focus_score(query, chunk)
            + specialization_overlap_score(query, chunk),
            chunk,
        ))

    for index, chunk in enumerate(keyword_hits):
        ranked_chunks.append((
            60 - index
            + branch_match_score(query, chunk)
            + intent_match_score(query, chunk)
            + program_focus_score(query, chunk)
            + specialization_overlap_score(query, chunk),
            chunk,
        ))

    ranked_chunks.sort(key=lambda item: item[0], reverse=True)
    has_specialization_matches = any(
        specialization_overlap_score(query, chunk) > 0 for _, chunk in ranked_chunks
    )
    asks_about_credits = any(term in normalized_query for term in CREDIT_TERMS)

    for _, chunk in ranked_chunks:
        if has_specialization_matches and asks_about_credits and not is_academic_program_chunk(chunk):
            continue
        if has_specialization_matches and is_academic_program_chunk(chunk):
            if specialization_overlap_score(query, chunk) <= 0:
                continue
        content = chunk.page_content.strip()
        if content and content not in seen:
            seen.add(content)
            combined.append(content)
            selected_chunks.append(chunk)

    limited_chunks = selected_chunks[:6]
    return {
        "context": "\n\n".join(combined[:6]),
        "sources": build_source_references(limited_chunks),
    }


def build_context(query, docs, db=None, source_docs=None):
    return build_context_bundle(query, docs, db=db, source_docs=source_docs)["context"]
