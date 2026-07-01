import logging
from functools import wraps
from flask import request, jsonify, g
from ..models.user import User
from ..services.firebase_auth import verify_token

logger = logging.getLogger(__name__)


def firebase_login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token manquant."}), 401

        token = auth_header.split(" ", 1)[1]
        decoded = verify_token(token)
        if not decoded:
            return jsonify({"error": "Token invalide ou expire."}), 401

        firebase_uid = decoded.get("uid")
        user = User.query.filter_by(firebase_uid=firebase_uid).first()
        if not user:
            return jsonify({"error": "Utilisateur introuvable."}), 401
        if not user.is_active:
            return jsonify({"error": "Ce compte est desactive."}), 401

        g.current_user = user
        g.firebase_claims = decoded
        return f(*args, **kwargs)
    return decorated


def get_firebase_user():
    return getattr(g, "current_user", None)


def get_firebase_claims():
    return getattr(g, "firebase_claims", {})
