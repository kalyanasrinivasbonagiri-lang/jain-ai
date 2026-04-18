import time

from flask import session

from ..constants.settings import (
    MAX_SESSION_CONTEXT_MESSAGES,
    MAX_SESSION_MESSAGES,
    SESSION_CHAT_KEY,
    SESSION_UPLOAD_FILENAME_KEY,
    SESSION_UPLOAD_TEXT_KEY,
    SESSION_LAST_ACTIVITY_KEY,
    SESSION_TIMEOUT_MINUTES,
)


def _now_ts():
    return int(time.time())


def _normalize_history_entry(entry):
    if isinstance(entry, (list, tuple)) and len(entry) >= 2:
        return {
            "role": entry[0],
            "message": entry[1],
        }

    if isinstance(entry, dict):
        return {
            "role": entry.get("role", ""),
            "message": entry.get("message", ""),
        }

    return {
        "role": "",
        "message": str(entry or ""),
    }


def _is_session_expired():
    last_activity = session.get(SESSION_LAST_ACTIVITY_KEY)
    if not isinstance(last_activity, int):
        return False
    timeout_seconds = SESSION_TIMEOUT_MINUTES * 60
    return (_now_ts() - last_activity) > timeout_seconds


def touch_session_activity():
    session[SESSION_LAST_ACTIVITY_KEY] = _now_ts()
    session.modified = True


def ensure_chat_history():
    if _is_session_expired():
        clear_chat_history()
    if SESSION_CHAT_KEY not in session or not isinstance(session[SESSION_CHAT_KEY], list):
        session[SESSION_CHAT_KEY] = []
    touch_session_activity()


def get_chat_history():
    ensure_chat_history()
    chat_history = [_normalize_history_entry(entry) for entry in session[SESSION_CHAT_KEY]]
    session[SESSION_CHAT_KEY] = chat_history
    return chat_history


def save_chat_history(chat_history):
    normalized_history = [_normalize_history_entry(entry) for entry in chat_history[-MAX_SESSION_MESSAGES:]]
    session[SESSION_CHAT_KEY] = normalized_history
    session.modified = True


def save_uploaded_context(text, filename):
    session[SESSION_UPLOAD_TEXT_KEY] = (text or "").strip()
    session[SESSION_UPLOAD_FILENAME_KEY] = (filename or "").strip()
    session.modified = True


def get_uploaded_context():
    ensure_chat_history()
    return (
        (session.get(SESSION_UPLOAD_TEXT_KEY) or "").strip(),
        (session.get(SESSION_UPLOAD_FILENAME_KEY) or "").strip(),
    )


def has_uploaded_context():
    text, _ = get_uploaded_context()
    return bool(text)


def clear_uploaded_context():
    session.pop(SESSION_UPLOAD_TEXT_KEY, None)
    session.pop(SESSION_UPLOAD_FILENAME_KEY, None)
    session.modified = True


def append_chat_message(role, message, attachment=None):
    chat_history = get_chat_history()
    chat_history.append({
        "role": role,
        "message": message,
    })
    save_chat_history(chat_history)


def clear_chat_history():
    session[SESSION_CHAT_KEY] = []
    clear_uploaded_context()
    touch_session_activity()


def get_recent_chat_context(max_messages=MAX_SESSION_CONTEXT_MESSAGES):
    chat_history = get_chat_history()
    if not chat_history:
        return ""

    recent_messages = chat_history[-max_messages:]
    formatted_lines = []
    for entry in recent_messages:
        speaker = "User" if entry["role"] == "user" else "Assistant"
        formatted_lines.append(f"{speaker}: {entry['message']}")
    return "\n".join(formatted_lines)
