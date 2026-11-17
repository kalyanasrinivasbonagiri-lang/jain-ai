import re

# Comprehensive mapping of academic acronyms and abbreviations to full names
PROGRAM_ALIASES = {
    "EEE": "Electrical and Electronics Engineering",
    "ECE": "Electronics and Communication Engineering",
    "ISE": "Information Science and Engineering",
    "CSBS": "Computer Science and Business Systems",
    "CTMA": "Mobile Applications and Cloud Technology",
    "CTIS": "Cloud Technology and Information Security",
    "AIML": "Artificial Intelligence and Machine Learning",
    "AIDE": "Artificial Intelligence and Data Engineering",
    "CPS": "Cyber Physical Systems",
    "IoT": "Internet of Things",
    "SE": "Software Engineering",
    "DS": "Data Science",
    "CSE": "Computer Science and Engineering",
    "Mech": "Mechanical Engineering",
    "Civil": "Civil Engineering",
    "Aero": "Aerospace Engineering",
}


def expand_aliases(query: str) -> str:
    """
    Expands program abbreviations and branch acronyms in the user query
    by appending the full canonical form next to the abbreviation.
    Example: "fee for EEE?" -> "fee for EEE (Electrical and Electronics Engineering)?"
    """
    if not query or not query.strip():
        return query

    expanded_query = query

    # Sort keys by length descending to match longer abbreviations first
    for alias, full_name in sorted(PROGRAM_ALIASES.items(), key=lambda item: len(item[0]), reverse=True):
        # Case-insensitive word boundary match
        pattern = rf"\b{re.escape(alias)}\b"
        if re.search(pattern, expanded_query, flags=re.IGNORECASE):
            # Avoid expanding if full name is already in the query
            if full_name.lower() in expanded_query.lower():
                continue

            # Replace abbreviation with "<alias> (<full_name>)"
            def _replacer(match):
                matched_text = match.group(0)
                return f"{matched_text} ({full_name})"

            expanded_query = re.sub(pattern, _replacer, expanded_query, count=1, flags=re.IGNORECASE)

    return expanded_query
