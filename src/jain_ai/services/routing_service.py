import re

from ..constants.routing import GENERAL_CHAT_PATTERNS, RAG_HINTS


def is_general_chat(query):
    normalized = " ".join(re.findall(r"\w+", query.lower())).strip()

    if not normalized:
        return True

    if normalized in GENERAL_CHAT_PATTERNS:
        return True

    if any(phrase in normalized for phrase in GENERAL_CHAT_PATTERNS):
        return True

    return not any(word in normalized for word in RAG_HINTS)


def is_university_query(query):
    normalized = " ".join(re.findall(r"\w+", query.lower())).strip()
    return any(word in normalized for word in RAG_HINTS)


def route_request(user_input, uploaded_filename):
    if uploaded_filename:
        return "upload"
    if is_university_query(user_input):
        return "rag"
    return "general"
