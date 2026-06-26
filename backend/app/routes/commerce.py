from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from ..schemas.commerce_schema import CommerceStep1Schema, CommerceStep2Schema, CommerceSchema
from ..schemas.categorie_schema import CategorieCreateSchema
from ..services import commerce_service

commerce_bp = Blueprint("commerce", __name__)
step1_schema = CommerceStep1Schema()
step2_schema = CommerceStep2Schema()
commerce_schema = CommerceSchema()
categorie_create_schema = CategorieCreateSchema()


@commerce_bp.route("/commerces", methods=["POST"])
@jwt_required()
def create_commerce():
    """
    Step 1 — Creer un commerce (draft).
    ---
    tags:
      - Commerce
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - nom_commercial
            - categorie_id
          properties:
            nom_commercial:
              type: string
            whatsapp_numero:
              type: string
            contact_telephonique:
              type: string
            categorie_id:
              type: integer
            description:
              type: string
    responses:
      201:
        description: Commerce cree (draft)
      400:
        description: Erreur de validation
    """
    try:
        data = step1_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    try:
        user_id = int(get_jwt_identity())
        result = commerce_service.create_step1(user_id, data)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@commerce_bp.route("/commerces/<int:commerce_id>/localisation", methods=["PUT"])
@jwt_required()
def update_localisation(commerce_id):
    """
    Step 2 — Ajouter localisation et horaires d'ouverture.
    ---
    tags:
      - Commerce
    security:
      - Bearer: []
    parameters:
      - in: path
        name: commerce_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          required:
            - latitude
            - longitude
            - adresse_complete
            - horaires
          properties:
            latitude:
              type: number
            longitude:
              type: number
            adresse_complete:
              type: string
            horaires:
              type: array
              items:
                type: object
                properties:
                  jour:
                    type: string
                  heure_ouverture:
                    type: string
                  heure_fermeture:
                    type: string
                  est_ferme:
                    type: boolean
                  est_24h:
                    type: boolean
    responses:
      200:
        description: Localisation mise a jour
      400:
        description: Erreur de validation
      403:
        description: Acces refuse
    """
    try:
        data = step2_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    try:
        user_id = int(get_jwt_identity())
        result = commerce_service.update_step2(commerce_id, user_id, data)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@commerce_bp.route("/commerces/<int:commerce_id>/photos", methods=["POST"])
@jwt_required()
def upload_photos(commerce_id):
    """
    Step 3 — Uploader des photos (1 a 3 images).
    ---
    tags:
      - Commerce
    security:
      - Bearer: []
    consumes:
      - multipart/form-data
    parameters:
      - in: path
        name: commerce_id
        type: integer
        required: true
      - in: formData
        name: photos
        type: array
        items:
          type: file
        required: true
        description: Images JPG, PNG ou WebP (max 5MB chacune)
    responses:
      201:
        description: Photos uploadées
      400:
        description: Erreur de validation ou de type
      403:
        description: Acces refuse
    """
    files = request.files.getlist("photos")
    if not files or all(f.filename == "" for f in files):
        return jsonify({"error": "Au moins une photo requise."}), 400

    try:
        user_id = int(get_jwt_identity())
        result = commerce_service.upload_photos(commerce_id, user_id, files)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@commerce_bp.route("/commerces/<int:commerce_id>/photos/<int:photo_id>", methods=["DELETE"])
@jwt_required()
def delete_photo(commerce_id, photo_id):
    """
    Supprimer une photo d'un commerce.
    ---
    tags:
      - Commerce
    security:
      - Bearer: []
    parameters:
      - in: path
        name: commerce_id
        type: integer
        required: true
      - in: path
        name: photo_id
        type: integer
        required: true
    responses:
      200:
        description: Photo supprimee
      403:
        description: Acces refuse
      404:
        description: Photo introuvable
    """
    try:
        user_id = int(get_jwt_identity())
        result = commerce_service.delete_photo(commerce_id, photo_id, user_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@commerce_bp.route("/commerces/<int:commerce_id>/publish", methods=["PATCH"])
@jwt_required()
def publish_commerce(commerce_id):
    """
    Finaliser — Publier le commerce (is_active = true).
    ---
    tags:
      - Commerce
    security:
      - Bearer: []
    parameters:
      - in: path
        name: commerce_id
        type: integer
        required: true
    responses:
      200:
        description: Commerce publie
      400:
        description: Etapes incompletes
      403:
        description: Acces refuse
    """
    try:
        user_id = int(get_jwt_identity())
        result = commerce_service.publish(commerce_id, user_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@commerce_bp.route("/commerces/<int:commerce_id>", methods=["GET"])
@jwt_required()
def get_commerce(commerce_id):
    """
    Recuperer les details d'un commerce.
    ---
    tags:
      - Commerce
    security:
      - Bearer: []
    parameters:
      - in: path
        name: commerce_id
        type: integer
        required: true
    responses:
      200:
        description: Details du commerce
      403:
        description: Acces refuse
      404:
        description: Commerce introuvable
    """
    try:
        user_id = int(get_jwt_identity())
        result = commerce_service.get_commerce(commerce_id, user_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@commerce_bp.route("/categories", methods=["GET"])
def list_categories():
    """
    Lister les categories actives.
    ---
    tags:
      - Commerce
    responses:
      200:
        description: Liste des categories
    """
    categories = commerce_service.list_categories()
    return jsonify([c.to_dict() for c in categories]), 200


@commerce_bp.route("/categories", methods=["POST"])
@jwt_required()
def create_category():
    """
    Creer une nouvelle categorie.
    ---
    tags:
      - Commerce
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - nom
          properties:
            nom:
              type: string
    responses:
      201:
        description: Categorie creee
      400:
        description: Erreur de validation
      401:
        description: Token manquant ou invalide
      409:
        description: La categorie existe deja
    """
    try:
        data = categorie_create_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    try:
        result = commerce_service.create_category(data)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
