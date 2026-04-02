from flask import Blueprint, redirect, render_template, request, url_for

from ..services.chat_service import handle_chat_turn
from ..services.session_service import clear_chat_history, get_chat_history


web_bp = Blueprint("web", __name__)


@web_bp.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if request.form.get("reset_chat") == "1":
            clear_chat_history()
            return redirect(url_for("web.home"))

        user_input = (request.form.get("query") or "").strip()
        file = request.files.get("file")

        if not user_input and not (file and file.filename):
            return render_template("index.html", chat_history=get_chat_history())

        handle_chat_turn(user_input, file)
        return redirect(url_for("web.home"))

    return render_template("index.html", chat_history=get_chat_history())
