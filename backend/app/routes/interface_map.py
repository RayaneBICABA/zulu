from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from ..schemas.interface_map_schema import ClientPositionSchema
from ..services import interface_map_service


interface_map_bp = Blueprint("interface_map", __name__)
client_position_schema = ClientPositionSchema()


@interface_map_bp.route("/map/commerces-proches", methods=["POST"])
def commerces_proches():
    """
    Recuperer les commerces actifs les plus proches de la position du client.
    ---
    tags:
      - Map
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - latitude
            - longitude
          properties:
            latitude:
              type: number
            longitude:
              type: number
            rayon_km:
              type: number
              default: 25
            limit:
              type: integer
              default: 10
            categorie_id:
              type: integer
    responses:
      200:
        description: Liste des commerces proches avec distance et itineraire
      400:
        description: Erreur de validation
    """
    try:
        data = client_position_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    result = interface_map_service.get_commerces_proches(data)
    return jsonify(result), 200
