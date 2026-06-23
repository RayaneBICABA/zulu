from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from ..models.user import User
from ..models.role import Role, Permission
from ..extensions import db


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Authentification requise."}), 401

            user = User.query.get(int(user_id))
            if not user:
                return jsonify({"error": "Utilisateur introuvable."}), 404

            if not any(user.has_role(role) for role in roles):
                return jsonify({"error": "Acces refuse. Role insuffisant."}), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def permission_required(*permissions):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Authentification requise."}), 401

            user = User.query.get(int(user_id))
            if not user:
                return jsonify({"error": "Utilisateur introuvable."}), 404

            if not any(user.has_permission(perm) for perm in permissions):
                return jsonify({"error": "Acces refuse. Permission insuffisante."}), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator


class RoleService:
    def create_role(self, name, description=None):
        if Role.query.filter_by(name=name).first():
            raise ValueError(f"Le role '{name}' existe deja.")
        role = Role(name=name, description=description)
        role.save()
        return role

    def create_permission(self, codename, name=None, description=None):
        if Permission.query.filter_by(codename=codename).first():
            raise ValueError(f"La permission '{codename}' existe deja.")
        permission = Permission(codename=codename, name=name, description=description)
        permission.save()
        return permission

    def assign_role(self, user_id, role_name):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("Utilisateur introuvable.")
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            raise ValueError(f"Role '{role_name}' introuvable.")
        if role in user.roles:
            raise ValueError("L'utilisateur possede deja ce role.")
        user.roles.append(role)
        user.save()
        return user

    def remove_role(self, user_id, role_name):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("Utilisateur introuvable.")
        role = Role.query.filter_by(name=role_name).first()
        if not role or role not in user.roles:
            raise ValueError("L'utilisateur ne possede pas ce role.")
        user.roles.remove(role)
        user.save()
        return user

    def assign_permission(self, role_name, permission_codename):
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            raise ValueError(f"Role '{role_name}' introuvable.")
        permission = Permission.query.filter_by(codename=permission_codename).first()
        if not permission:
            raise ValueError(f"Permission '{permission_codename}' introuvable.")
        if permission in role.permissions:
            raise ValueError("Le role possede deja cette permission.")
        role.permissions.append(permission)
        role.save()
        return role

    def get_all_roles(self):
        return Role.query.all()

    def get_all_permissions(self):
        return Permission.query.all()

    def get_user_roles(self, user_id):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("Utilisateur introuvable.")
        return user.roles
