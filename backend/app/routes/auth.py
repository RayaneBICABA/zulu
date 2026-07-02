from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from ..schemas import RegisterSchema, LoginSchema, UserSchema
from ..services import auth_service
from ..extensions import limiter
from ..models.user import User

from ..services.email_service import generate_verification_token, send_verification_email

auth_bp = Blueprint("auth", __name__)
register_schema = RegisterSchema()
login_schema = LoginSchema()
user_schema = UserSchema()


@auth_bp.route("/auth/register", methods=["POST"])
@limiter.limit("3 per minute")
def register():
    """
    Inscription d'un nouvel utilisateur.
    ---
    tags:
      - Authentification
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              format: email
            password:
              type: string
              minLength: 8
            first_name:
              type: string
            last_name:
              type: string
    responses:
      201:
        description: Utilisateur cree avec succes
      400:
        description: Erreur de validation
      409:
        description: Email deja utilise
    """
    try:
        data = register_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    try:
        user = auth_service.register(
            email=data["email"],
            password=data["password"],
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
        )
        return jsonify({"message": "Inscription reussie.", "user": user.to_dict()}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409


@auth_bp.route("/auth/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    """
    Connexion d'un utilisateur.
    ---
    tags:
      - Authentification
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: Connexion reussie, retourne les tokens
      400:
        description: Erreur de validation
      401:
        description: Identifiants incorrects
    """
    try:
        data = login_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    try:
        result = auth_service.login(data["email"], data["password"])
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
