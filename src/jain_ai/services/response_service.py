import re

from ..llm.groq_client import call_text_model


def context_has_substance(context, min_chars=120, min_words=20):
    normalized = re.sub(r"\s+", " ", context or "").strip()
    if not normalized:
        return False
    if len(normalized) >= min_chars and len(normalized.split()) >= min_words:
        return True
    if re.search(r"\d", normalized) and len(normalized.split()) >= 8:
        return True
    return len(normalized.split()) >= 12


def format_club_list_answer(query, context):
    normalized = query.lower()
    asks_for_clubs = "club" in normalized or "clubs" in normalized
    asks_broadly = any(phrase in normalized for phrase in (
        "is there any club",
        "is there any clubs",
        "what clubs",
        "which clubs",
        "list all clubs",
        "clubs in jain",
    ))

    if not (asks_for_clubs and asks_broadly):
        return None

    matches = re.findall(
        r"^\s*\d+\.\s*(.+?)\s*-\s*Branch\s*/\s*School:\s*(.+?)\s*$",
        context,
        flags=re.IGNORECASE | re.MULTILINE,
    )

    if not matches:
        return None

    lines = ["Yes, Jain University has several student clubs. Here are the clubs with their branch or school:"]
    for club_name, branch in matches:
        lines.append(f"- {club_name.strip()} - {branch.strip()}")
    return "\n".join(lines)


def direct_fact_answer(query, context):
    normalized = query.lower()
    compact_context = re.sub(r"\s+", " ", context)

    if ("prof" in normalized or "professor" in normalized or "faculty" in normalized) and (
        "name" in normalized or "submitted" in normalized or "submit" in normalized
    ):
        match = re.search(r"submitted to\s*[:\-]?\s*(prof\.?\s*[A-Za-z .]+)", compact_context, re.IGNORECASE)
        if match:
            return f"The professor name is {match.group(1).strip()}."

    if (
        ("my name" in normalized or "who submitted" in normalized or "submitted by" in normalized)
        or ("name" in normalized and "pdf" in normalized)
    ):
        match = re.search(r"submitted by\s*[:\-]?\s*([A-Za-z .]+)", compact_context, re.IGNORECASE)
        if match:
            return f"The submitted name is {match.group(1).strip()}."

    if (
        "highest ctc overall record" in normalized
        or ("highest ctc" in normalized and "overall" in normalized)
        or ("ctc" in normalized and "overall record" in normalized)
    ):
        match = re.search(r"highest ctc\s*\(overall record\)\s*[:\-]?\s*(\d+(?:\.\d+)?\s*LPA)", compact_context, re.IGNORECASE)
        if match:
            value = re.sub(r"\s+", " ", match.group(1).upper()).strip()
            return f"The highest CTC overall record is {value}."

    if "highest ctc dashboard" in normalized or ("highest ctc" in normalized and "dashboard" in normalized):
        match = re.search(r"highest ctc\s*\(dashboard\)\s*[:\-]?\s*(\d+(?:\.\d+)?\s*LPA)", compact_context, re.IGNORECASE)
        if match:
            value = re.sub(r"\s+", " ", match.group(1).upper()).strip()
            return f"The highest CTC on the dashboard is {value}."

    if (
        "highest package" in normalized
        or ("package" in normalized and "highest" in normalized)
        or "highest ctc" in normalized
    ):
        match = re.search(r"highest (?:package|ctc)[^.:\n]*?(\d+(?:\.\d+)?\s*LPA)", compact_context, re.IGNORECASE)
        if match:
            value = re.sub(r"\s+", " ", match.group(1).upper()).strip()
            return f"The highest package is {value}."

    if "average ctc dashboard" in normalized or ("average ctc" in normalized and "dashboard" in normalized):
        match = re.search(r"average ctc\s*\(dashboard\)\s*[:\-]?\s*(\d+(?:\.\d+)?\s*LPA)", compact_context, re.IGNORECASE)
        if match:
            value = re.sub(r"\s+", " ", match.group(1).upper()).strip()
            return f"The average CTC on the dashboard is {value}."

    if "average package" in normalized or ("package" in normalized and "average" in normalized) or "average ctc" in normalized:
        match = re.search(r"average (?:packages?|ctc)[^.:\n]*?(\d+(?:\.\d+)?\s*LPA\s*[--]\s*\d+(?:\.\d+)?\s*LPA)", compact_context, re.IGNORECASE)
        if match:
            return f"The average package range is {match.group(1)}."

    if "lowest ctc" in normalized or ("lowest" in normalized and "ctc" in normalized):
        match = re.search(r"lowest ctc\s*[:\-]?\s*(\d+(?:\.\d+)?\s*LPA)", compact_context, re.IGNORECASE)
        if match:
            value = re.sub(r"\s+", " ", match.group(1).upper()).strip()
            return f"The lowest CTC is {value}."

    if "placement percentage" in normalized or ("placement" in normalized and "percentage" in normalized):
        match = re.search(r"placement percentage\s*[:\-]?\s*(\d+(?:\.\d+)?\s*%)", compact_context, re.IGNORECASE)
        if match:
            return f"The placement percentage is {match.group(1)}."

    return None


def answer_from_context(query, context, system_prompt, chat_context=""):
    if not context.strip():
        return "I could not find the answer in the available source material."

    club_list_answer = format_club_list_answer(query, context)
    if club_list_answer:
        return club_list_answer

    fact_answer = direct_fact_answer(query, context)
    if fact_answer:
        return fact_answer

    conversation_block = ""
    if chat_context.strip():
        conversation_block = f"""
Recent conversation:
{chat_context}

Use the recent conversation only to resolve follow-up references such as "it", "they", or "that club".
Do not let it override the source context.

"""

    prompt = f"""
{conversation_block}Context:
{context}

Question:
{query}

Answer using only the context above. If the answer is present, state the exact value in the first sentence.
If the answer is not present, say that the available source material does not contain it.
"""
    return call_text_model(system_prompt, prompt, temperature=0.0)


def answer_with_fallback(query, context, system_prompt, fallback_prompt, chat_context=""):
    if not context_has_substance(context):
        return call_text_model(fallback_prompt, query, temperature=0.2)

    return answer_from_context(query, context, system_prompt, chat_context=chat_context)
