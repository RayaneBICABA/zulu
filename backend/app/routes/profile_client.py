from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..schemas import ProfileClientSchema
from ..services.profile_client_service import ProfileClientService

profile_user_bp = Blueprint("profile", __name__)
profile_schema = ProfileClientSchema()
profile_service = ProfileClientService()


@profile_user_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    """
    Récupérer le profil de l'utilisateur connecté.
    ---
    tags:
      - Profil
    security:
      - Bearer: []
    responses:
      200:
        description: Profil utilisateur récupéré avec succès.
      404:
        description: Utilisateur introuvable.
    """
    try:
        user_id = int(get_jwt_identity())
        profile = profile_service.get_profile(user_id)
        return jsonify(profile_schema.dump(profile)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception:
        return jsonify({"error": "Une erreur interne est survenue."}), 500