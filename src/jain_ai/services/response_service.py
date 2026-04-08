import re

from ..llm.groq_client import call_text_model


PREVIOUS_PAPERS_DRIVE_LINK = "https://drive.google.com/drive/folders/1uHiGpzL9Yu5iy1G1bO-Tmh6M6vDVwTvg?usp=sharing"
ADMISSIONS_APPLICATION_LINK = "https://jgigroup.in/btech2026/"
ADMISSIONS_CANCELLATION_LINK = "https://www.jainuniversity.ac.in/admission/cancellation-and-refund-rules"


def previous_papers_answer(query):
    normalized = re.sub(r"\s+", " ", (query or "").lower()).strip()
    asks_for_papers = any(term in normalized for term in (
        "previous year paper",
        "previous year papers",
        "prev year paper",
        "prev year papers",
        "question paper",
        "question papers",
        "old paper",
        "old papers",
        "exam pattern",
        "exam format",
        "pattern of exam",
        "format of exam",
        "jet exam pattern",
        "jet pattern",
    ))

    if not asks_for_papers:
        return None

    return (
        "You can find previous year papers, exam format details, and JET exam pattern here: "
        f"{PREVIOUS_PAPERS_DRIVE_LINK} "
        "Please open the folder and choose the paper or format you need."
    )


def admissions_link_answer(query):
    normalized = re.sub(r"\s+", " ", (query or "").lower()).strip()
    asks_directly_for_link = any(term in normalized for term in (
        "where to apply",
        "application link",
        "admission link",
        "apply link",
    ))

    if not asks_directly_for_link:
        return None

    return (
        "You can apply for Jain University through the official application portal: "
        f"{ADMISSIONS_APPLICATION_LINK}\n\n"
        "For cancellation and refund policy details, use: "
        f"{ADMISSIONS_CANCELLATION_LINK}"
    )


def should_append_admissions_links(query):
    normalized = re.sub(r"\s+", " ", (query or "").lower()).strip()
    return any(term in normalized for term in (
        "how to join",
        "join jain",
        "admission process",
        "how to apply",
        "where to apply",
        "application link",
        "admission link",
        "apply link",
        "apply for jain",
    ))


def advisory_branch_answer(query, context):
    normalized = re.sub(r"\s+", " ", (query or "").lower()).strip()
    asks_for_best = "best" in normalized
    asks_about_academics = any(term in normalized for term in (
        "branch", "course", "program", "aiml", "ai ml", "cse", "ece", "eee", "ise",
    ))

    if not (asks_for_best and asks_about_academics):
        return None

    mentioned_options = []
    for label in ("AIML", "CSE", "ECE", "EEE", "ISE", "Cyber Security", "Data Science", "IoT"):
        if label.lower() in normalized:
            mentioned_options.append(label)

    comparison_text = "the available Jain University documents"
    if mentioned_options:
        comparison_text = f"the available Jain University documents for {', '.join(mentioned_options)}"

    return (
        "There is no single best branch for everyone. The right choice depends on your interests, "
        "career goals, and strengths. "
        f"I can compare {comparison_text} on curriculum, fees, and placement-related details if you want."
    )


def extract_relevant_links(query, context):
    normalized = re.sub(r"\s+", " ", (query or "").lower()).strip()
    asks_for_links = any(term in normalized for term in (
        "link", "website", "site", "apply", "application", "admission process",
        "how to join", "where to apply", "contact",
    ))
    if not asks_for_links:
        return []

    labeled_links = []
    seen = set()
    for raw_line in (context or "").splitlines():
        line = raw_line.strip()
        if "http://" not in line and "https://" not in line:
            continue

        match = re.search(r"(https?://\S+)", line)
        if not match:
            continue

        url = match.group(1).rstrip(").,")
        label = line[:match.start()].strip(" :-")
        if not label:
            label = "Relevant link"

        key = (label.lower(), url.lower())
        if key in seen:
            continue
        seen.add(key)
        labeled_links.append((label, url))

    return labeled_links


def append_relevant_links(answer, query, context):
    links = extract_relevant_links(query, context)
    if should_append_admissions_links(query):
        links = [("Application Link", ADMISSIONS_APPLICATION_LINK), ("Cancellation and Refund Policy", ADMISSIONS_CANCELLATION_LINK)] + links

    if not links:
        return answer

    lines = [answer.rstrip(), "", "Relevant links:"]
    seen = set()
    deduped_links = []
    for label, url in links:
        key = (label.lower(), url.lower())
        if key in seen:
            continue
        seen.add(key)
        deduped_links.append((label, url))

    for label, url in deduped_links[:4]:
        lines.append(f"- {label}: {url}")
    return "\n".join(lines)


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
    papers_answer = previous_papers_answer(query)
    if papers_answer:
        return papers_answer

    admissions_answer = admissions_link_answer(query)
    if admissions_answer:
        return admissions_answer

    if not context.strip():
        return "I could not find the answer in the available source material."

    branch_advice = advisory_branch_answer(query, context)
    if branch_advice:
        return branch_advice

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
    answer = call_text_model(system_prompt, prompt, temperature=0.0)
    return append_relevant_links(answer, query, context)


def answer_with_fallback(query, context, system_prompt, fallback_prompt, chat_context=""):
    papers_answer = previous_papers_answer(query)
    if papers_answer:
        return papers_answer

    admissions_answer = admissions_link_answer(query)
    if admissions_answer:
        return admissions_answer

    if not context_has_substance(context):
        return call_text_model(fallback_prompt, query, temperature=0.2)

    return answer_from_context(query, context, system_prompt, chat_context=chat_context)
