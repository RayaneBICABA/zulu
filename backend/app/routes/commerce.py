from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from ..schemas.commerce_schema import (
    CommerceStep1Schema, CommerceStep2Schema, CommerceSchema,
    FavoriCreateSchema, ProduitImageCreateSchema,
    SwitchCommerceSchema,
)
from ..schemas.categorie_schema import CategorieCreateSchema
from ..schemas.commentaire_schema import CommentaireCreateSchema
from ..services import commerce_service
from ..services.role_service import role_required, RoleService

commerce_bp = Blueprint("commerce", __name__)
step1_schema = CommerceStep1Schema()
step2_schema = CommerceStep2Schema()
commerce_schema = CommerceSchema()
categorie_create_schema = CategorieCreateSchema()
favori_create_schema = FavoriCreateSchema()
produit_image_create_schema = ProduitImageCreateSchema()
commentaire_create_schema = CommentaireCreateSchema()
switch_commerce_schema = SwitchCommerceSchema()


@commerce_bp.route("/commerces", methods=["GET"])
def list_public_commerces():
    """
    Lister les commerces actifs (public).
    ---
    tags:
      - Commerce
    parameters:
      - in: query
        name: q
        type: string
        description: Recherche par nom commercial ou categorie
      - in: query
        name: categorie_id
        type: integer
        description: Filtrer par categorie
      - in: query
        name: page
        type: integer
        default: 1
      - in: query
        name: per_page
        type: integer
        default: 20
    responses:
      200:
        description: Liste des commerces actifs
    """
    from flask import request as req
    search = req.args.get("q", type=str)
    categorie_id = req.args.get("categorie_id", type=int)
    page = req.args.get("page", 1, type=int)
    per_page = req.args.get("per_page", 20, type=int)

    result = commerce_service.list_public_commerces(
        search=search,
        categorie_id=categorie_id,
        page=page,
        per_page=per_page,
    )
    return jsonify(result), 200


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

        from ..models.role import Role
        from ..models.user import User

        user = User.query.get(user_id)
        artisan_role = Role.query.filter_by(name="artisan").first()
        if user and artisan_role and artisan_role not in user.roles:
            user.roles.append(artisan_role)
            user.save()

        return jsonify({**result, "artisan_role_assigned": True}), 200
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
    from ..models.categorie import Categorie
    from ..extensions import db

    if Categorie.query.count() == 0:
        defaults = [
            "Alimentation & Restauration",
            "Sante & Bien-etre",
            "Batiment & Construction",
            "Services & Technologies",
        ]
        for nom in defaults:
            db.session.add(Categorie(nom=nom))
        db.session.commit()

    categories = commerce_service.list_categories()
    return jsonify([c.to_dict() for c in categories]), 200


@commerce_bp.route("/categories", methods=["POST"])
@jwt_required()
@role_required("admin")
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


@commerce_bp.route("/categories/<int:categorie_id>", methods=["PUT", "DELETE"])
@jwt_required()
@role_required("admin")
def manage_category(categorie_id):
    if request.method == "PUT":
        try:
            data = categorie_create_schema.load(request.get_json())
        except ValidationError as err:
            return jsonify({"error": err.messages}), 400
        try:
            result = commerce_service.update_category(categorie_id, data)
            return jsonify(result), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    try:
        result = commerce_service.delete_category(categorie_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@commerce_bp.route("/artisan/home", methods=["GET"])
@jwt_required()
@role_required("artisan")
def artisan_home():
    """
    Dashboard artisan — Bienvenue + stats + commerce complet.
    ---
    tags:
      - Artisan
    security:
      - Bearer: []
    responses:
      200:
        description: Dashboard artisan
      401:
        description: Token manquant ou invalide
      404:
        description: Aucun commerce trouve
    """
    try:
        user_id = int(get_jwt_identity())
        result = commerce_service.get_artisan_home(user_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@commerce_bp.route("/artisan/profile", methods=["GET"])
@jwt_required()
@role_required("artisan")
def artisan_profile():
    """
    Profil artisan — infos user + liste commerces + nb_commerces.
    ---
    tags:
      - Artisan
    security:
      - Bearer: []
    responses:
      200:
        description: Profil artisan
      401:
        description: Token manquant ou invalide
    """
    try:
        user_id = int(get_jwt_identity())
        result = commerce_service.get_artisan_profile(user_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@commerce_bp.route("/artisan/active-commerce", methods=["PATCH"])
@jwt_required()
@role_required("artisan")
def switch_commerce():
    """
    Changer le commerce actif de l'artisan.
    ---
    tags:
      - Artisan
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - commerce_id
          properties:
            commerce_id:
              type: integer
    responses:
      200:
        description: Commerce active
      400:
        description: Erreur de validation
      401:
        description: Token manquant ou invalide
      403:
        description: Acces refuse
      404:
        description: Commerce introuvable
    """
    try:
        data = switch_commerce_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    try:
        user_id = int(get_jwt_identity())
        result = commerce_service.switch_commerce(user_id, data["commerce_id"])
        return jsonify(result), 200
    except ValueError as e:
        error_msg = str(e)
        if "Acces refuse" in error_msg:
            return jsonify({"error": error_msg}), 403
        return jsonify({"error": error_msg}), 404


@commerce_bp.route("/artisan/commerces/cards", methods=["GET"])
@jwt_required()
@role_required("artisan")
def get_commerces_cards():
    """
    Lister les commerces de l'artisan sous forme de cards.
    ---
    tags:
      - Artisan
    security:
      - Bearer: []
    responses:
      200:
        description: Liste des cards commerces
      401:
        description: Token manquant ou invalide
    """
    try:
        user_id = int(get_jwt_identity())
        result = commerce_service.get_commerces_cards(user_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@commerce_bp.route("/commerces/<int:commerce_id>/vues", methods=["POST"])
def record_vue(commerce_id):
    """
    Enregistrer une vue sur le profile d'un commerce.
    ---
    tags:
      - Commerce
    parameters:
      - in: path
        name: commerce_id
        type: integer
        required: true
    responses:
      201:
        description: Vue enregistree
      400:
        description: Commerce introuvable
    """
    try:
        ip = request.remote_addr
        ua = request.headers.get("User-Agent", "")

        user_id = None
        try:
            user_id = int(get_jwt_identity())
        except Exception:
            pass

        result = commerce_service.record_vue(
            commerce_id=commerce_id,
            ip_address=ip,
            user_agent=ua,
            user_id=user_id,
        )
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@commerce_bp.route("/commerces/<int:commerce_id>/favoris", methods=["POST"])
@jwt_required()
def add_favori(commerce_id):
    """
    Ajouter un commerce aux favoris.
    ---
    tags:
      - Favoris
    security:
      - Bearer: []
    parameters:
      - in: path
        name: commerce_id
        type: integer
        required: true
    responses:
      201:
        description: Ajoute aux favoris
      400:
        description: Deja en favori ou commerce introuvable
      401:
        description: Token manquant ou invalide
    """
    try:
        user_id = int(get_jwt_identity())
        result = commerce_service.add_favori(user_id, commerce_id)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@commerce_bp.route("/commerces/<int:commerce_id>/favoris", methods=["DELETE"])
@jwt_required()
def remove_favori(commerce_id):
    """
    Retirer un commerce des favoris.
    ---
    tags:
      - Favoris
    security:
      - Bearer: []
    parameters:
      - in: path
        name: commerce_id
        type: integer
        required: true
    responses:
      200:
        description: Retire des favoris
      400:
        description: Favori introuvable
      401:
        description: Token manquant ou invalide
    """
    try:
        user_id = int(get_jwt_identity())
        result = commerce_service.remove_favori(user_id, commerce_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@commerce_bp.route("/favoris", methods=["GET"])
@jwt_required()
def list_favoris():
    """
    Lister les favoris de l'utilisateur connecte.
    ---
    tags:
      - Favoris
    security:
      - Bearer: []
    responses:
      200:
        description: Liste des favoris avec details commerce
      401:
        description: Token manquant ou invalide
    """
    try:
        user_id = int(get_jwt_identity())
        result = commerce_service.list_favoris(user_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@commerce_bp.route("/commerces/<int:commerce_id>/produit-images", methods=["POST"])
@jwt_required()
def upload_produit_image(commerce_id):
    """
    Uploader une image de produit (max 5, uniquement si is_vendeur_produits).
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
        name: image
        type: file
        required: true
        description: Image JPG, PNG ou WebP (max 5MB)
    responses:
      201:
        description: Image uploadée
      400:
        description: Erreur de validation
      403:
        description: Acces refuse ou non vendeur
    """
    file = request.files.get("image")
    if not file or file.filename == "":
        return jsonify({"error": "Une image requise."}), 400

    try:
        user_id = int(get_jwt_identity())
        result = commerce_service.upload_produit_image(commerce_id, user_id, file)
        return jsonify(result), 201
    except ValueError as e:
        error_msg = str(e)
        if "vendeur" in error_msg.lower():
            return jsonify({"error": error_msg}), 403
        return jsonify({"error": error_msg}), 400


@commerce_bp.route("/commerces/<int:commerce_id>/produit-images/<int:image_id>", methods=["DELETE"])
@jwt_required()
def delete_produit_image(commerce_id, image_id):
    """
    Supprimer une image de produit.
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
        name: image_id
        type: integer
        required: true
    responses:
      200:
        description: Image supprimee
      400:
        description: Image introuvable
      403:
        description: Acces refuse
    """
    try:
        user_id = int(get_jwt_identity())
        result = commerce_service.delete_produit_image(commerce_id, image_id, user_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@commerce_bp.route("/commerces/<int:commerce_id>/geolocalisation", methods=["GET"])
@jwt_required()
def share_geolocalisation(commerce_id):
    """
    Generer un lien WhatsApp pour partager la geolocalisation du commerce.
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
        description: Lien WhatsApp genere
      400:
        description: Commerce introuvable ou localisation manquante
    """
    try:
        user_id = int(get_jwt_identity())
        result = commerce_service.build_geolocalisation_url(commerce_id, user_id)
        return jsonify({"geolocalisation_url": result}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@commerce_bp.route("/commerces/<int:commerce_id>/rating", methods=["GET"])
def get_commerce_rating(commerce_id):
    """
    Recuperer la note IA et les etoiles d'un commerce.
    ---
    tags:
      - Commerce
    parameters:
      - in: path
        name: commerce_id
        type: integer
        required: true
    responses:
      200:
        description: Note et etoiles du commerce
        schema:
          type: object
          properties:
            commerce_id:
              type: integer
            average_rating:
              type: number
            rating_count:
              type: integer
            etoiles:
              type: object
              properties:
                pleines:
                  type: integer
                demies:
                  type: integer
                vides:
                  type: integer
      404:
        description: Commerce introuvable
    """
    from app.models.commerce import Commerce, CommerceStats
    from app.services.ai_service import compute_etoiles

    commerce = Commerce.query.get(commerce_id)
    if not commerce:
        return jsonify({"error": "Commerce introuvable."}), 404

    stats = CommerceStats.query.filter_by(commerce_id=commerce_id).first()
    average_rating = float(stats.average_rating) if stats and stats.average_rating else 0.0
    rating_count = stats.rating_count if stats else 0

    return jsonify({
        "commerce_id": commerce_id,
        "average_rating": average_rating,
        "rating_count": rating_count,
        "etoiles": compute_etoiles(average_rating),
    }), 200


@commerce_bp.route("/commerces/<int:commerce_id>/commentaires", methods=["POST"])
@jwt_required()
def create_commentaire(commerce_id):
    """
    Laisser un commentaire sur un commerce.
    ---
    tags:
      - Commentaires
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
            - contenu
          properties:
            contenu:
              type: string
              maxLength: 2000
    responses:
      201:
        description: Commentaire cree
      400:
        description: Erreur de validation
      401:
        description: Token manquant ou invalide
      403:
        description: Acces refuse (proprietaire du commerce)
    """
    try:
        data = commentaire_create_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    try:
        user_id = int(get_jwt_identity())
        result = commerce_service.create_commentaire(user_id, commerce_id, data)
        return jsonify(result), 201
    except ValueError as e:
        error_msg = str(e)
        if "propre commerce" in error_msg:
            return jsonify({"error": error_msg}), 403
        return jsonify({"error": error_msg}), 400


@commerce_bp.route("/commerces/<int:commerce_id>/commentaires", methods=["GET"])
def list_commentaires(commerce_id):
    """
    Lister les commentaires d'un commerce.
    ---
    tags:
      - Commentaires
    parameters:
      - in: path
        name: commerce_id
        type: integer
        required: true
    responses:
      200:
        description: Liste des commentaires
        schema:
          type: object
          properties:
            nb_commentaires:
              type: integer
            commentaires:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  contenu:
                    type: string
                  created_at:
                    type: string
                    format: date-time
                  auteur:
                    type: object
                    properties:
                      id:
                        type: integer
                      first_name:
                        type: string
                      last_name:
                        type: string
      404:
        description: Commerce introuvable
    """
    try:
        result = commerce_service.list_commentaires(commerce_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@commerce_bp.route("/commerces/<int:commerce_id>/commentaires/<int:commentaire_id>", methods=["DELETE"])
@jwt_required()
def delete_commentaire(commerce_id, commentaire_id):
    """
    Supprimer un commentaire (auteur uniquement).
    ---
    tags:
      - Commentaires
    security:
      - Bearer: []
    parameters:
      - in: path
        name: commerce_id
        type: integer
        required: true
      - in: path
        name: commentaire_id
        type: integer
        required: true
    responses:
      200:
        description: Commentaire supprime
      401:
        description: Token manquant ou invalide
      403:
        description: Acces refuse (pas l'auteur)
      404:
        description: Commentaire introuvable
    """
    try:
        user_id = int(get_jwt_identity())
        result = commerce_service.delete_commentaire(user_id, commentaire_id)
        return jsonify(result), 200
    except ValueError as e:
        error_msg = str(e)
        if "Acces refuse" in error_msg:
            return jsonify({"error": error_msg}), 403
        return jsonify({"error": error_msg}), 404
