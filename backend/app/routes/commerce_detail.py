from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from marshmallow import ValidationError
from ..schemas.commerce_detail_schema import CommerceDetailPositionSchema, CommerceAvisCreateSchema
from ..services.commerce_detail_service import CommerceDetailService


commerce_detail_bp = Blueprint("commerce_detail", __name__)
position_schema = CommerceDetailPositionSchema()
avis_create_schema = CommerceAvisCreateSchema()
commerce_detail_service = CommerceDetailService()


@commerce_detail_bp.route("/commerces/<int:commerce_id>/detail", methods=["GET"])
def get_commerce_detail(commerce_id):
    """
    Recuperer le detail public d'un commerce.
    ---
    tags:
      - Commerce Detail
    parameters:
      - in: path
        name: commerce_id
        type: integer
        required: true
      - in: query
        name: latitude
        type: number
      - in: query
        name: longitude
        type: number
    responses:
      200:
        description: Detail du commerce
      400:
        description: Erreur de validation
      404:
        description: Commerce introuvable
    """
    try:
        data = position_schema.load(request.args)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    user_id = None
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        user_id = int(identity) if identity else None
    except Exception:
        user_id = None

    try:
        result = commerce_detail_service.get_detail(commerce_id, data, user_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@commerce_detail_bp.route("/commerces/<int:commerce_id>/avis", methods=["POST"])
@jwt_required()
def create_commerce_avis(commerce_id):
    """
    Laisser un avis sur un commerce.
    ---
    tags:
      - Commerce Detail
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
            - note
          properties:
            note:
              type: integer
              minimum: 1
              maximum: 5
            commentaire:
              type: string
    responses:
      201:
        description: Avis cree
      400:
        description: Erreur de validation
      401:
        description: Token manquant ou invalide
    """
    try:
        data = avis_create_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    try:
        user_id = int(get_jwt_identity())
        result = commerce_detail_service.create_avis(commerce_id, user_id, data)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
