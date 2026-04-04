import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from flask import Flask, session

from jain_ai.constants.settings import SESSION_CHAT_KEY, SESSION_LAST_ACTIVITY_KEY
from jain_ai.services import session_service


def build_test_app():
    app = Flask(__name__)
    app.secret_key = "test-secret"
    return app


def test_expired_session_history_is_cleared(monkeypatch):
    app = build_test_app()

    with app.test_request_context("/"):
        session[SESSION_CHAT_KEY] = [["user", "Old question"], ["bot", "Old answer"]]
        session[SESSION_LAST_ACTIVITY_KEY] = 100

        monkeypatch.setattr(session_service, "_now_ts", lambda: 4000)
        session_service.ensure_chat_history()

        assert session_service.get_chat_history() == []
        assert session[SESSION_LAST_ACTIVITY_KEY] == 4000


def test_recent_chat_context_uses_latest_messages():
    app = build_test_app()

    with app.test_request_context("/"):
        session[SESSION_CHAT_KEY] = [
            ["user", "Tell me about the coding club"],
            ["bot", "The coding club meets weekly."],
            ["user", "Who is the coordinator?"],
            ["bot", "The source does not include that detail."],
        ]

        context = session_service.get_recent_chat_context(max_messages=3)

        assert "User: Tell me about the coding club" not in context
        assert "Assistant: The coding club meets weekly." in context
        assert "User: Who is the coordinator?" in context
        assert "Assistant: The source does not include that detail." in context
