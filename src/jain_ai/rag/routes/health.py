from datetime import datetime, timezone

from flask import Blueprint, jsonify

from ...constants.settings import APP_NAME
from ..pipeline import get_rag_pipeline


health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health():
    pipeline = get_rag_pipeline()
    pipeline.initialize()
    return jsonify(
        {
            "status": "ok",
            "app": APP_NAME,
            "time": datetime.now(timezone.utc).isoformat(),
            "vector_store_ready": pipeline.vector_store_ready,
            "documents_loaded": len(pipeline.docs),
        }
    )
