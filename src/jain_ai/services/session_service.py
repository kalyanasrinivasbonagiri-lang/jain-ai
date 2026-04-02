from flask import session

from ..constants.settings import MAX_SESSION_MESSAGES, SESSION_CHAT_KEY


def ensure_chat_history():
    if SESSION_CHAT_KEY not in session or not isinstance(session[SESSION_CHAT_KEY], list):
        session[SESSION_CHAT_KEY] = []


def get_chat_history():
    ensure_chat_history()
    return session[SESSION_CHAT_KEY]


def save_chat_history(chat_history):
    session[SESSION_CHAT_KEY] = chat_history[-MAX_SESSION_MESSAGES:]
    session.modified = True


def append_chat_message(role, message):
    chat_history = get_chat_history()
    chat_history.append([role, message])
    save_chat_history(chat_history)


def clear_chat_history():
    session[SESSION_CHAT_KEY] = []
    session.modified = True
