import re

from ..llm.groq_client import call_text_model


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

    if "highest package" in normalized or ("package" in normalized and "highest" in normalized):
        match = re.search(r"highest package[^.:\n]*?(\d+\s*LPA)", compact_context, re.IGNORECASE)
        if match:
            value = re.sub(r"\s+", " ", match.group(1).upper()).strip()
            return f"The highest package is {value}."

    if "average package" in normalized or ("package" in normalized and "average" in normalized):
        match = re.search(r"average packages?[^.:\n]*?(\d+\s*LPA\s*[–-]\s*\d+\s*LPA)", compact_context, re.IGNORECASE)
        if match:
            return f"The average package range is {match.group(1).replace('–', '-')}."

    return None


def answer_from_context(query, context, system_prompt, chat_context=""):
    if not context.strip():
        return "I could not find the answer in the available source material."

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
