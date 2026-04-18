import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from flask import Flask

from jain_ai.services import chat_service
from jain_ai.services.session_service import get_uploaded_context


def build_test_app():
    app = Flask(__name__)
    app.secret_key = "test-secret"
    return app


def test_follow_up_uses_saved_uploaded_context(monkeypatch):
    app = build_test_app()

    with app.test_request_context("/"):
        monkeypatch.setattr(chat_service, "route_request", lambda *args, **kwargs: "upload")
        monkeypatch.setattr(
            chat_service,
            "answer_from_context",
            lambda query, context, system_prompt, chat_context="": f"Answered from file: {query} | {context}",
        )

        chat_service.save_uploaded_context("Candidate skills: Python, SQL", "resume.pdf")

        reply = chat_service.handle_chat_turn("What are his skills?", None)

        assert "Answered from file: What are his skills?" in reply
        assert "Candidate skills: Python, SQL" in reply


def test_new_upload_persists_extracted_text(monkeypatch):
    app = build_test_app()

    class DummyFile:
        filename = "resume.pdf"

    with app.test_request_context("/"):
        monkeypatch.setattr(chat_service, "route_request", lambda *args, **kwargs: "upload")
        monkeypatch.setattr(
            chat_service,
            "extract_uploaded_text",
            lambda _file: ("Candidate skills: Python, SQL", "resume.pdf", None),
        )
        monkeypatch.setattr(
            chat_service,
            "answer_from_context",
            lambda query, context, system_prompt, chat_context="": f"Answered from file: {query} | {context}",
        )

        reply = chat_service.handle_chat_turn("What is the candidate's name?", DummyFile())
        saved_text, saved_filename = get_uploaded_context()

        assert "Answered from file: What is the candidate's name?" in reply
        assert saved_text == "Candidate skills: Python, SQL"
        assert saved_filename == "resume.pdf"
