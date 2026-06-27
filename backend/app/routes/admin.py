from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import Schema, fields, validate
from marshmallow import ValidationError
from ..services import role_service
from ..services.role_service import role_required, permission_required

admin_bp = Blueprint("admin", __name__)


class RoleSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=80))
    description = fields.Str(validate=validate.Length(max=255))


class PermissionSchema(Schema):
    codename = fields.Str(required=True, validate=validate.Length(min=2, max=80))
    name = fields.Str(validate=validate.Length(max=255))
    description = fields.Str(validate=validate.Length(max=255))


class AssignRoleSchema(Schema):
    user_id = fields.Int(required=True)
    role_name = fields.Str(required=True)


role_schema = RoleSchema()
perm_schema = PermissionSchema()
assign_schema = AssignRoleSchema()


@admin_bp.route("/admin/roles", methods=["GET"])
@jwt_required()
@role_required("admin")
def list_roles():
    """
    Lister tous les roles.
    ---
    tags:
      - Administration
    responses:
      200:
        description: Liste des roles
    """
    roles = role_service.get_all_roles()
    return jsonify([r.to_dict() for r in roles]), 200


@admin_bp.route("/admin/roles", methods=["POST"])
@jwt_required()
@role_required("admin")
def create_role():
    """
    Creer un nouveau role.
    ---
    tags:
      - Administration
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              minLength: 2
            description:
              type: string
    responses:
      201:
        description: Role cree
      400:
        description: Erreur de validation
      401:
        description: Token manquant ou invalide
      403:
        description: Acces refuse (role admin requis)
      409:
        description: Le role existe deja
    """
    try:
        data = role_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    try:
        role = role_service.create_role(data["name"], data.get("description"))
        return jsonify(role.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409


@admin_bp.route("/admin/permissions", methods=["GET"])
@jwt_required()
@role_required("admin")
def list_permissions():
    """
    Lister toutes les permissions.
    ---
    tags:
      - Administration
    security:
      - Bearer: []
    responses:
      200:
        description: Liste des permissions
      401:
        description: Token manquant ou invalide
      403:
        description: Acces refuse (role admin requis)
    """
    permissions = role_service.get_all_permissions()
    return jsonify([p.to_dict() for p in permissions]), 200


@admin_bp.route("/admin/permissions", methods=["POST"])
@jwt_required()
@role_required("admin")
def create_permission():
    """
    Creer une nouvelle permission.
    ---
    tags:
      - Administration
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - codename
          properties:
            codename:
              type: string
              minLength: 2
            name:
              type: string
            description:
              type: string
    responses:
      201:
        description: Permission creee
      400:
        description: Erreur de validation
      401:
        description: Token manquant ou invalide
      403:
        description: Acces refuse (role admin requis)
      409:
        description: La permission existe deja
    """
    try:
        data = perm_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    try:
        permission = role_service.create_permission(data["codename"], data.get("name"), data.get("description"))
        return jsonify(permission.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409


@admin_bp.route("/admin/users/<int:user_id>/roles", methods=["POST"])
@jwt_required()
@role_required("admin")
def assign_role(user_id):
    """
    Assigner un role a un utilisateur.
    ---
    tags:
      - Administration
    security:
      - Bearer: []
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          required:
            - role_name
          properties:
            role_name:
              type: string
    responses:
      200:
        description: Role assigne
      400:
        description: Erreur de validation
      401:
        description: Token manquant ou invalide
      403:
        description: Acces refuse (role admin requis)
    """
    data = request.get_json() or {}
    role_name = data.get("role_name")
    if not role_name:
        return jsonify({"error": "role_name requis."}), 400

    try:
        user = role_service.assign_role(user_id, role_name)
        return jsonify({"message": "Role assigne.", "user": user.to_dict()}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@admin_bp.route("/admin/users/<int:user_id>/roles", methods=["DELETE"])
@jwt_required()
@role_required("admin")
def remove_role(user_id):
    """
    Retirer un role a un utilisateur.
    ---
    tags:
      - Administration
    security:
      - Bearer: []
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          required:
            - role_name
          properties:
            role_name:
              type: string
    responses:
      200:
        description: Role retire
      400:
        description: Erreur de validation
      401:
        description: Token manquant ou invalide
      403:
        description: Acces refuse (role admin requis)
    """
    data = request.get_json() or {}
    role_name = data.get("role_name")
    if not role_name:
        return jsonify({"error": "role_name requis."}), 400

    try:
        user = role_service.remove_role(user_id, role_name)
        return jsonify({"message": "Role retire.", "user": user.to_dict()}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@admin_bp.route("/admin/users/<int:user_id>/roles", methods=["GET"])
@jwt_required()
@role_required("admin")
def get_user_roles(user_id):
    """
    Voir les roles d'un utilisateur.
    ---
    tags:
      - Administration
    security:
      - Bearer: []
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
    responses:
      200:
        description: Liste des roles de l'utilisateur
      401:
        description: Token manquant ou invalide
      403:
        description: Acces refuse (role admin requis)
      404:
        description: Utilisateur introuvable
    """
    try:
        roles = role_service.get_user_roles(user_id)
        return jsonify([r.to_dict() for r in roles]), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@admin_bp.route("/admin/roles/<role_name>/permissions", methods=["POST"])
@jwt_required()
@role_required("admin")
def assign_permission(role_name):
    """
    Assigner une permission a un role.
    ---
    tags:
      - Administration
    security:
      - Bearer: []
    parameters:
      - in: path
        name: role_name
        type: string
        required: true
      - in: body
        name: body
        schema:
          type: object
          required:
            - permission_codename
          properties:
            permission_codename:
              type: string
    responses:
      200:
        description: Permission assignee au role
      400:
        description: Erreur de validation
      401:
        description: Token manquant ou invalide
      403:
        description: Acces refuse (role admin requis)
    """
    data = request.get_json() or {}
    permission_codename = data.get("permission_codename")
    if not permission_codename:
        return jsonify({"error": "permission_codename requis."}), 400

    try:
        role = role_service.assign_permission(role_name, permission_codename)
        return jsonify({"message": "Permission assignee au role.", "role": role.to_dict()}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
