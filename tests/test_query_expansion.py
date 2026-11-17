import os
import sys
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from jain_ai.utils.query_expansion import expand_aliases, PROGRAM_ALIASES


def test_expand_aliases_eee():
    result = expand_aliases("fee for EEE?")
    assert "EEE (Electrical and Electronics Engineering)" in result


def test_expand_aliases_ece_and_ise():
    result = expand_aliases("What is the fee for ECE and ISE?")
    assert "ECE (Electronics and Communication Engineering)" in result
    assert "ISE (Information Science and Engineering)" in result


def test_expand_aliases_avoids_false_positives_for_se():
    # 'se' should only match standalone word, not inside words
    query = "please release these notes"
    result = expand_aliases(query)
    assert result == query
    assert "Software Engineering" not in result


def test_expand_aliases_standalone_se():
    query = "syllabus for SE branch"
    result = expand_aliases(query)
    assert "SE (Software Engineering)" in result


def test_expand_aliases_does_not_duplicate_if_already_present():
    query = "fee for EEE Electrical and Electronics Engineering"
    result = expand_aliases(query)
    assert result == query


def test_expand_aliases_all_required_acronyms():
    required = [
        "EEE", "ECE", "ISE", "CSBS", "CTMA", "CTIS", "AIML",
        "AIDE", "CPS", "IoT", "SE", "DS", "CSE", "Mech", "Civil", "Aero"
    ]
    for acr in required:
        assert acr in PROGRAM_ALIASES
        expanded = expand_aliases(f"tell me about {acr}")
        assert f"{acr} ({PROGRAM_ALIASES[acr]})" in expanded
