from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)

@health_bp.route("/health", methods=["GET"])
def health_check():
    """
    Vérifie que l'API est opérationnelle.
    ---
    tags:
      - Health
    responses:
      200:
        description: API en ligne et opérationnelle
    """
    return jsonify({
        "status": "ok",
        "message": "Zawani API is running"
    }), 200
