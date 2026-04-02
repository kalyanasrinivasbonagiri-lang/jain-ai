import re
from difflib import SequenceMatcher


def normalize_query(text):
    return " ".join(re.findall(r"\w+", text.lower())).strip()


def similar(left, right):
    if abs(len(left) - len(right)) > 2:
        return False
    return SequenceMatcher(None, left, right).ratio() >= 0.78
