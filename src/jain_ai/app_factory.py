from flask import Flask, redirect, render_template, request, url_for
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import RequestEntityTooLarge

from .config import STATIC_DIR, TEMPLATE_DIR, apply_app_config
from .constants.settings import APP_NAME, MAX_FILE_SIZE_MB
from .extensions import initialize_extensions
from .rag.routes import register_blueprints
from .services.session_service import ensure_chat_history, get_chat_history
from .utils.logging_utils import get_logger


logger = get_logger(APP_NAME.lower().replace(" ", "_"))


def create_app():
    app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
    apply_app_config(app)
    initialize_extensions()
    register_blueprints(app)

    @app.route("/favicon.ico")
    def favicon():
        return redirect(url_for("static", filename="favicon.svg"), code=302)
    @app.before_request
    def prepare_request():
        ensure_chat_history()

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return error
    @app.errorhandler(RequestEntityTooLarge)
    def handle_file_too_large(_error):
        logger.warning("Rejected oversized upload from %s", request.remote_addr)
        return render_template(
            "index.html",
            chat_history=get_chat_history() + [["bot", f"File is too large. Maximum upload size is {MAX_FILE_SIZE_MB} MB."]],
        ), 413

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        logger.exception("Unhandled application error: %s", error)
        return render_template(
            "index.html",
            chat_history=get_chat_history() + [["bot", "Something went wrong. Please try again in a moment."]],
        ), 500

    return app
