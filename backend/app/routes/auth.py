from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from ..schemas import RegisterSchema, LoginSchema, UserSchema
from ..services import auth_service
from ..extensions import limiter
from ..models.user import User
from ..models.role import Role
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


@auth_bp.route("/auth/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """
    Rafraichir le token d'acces.
    ---
    tags:
      - Authentification
    responses:
      200:
        description: Nouveau token d'acces
    """
    identity = get_jwt_identity()
    result = auth_service.refresh(identity)
    return jsonify(result), 200


@auth_bp.route("/auth/me", methods=["GET"])
@jwt_required()
def me():
    """
    Recuperer les informations de l'utilisateur connecte.
    ---
    tags:
      - Authentification
    responses:
      200:
        description: Informations de l'utilisateur
    """
    user_id = int(get_jwt_identity())
    try:
        data = auth_service.me(user_id)
        return jsonify(data), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@auth_bp.route("/auth/verify-email", methods=["POST"])
def verify_email():
    """
    Confirmer l'adresse email via un token.
    ---
    tags:
      - Authentification
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - token
          properties:
            token:
              type: string
    responses:
      200:
        description: Email verifie avec succes
      400:
        description: Token invalide ou expire
    """
    data = request.get_json() or {}
    token = data.get("token")
    if not token:
        return jsonify({"error": "Token requis."}), 400

    try:
        user = auth_service.verify_email(token)
        return jsonify({"message": "Email verifie avec succes.", "user": user.to_dict()}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@auth_bp.route("/auth/forgot-password", methods=["POST"])
@limiter.limit("3 per minute")
def forgot_password():
    """
    Envoyer un email de reinitialisation de mot de passe.
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
          properties:
            email:
              type: string
    responses:
      200:
        description: Email envoye si le compte existe
    """
    data = request.get_json() or {}
    email = data.get("email")
    if not email:
        return jsonify({"error": "Email requis."}), 400

    auth_service.forgot_password(email)
    return jsonify({"message": "Si un compte existe avec cet email, un lien de reinitialisation a ete envoye."}), 200


@auth_bp.route("/auth/reset-password", methods=["POST"])
@limiter.limit("3 per minute")
def reset_password():
    """
    Reinitialiser le mot de passe avec un token.
    ---
    tags:
      - Authentification
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - token
            - password
          properties:
            token:
              type: string
            password:
              type: string
              minLength: 8
    responses:
      200:
        description: Mot de passe reinitialise avec succes
      400:
        description: Token invalide ou expire
    """
    data = request.get_json() or {}
    token = data.get("token")
    password = data.get("password")

    if not token or not password:
        return jsonify({"error": "Token et mot de passe requis."}), 400
    if len(password) < 8:
        return jsonify({"error": "Le mot de passe doit contenir au moins 8 caracteres."}), 400

    try:
        auth_service.reset_password(token, password)
        return jsonify({"message": "Mot de passe reinitialise avec succes."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@auth_bp.route("/auth/resend-verification", methods=["POST"])
@jwt_required()
def resend_verification():
    """
    Renvoyer l'email de verification.
    ---
    tags:
      - Authentification
    security:
      - Bearer: []
    responses:
      200:
        description: Email de verification renvoye
      400:
        description: Email deja verifie
      401:
        description: Token manquant ou invalide
      404:
        description: Utilisateur introuvable
    """
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Utilisateur introuvable."}), 404
    if user.is_verified:
        return jsonify({"error": "Email deja verifie."}), 400

    token = generate_verification_token(user.email)
    send_verification_email(user.email, token)
    return jsonify({"message": "Email de verification renvoye."}), 200


@auth_bp.route("/auth/become-artisan", methods=["POST"])
@jwt_required()
def become_artisan():
    """
    Permet a un client de devenir artisan.
    ---
    tags:
      - Authentification
    security:
      - Bearer: []
    responses:
      200:
        description: Role artisan ajoute avec succes
      400:
        description: Deja artisan ou erreur
    """
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Utilisateur introuvable."}), 404

    if user.has_role("artisan"):
        return jsonify({"error": "Vous etes deja artisan."}), 400

    artisan_role = Role.query.filter_by(name="artisan").first()
    if not artisan_role:
        return jsonify({"error": "Role artisan introuvable."}), 500

    user.roles.append(artisan_role)
    user.save()

    return jsonify({
        "message": "Felicitation ! Vous etes maintenant artisan.",
        "user": user.to_dict(),
    }), 200


@auth_bp.route("/auth/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    Deconnexion — le front supprime le token du storage.
    ---
    tags:
      - Authentification
    security:
      - Bearer: []
    responses:
      200:
        description: Deconnexion reussie
      401:
        description: Token manquant ou invalide
    """
    return jsonify({"message": "Deconnexion reussie."}), 200


@auth_bp.route("/auth/clear-users", methods=["POST"])
def clear_users():
    from sqlalchemy import text
    from ..extensions import db

    try:
        db.session.execute(text("DELETE FROM produit_images WHERE commerce_id IN (SELECT id FROM commerces WHERE user_id IN (SELECT id FROM users))"))
        db.session.execute(text("DELETE FROM horaires_ouverture WHERE commerce_id IN (SELECT id FROM commerces WHERE user_id IN (SELECT id FROM users))"))
        db.session.execute(text("DELETE FROM commerce_photos WHERE commerce_id IN (SELECT id FROM commerces WHERE user_id IN (SELECT id FROM users))"))
        db.session.execute(text("DELETE FROM commerce_stats WHERE commerce_id IN (SELECT id FROM commerces WHERE user_id IN (SELECT id FROM users))"))
        db.session.execute(text("DELETE FROM commentaires WHERE commerce_id IN (SELECT id FROM commerces WHERE user_id IN (SELECT id FROM users))"))
        db.session.execute(text("DELETE FROM commentaires WHERE moderated_by IN (SELECT id FROM users)"))
        db.session.execute(text("DELETE FROM commentaires WHERE auteur_id IN (SELECT id FROM users)"))
        db.session.execute(text("DELETE FROM vues_profile WHERE user_id IN (SELECT id FROM users)"))
        db.session.execute(text("DELETE FROM favoris WHERE user_id IN (SELECT id FROM users)"))
        db.session.execute(text("DELETE FROM user_roles WHERE user_id IN (SELECT id FROM users)"))
        db.session.execute(text("DELETE FROM commerces WHERE user_id IN (SELECT id FROM users)"))
        for user in User.query.all():
            db.session.delete(user)
        db.session.commit()

        return jsonify({"message": "Tous les utilisateurs ont ete supprimes."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
