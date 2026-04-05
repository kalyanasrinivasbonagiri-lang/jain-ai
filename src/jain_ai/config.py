import os

from .constants.settings import (
    DEFAULT_FLASK_SECRET_KEY,
    DEFAULT_HOST,
    DEFAULT_LOG_LEVEL,
    DEFAULT_MAX_FILE_SIZE_BYTES,
    DEFAULT_PORT,
)
from .utils.file_utils import ensure_directories, first_existing_path, load_local_env
from .utils.logging_utils import configure_logging


BASE_DIR = first_existing_path(".")
load_local_env(os.path.join(BASE_DIR, ".env"))

TEMPLATE_DIR = first_existing_path("templates", os.path.join("src", "jain_ai_assistant", "templates"))
STATIC_DIR = first_existing_path("static")
DATA_DIR = first_existing_path("data")
RAW_DATA_DIR = first_existing_path(os.path.join("data", "raw", "academics"), "data")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
UPLOADS_DIR = os.path.join(DATA_DIR, "uploads")
STORAGE_DIR = first_existing_path("storage")
VECTOR_DB_DIR = os.path.join(STORAGE_DIR, "vector_db")
EMBEDDING_MODEL_PATH = os.path.join(STORAGE_DIR, "embedding_model.txt")
LOGS_DIR = os.path.join(STORAGE_DIR, "logs")
CACHE_DIR = os.path.join(STORAGE_DIR, "cache")
PROCESSED_FILES_PATH = os.path.join(STORAGE_DIR, "processed_files.txt")

ensure_directories(
    DATA_DIR,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    UPLOADS_DIR,
    STORAGE_DIR,
    VECTOR_DB_DIR,
    LOGS_DIR,
    CACHE_DIR,
)
configure_logging(os.environ.get("LOG_LEVEL", DEFAULT_LOG_LEVEL))


def apply_app_config(app):
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", DEFAULT_FLASK_SECRET_KEY)
    app.config["MAX_CONTENT_LENGTH"] = DEFAULT_MAX_FILE_SIZE_BYTES
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = os.environ.get("SESSION_COOKIE_SECURE", "false").lower() == "true"
    return app


def get_runtime_host():
    return os.environ.get("HOST", DEFAULT_HOST)


def get_runtime_port():
    return int(os.environ.get("PORT", str(DEFAULT_PORT)))
