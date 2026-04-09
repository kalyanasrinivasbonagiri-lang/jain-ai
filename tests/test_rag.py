import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from langchain_core.documents import Document

from jain_ai.rag.retrieval import build_context_bundle
from jain_ai.services.chat_service import split_compound_question
from jain_ai.services import response_service


def test_build_context_bundle_returns_folder_and_file_sources():
    docs = [
        Document(
            page_content="The hostel fees are 120000 rupees per year including mess.",
            metadata={"source": "hostel/hostel_facilities_and_fees.txt"},
        ),
        Document(
            page_content="Transport service is available from major Bengaluru routes.",
            metadata={"source": "transport/transport_services.txt"},
        ),
    ]

    result = build_context_bundle("What are the hostel fees?", docs, source_docs=docs)

    assert "120000" in result["context"]
    assert {"folder": "hostel", "file": "hostel_facilities_and_fees.txt"} in result["sources"]


def test_answer_from_context_appends_source_references(monkeypatch):
    monkeypatch.setattr(response_service, "call_text_model", lambda *_args, **_kwargs: "The hostel fees are 120000 rupees per year.")

    answer = response_service.answer_from_context(
        "What are the hostel fees?",
        "Hostel fees: 120000 rupees per year.",
        "system prompt",
        source_references=[{"folder": "hostel", "file": "hostel_facilities_and_fees.txt"}],
    )

    assert "Sources:" in answer
    assert "Folder: hostel | File: hostel_facilities_and_fees.txt" in answer


def test_compound_question_is_split_into_two_sub_questions():
    parts = split_compound_question(
        "what is the highest package in jain and what is the fees for cse aiml in jain"
    )

    assert parts == [
        "what is the highest package in jain?",
        "what is the fees for cse aiml in jain?",
    ]


def test_generic_jain_keyword_does_not_push_irrelevant_club_file_to_top():
    docs = [
        Document(
            page_content="Jain University has many student clubs and activities for all branches.",
            metadata={"source": "clubs/clubs_overview.txt"},
        ),
        Document(
            page_content="What is the fee for CSE AIML: INR 4,00,000 per annum.",
            metadata={"source": "admissions/branch_wise_fees.txt"},
        ),
    ]

    result = build_context_bundle("What is the fees for CSE AIML in Jain?", docs, source_docs=docs)

    assert result["sources"][0] == {"folder": "admissions", "file": "branch_wise_fees.txt"}


def test_fee_intent_outranks_branch_only_club_sources():
    docs = [
        Document(
            page_content="1. ENIGMA - Branch / School: CSE and CSE STAR\n5. Neuron.AI Club - Branch / School: CSE (AI)",
            metadata={"source": "clubs/clubs_list_only.txt"},
        ),
        Document(
            page_content="What is the fee for CSE AIML: INR 4,00,000 per annum",
            metadata={"source": "admissions/branch_wise_fees.txt"},
        ),
    ]

    result = build_context_bundle("what is the fees for cse aiml in jian", docs, source_docs=docs)

    assert result["sources"][:1] == [{"folder": "admissions", "file": "branch_wise_fees.txt"}]


def test_credit_intent_outranks_branch_only_club_sources():
    docs = [
        Document(
            page_content="1. ENIGMA - Branch / School: CSE and CSE STAR\n5. Neuron.AI Club - Branch / School: CSE (AI)",
            metadata={"source": "clubs/clubs_list_only.txt"},
        ),
        Document(
            page_content="PROGRAM TOTALS:\nTotal Number of Subjects: 44\nTotal Program Credits: 165",
            metadata={"source": "academics/cse_aiml_btech_2024_2028.txt"},
        ),
    ]

    result = build_context_bundle("what are the total credits for cse aiml", docs, source_docs=docs)

    assert result["sources"][:1] == [{"folder": "academics", "file": "cse_aiml_btech_2024_2028.txt"}]


def test_ai_query_prefers_cse_ai_curriculum_over_aiml_and_clubs():
    docs = [
        Document(
            page_content="Jain University has multiple student clubs. Neuron.AI Club - Branch / School: CSE (AI)",
            metadata={"source": "clubs/clubs_overview.txt"},
        ),
        Document(
            page_content="PROGRAM TOTALS\nTotal Program Credits: 165\nSpecialization: Artificial Intelligence and Machine Learning",
            metadata={"source": "academics/cse_aiml_btech_2024_2028.txt"},
        ),
        Document(
            page_content="PROGRAM TOTALS\nTotal Program Credits: 164\nSpecialization: Artificial Intelligence",
            metadata={"source": "academics/cse_ai_btech_2024_2028.txt"},
        ),
    ]

    result = build_context_bundle("how many total credits will a cse ai student get", docs, source_docs=docs)

    assert "164" in result["context"]
    assert result["sources"][:1] == [{"folder": "academics", "file": "cse_ai_btech_2024_2028.txt"}]


def test_aiml_query_prefers_cse_aiml_curriculum_over_cse_ai():
    docs = [
        Document(
            page_content="PROGRAM TOTALS\nTotal Program Credits: 164\nSpecialization: Artificial Intelligence",
            metadata={"source": "academics/cse_ai_btech_2024_2028.txt"},
        ),
        Document(
            page_content="PROGRAM TOTALS\nTotal Program Credits: 165\nSpecialization: Artificial Intelligence and Machine Learning",
            metadata={"source": "academics/cse_aiml_btech_2024_2028.txt"},
        ),
    ]

    result = build_context_bundle("what are the total credits for cse aiml", docs, source_docs=docs)

    assert "165" in result["context"]
    assert result["sources"][:1] == [{"folder": "academics", "file": "cse_aiml_btech_2024_2028.txt"}]


def test_devops_query_prefers_devops_curriculum_and_excludes_other_program_totals():
    docs = [
        Document(
            page_content="PROGRAM TOTALS\nTotal Program Credits: 164\nSpecialization: AI-Driven DevOps",
            metadata={"source": "academics/cse_ai_driven_devops_btech_2024_2028.txt"},
        ),
        Document(
            page_content="PROGRAM TOTALS\nTotal Program Credits: 165\nSpecialization: Artificial Intelligence and Machine Learning",
            metadata={"source": "academics/cse_aiml_btech_2024_2028.txt"},
        ),
        Document(
            page_content="PROGRAM TOTALS\nTotal Program Credits: 162\nSpecialization: Data Science",
            metadata={"source": "academics/cse_datascience_btech_2024_2028.txt"},
        ),
    ]

    result = build_context_bundle("how many credits does AI-Driven DevOps will get", docs, source_docs=docs)

    assert "164" in result["context"]
    assert "165" not in result["context"]
    assert "162" not in result["context"]
    assert result["sources"][:1] == [{"folder": "academics", "file": "cse_ai_driven_devops_btech_2024_2028.txt"}]


def test_specialization_overlap_filters_out_unrelated_academic_program_files():
    docs = [
        Document(
            page_content="PROGRAM TOTALS\nTotal Program Credits: 164\nSpecialization: Artificial Intelligence",
            metadata={"source": "academics/cse_ai_btech_2024_2028.txt"},
        ),
        Document(
            page_content="PROGRAM TOTALS\nTotal Program Credits: 165\nSpecialization: Artificial Intelligence and Machine Learning",
            metadata={"source": "academics/cse_aiml_btech_2024_2028.txt"},
        ),
        Document(
            page_content="PROGRAM TOTALS\nTotal Program Credits: 164\nSpecialization: AI-Driven DevOps",
            metadata={"source": "academics/cse_ai_driven_devops_btech_2024_2028.txt"},
        ),
    ]

    result = build_context_bundle("what are the total credits for cse aiml", docs, source_docs=docs)

    assert "165" in result["context"]
    assert "164\n\nPROGRAM TOTALS" not in result["context"]
    assert result["sources"][:1] == [{"folder": "academics", "file": "cse_aiml_btech_2024_2028.txt"}]


def test_ctis_credit_query_prefers_ctis_curriculum_and_excludes_admissions_overview():
    docs = [
        Document(
            page_content="Admissions overview for Jain University with general policy notes.",
            metadata={"source": "admissions/admissions_overview.txt"},
        ),
        Document(
            page_content="PROGRAM TOTALS\nTotal Program Credits: 165\nSpecialization: Artificial Intelligence and Machine Learning",
            metadata={"source": "academics/cse_aiml_btech_2024_2028.txt"},
        ),
        Document(
            page_content="PROGRAM TOTALS\nTotal Program Credits: 164\nSpecialization: Cloud Technology and Information Security (CTIS)",
            metadata={"source": "academics/cse_ctis_btech_2024_2028.txt"},
        ),
    ]

    result = build_context_bundle("what are the total credits for cse ctis in jain", docs, source_docs=docs)

    assert "164" in result["context"]
    assert "165" not in result["context"]
    assert result["sources"][:1] == [{"folder": "academics", "file": "cse_ctis_btech_2024_2028.txt"}]
