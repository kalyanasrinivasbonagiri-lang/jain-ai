from flask import Blueprint, jsonify


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/status", methods=["GET"])
def status():
    return jsonify({"admin": "ready"})
