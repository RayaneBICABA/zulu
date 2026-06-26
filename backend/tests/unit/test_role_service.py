import pytest
from app.services import role_service
from app.models.user import User
from app.models.role import Role, Permission
from app.services import auth_service


class TestRoles:
    def test_create_role(self, app):
        with app.app_context():
            role = role_service.create_role("moderator", "Moderator")
            assert role.id is not None
            assert role.name == "moderator"
            assert role.description == "Moderator"

    def test_create_role_raises_on_duplicate(self, app):
        with app.app_context():
            role_service.create_role("moderator")
            with pytest.raises(ValueError, match="existe deja"):
                role_service.create_role("moderator")

    def test_get_all_roles(self, app):
        with app.app_context():
            role_service.create_role("editor")
            role_service.create_role("viewer")
            roles = role_service.get_all_roles()
            assert len(roles) == 5  # 3 seeded + 2 created

    def test_get_user_roles_raises_on_unknown_user(self, app):
        with app.app_context():
            with pytest.raises(ValueError, match="Utilisateur introuvable"):
                role_service.get_user_roles(9999)


class TestPermissions:
    def test_create_permission(self, app):
        with app.app_context():
            perm = role_service.create_permission("users:read", "Lire les utilisateurs", "Permission de lecture")
            assert perm.id is not None
            assert perm.codename == "users:read"

    def test_create_permission_raises_on_duplicate(self, app):
        with app.app_context():
            role_service.create_permission("posts:delete")
            with pytest.raises(ValueError, match="existe deja"):
                role_service.create_permission("posts:delete")

    def test_get_all_permissions(self, app):
        with app.app_context():
            role_service.create_permission("read")
            role_service.create_permission("write")
            perms = role_service.get_all_permissions()
            assert len(perms) == 2


class TestAssignments:
    def test_assign_role_to_user(self, app):
        with app.app_context():
            user = auth_service.register(email="assign@test.com", password="password123")
            result = role_service.assign_role(user.id, "admin")
            assert result.has_role("admin") is True

    def test_assign_role_raises_on_unknown_user(self, app):
        with app.app_context():
            with pytest.raises(ValueError, match="Utilisateur introuvable"):
                role_service.assign_role(9999, "admin")

    def test_assign_role_raises_on_duplicate(self, app):
        with app.app_context():
            user = auth_service.register(email="dup@test.com", password="password123")
            role_service.assign_role(user.id, "admin")
            with pytest.raises(ValueError, match="possede deja ce role"):
                role_service.assign_role(user.id, "admin")

    def test_remove_role_from_user(self, app):
        with app.app_context():
            user = auth_service.register(email="rm@test.com", password="password123")
            role_service.assign_role(user.id, "admin")
            result = role_service.remove_role(user.id, "admin")
            assert result.has_role("admin") is False

    def test_assign_permission_to_role(self, app):
        with app.app_context():
            role_service.create_role("editor")
            role_service.create_permission("posts:edit")
            role = role_service.assign_permission("editor", "posts:edit")
            assert any(p.codename == "posts:edit" for p in role.permissions)

    def test_assign_permission_raises_on_unknown_role(self, app):
        with app.app_context():
            with pytest.raises(ValueError, match="introuvable"):
                role_service.assign_permission("ghost", "anything")

    def test_user_has_permission_through_role(self, app):
        with app.app_context():
            user = auth_service.register(email="perm@test.com", password="password123")
            role_service.create_permission("users:delete")
            role_service.assign_permission("admin", "users:delete")
            role_service.assign_role(user.id, "admin")
            assert user.has_permission("users:delete") is True
            assert user.has_permission("posts:create") is False
