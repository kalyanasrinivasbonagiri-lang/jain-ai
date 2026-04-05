import re
from difflib import SequenceMatcher

from ..constants.prompts import ROUTER_SYSTEM_PROMPT
from ..constants.routing import BROAD_HELP_PATTERNS, FOLLOW_UP_REFERENCES, GENERAL_CHAT_PATTERNS, RAG_HINTS
from ..llm.groq_client import call_text_model


VALID_ROUTES = {"general", "rag", "upload", "summarize", "follow_up"}


def normalize_query(query):
    return " ".join(re.findall(r"\w+", (query or "").lower())).strip()


def contains_phrase(normalized, phrase):
    escaped = re.escape(phrase)
    pattern = rf"(?<!\w){escaped}(?!\w)"
    return re.search(pattern, normalized) is not None


def similar_token(left, right, threshold=0.84):
    if abs(len(left) - len(right)) > 2:
        return False
    return SequenceMatcher(None, left, right).ratio() >= threshold


def contains_rag_hint(normalized):
    if any(word in normalized for word in RAG_HINTS):
        return True

    tokens = normalized.split()
    for token in tokens:
        if len(token) < 4:
            continue
        if any(similar_token(token, hint) for hint in RAG_HINTS if len(hint) >= 4):
            return True

    return False


def is_general_chat(query):
    normalized = normalize_query(query)

    if not normalized:
        return True

    if normalized in GENERAL_CHAT_PATTERNS:
        return True

    if any(contains_phrase(normalized, phrase) for phrase in GENERAL_CHAT_PATTERNS):
        return True

    if any(contains_phrase(normalized, phrase) for phrase in BROAD_HELP_PATTERNS):
        return True

    return not contains_rag_hint(normalized)


def is_university_query(query):
    normalized = normalize_query(query)
    return contains_rag_hint(normalized)


def is_follow_up_query(query):
    normalized = normalize_query(query)
    words = normalized.split()

    if not words:
        return False

    if normalized.startswith("what about "):
        return True

    if len(words) <= 4 and any(reference in normalized for reference in FOLLOW_UP_REFERENCES):
        return True

    if len(words) <= 2 and not contains_rag_hint(normalized):
        return True

    return False


def is_summarize_query(query):
    normalized = normalize_query(query)
    summarize_terms = ("summarize", "summary", "summery", "brief", "overview")
    return any(term in normalized for term in summarize_terms)


def heuristic_route_request(user_input, uploaded_filename):
    if uploaded_filename:
        return "upload"
    if is_summarize_query(user_input):
        return "summarize"
    if is_follow_up_query(user_input):
        return "follow_up"
    if is_general_chat(user_input):
        return "general"
    if is_university_query(user_input):
        return "rag"
    return "general"


def build_router_message(user_input, uploaded_filename):
    normalized = (user_input or "").strip()
    if uploaded_filename:
        return (
            f"Uploaded filename: {uploaded_filename}\n"
            f"User message: {normalized or '[no text message]'}"
        )
    return normalized or "[empty message]"


def parse_route_label(raw_label):
    cleaned = normalize_query(raw_label).replace(" ", "_")
    if cleaned in VALID_ROUTES:
        return cleaned

    for label in VALID_ROUTES:
        if label in normalize_query(raw_label).split():
            return label

    return None


def route_request(user_input, uploaded_filename):
    heuristic_label = heuristic_route_request(user_input, uploaded_filename)

    try:
        model_label = parse_route_label(
            call_text_model(
                ROUTER_SYSTEM_PROMPT,
                build_router_message(user_input, uploaded_filename),
                temperature=0.0,
            )
        )
        if model_label in VALID_ROUTES:
            return model_label
    except Exception:
        pass

    return heuristic_label
