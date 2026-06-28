import logging
from flask import Blueprint, request, jsonify, g
from ..models.user import User
from ..models.role import Role
from ..services.firebase_auth import verify_token
from ..middleware.firebase_middleware import firebase_login_required
from ..extensions import db, limiter

logger = logging.getLogger(__name__)

firebase_auth_bp = Blueprint("firebase_auth", __name__)


@firebase_auth_bp.route("/auth/firebase-login", methods=["POST"])
@limiter.limit("10 per minute")
def firebase_login():
    data = request.get_json() or {}
    token = data.get("token")
    if not token:
        return jsonify({"error": "Token requis."}), 400

    decoded = verify_token(token)
    if not decoded:
        return jsonify({"error": "Token invalide."}), 401

    firebase_uid = decoded.get("uid")
    email = decoded.get("email", "")
    name = decoded.get("name", "")
    first_name = data.get("first_name") or decoded.get("given_name", "")
    last_name = data.get("last_name") or decoded.get("family_name", "")
    email_verified = decoded.get("email_verified", False)

    if not email:
        return jsonify({"error": "Email non fourni par Firebase."}), 400

    user = User.query.filter_by(firebase_uid=firebase_uid).first()
    if not user:
        user = User.query.filter_by(email=email).first()
        if user:
            user.firebase_uid = firebase_uid
            user.is_verified = email_verified or user.is_verified
        else:
            user = User(
                email=email,
                firebase_uid=firebase_uid,
                first_name=first_name or name.split()[0] if name else None,
                last_name=last_name or " ".join(name.split()[1:]) if name else None,
                is_verified=email_verified,
            )
            user.save()
            client_role = Role.query.filter_by(name="client").first()
            if client_role:
                user.roles.append(client_role)
                user.save()

    return jsonify({
        "user": user.to_dict(),
        "token": token,
    }), 200


@firebase_auth_bp.route("/auth/me", methods=["GET"])
@firebase_login_required
def me():
    return jsonify(g.current_user.to_dict()), 200
