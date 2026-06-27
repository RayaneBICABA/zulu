import pytest
from app.services import auth_service
from app.services.profile_client_service import ProfileClientService
from app.models.role import Role
from app.extensions import db


class TestGetProfile:
    def test_returns_all_expected_fields(self, app):
        with app.app_context():
            user = auth_service.register(email="fields@test.com", password="password123")
            profile = ProfileClientService.get_profile(user.id)
            assert profile["id"] == user.id
            assert profile["email"] == "fields@test.com"
            assert profile["first_name"] is None
            assert profile["last_name"] is None
            assert profile["is_verified"] is False
            assert profile["is_active"] is True
            assert isinstance(profile["roles"], list)
            assert isinstance(profile["can_become_artisan"], bool)
            assert profile["created_at"] is not None
            assert profile["updated_at"] is not None

    def test_returns_correct_email(self, app):
        with app.app_context():
            user = auth_service.register(email="profile@test.com", password="password123")
            profile = ProfileClientService.get_profile(user.id)
            assert profile["email"] == "profile@test.com"

    def test_raises_on_unknown_user(self, app):
        with app.app_context():
            with pytest.raises(ValueError, match="Utilisateur introuvable"):
                ProfileClientService.get_profile(9999)

    def test_roles_is_empty_list_by_default(self, app):
        with app.app_context():
            user = auth_service.register(email="noroles@test.com", password="password123")
            profile = ProfileClientService.get_profile(user.id)
            assert profile["roles"] == ["client"]

    def test_roles_contains_assigned_role(self, app):
        with app.app_context():
            user = auth_service.register(email="withrole@test.com", password="password123")
            role = Role.query.filter_by(name="citizen").first()
            if not role:
                role = Role(name="citizen")
                db.session.add(role)
                db.session.commit()
            user.roles.append(role)
            user.save()
            profile = ProfileClientService.get_profile(user.id)
            assert "citizen" in profile["roles"]


class TestCanBecomeArtisan:
    def test_returns_true_for_active_verified_user(self, app):
        with app.app_context():
            user = auth_service.register(email="can@test.com", password="password123")
            user.is_verified = True
            user.save()
            assert ProfileClientService.can_become_artisan(user) is True

    def test_returns_false_if_not_verified(self, app):
        with app.app_context():
            user = auth_service.register(email="notverif@test.com", password="password123")
            assert ProfileClientService.can_become_artisan(user) is False

    def test_returns_false_if_inactive(self, app):
        with app.app_context():
            user = auth_service.register(email="notactive@test.com", password="password123")
            user.is_verified = True
            user.is_active = False
            user.save()
            assert ProfileClientService.can_become_artisan(user) is False

    def test_returns_false_if_already_artisan(self, app):
        with app.app_context():
            user = auth_service.register(email="isartisan@test.com", password="password123")
            user.is_verified = True
            role = Role.query.filter_by(name="artisan").first()
            if not role:
                role = Role(name="artisan")
                db.session.add(role)
                db.session.commit()
            user.roles.append(role)
            user.save()
            assert ProfileClientService.can_become_artisan(user) is False

    def test_returns_false_if_admin(self, app):
        with app.app_context():
            user = auth_service.register(email="isadmin@test.com", password="password123")
            user.is_verified = True
            role = Role.query.filter_by(name="admin").first()
            if not role:
                role = Role(name="admin")
                db.session.add(role)
                db.session.commit()
            user.roles.append(role)
            user.save()
            assert ProfileClientService.can_become_artisan(user) is False

    def test_can_become_artisan_reflected_in_profile(self, app):
        with app.app_context():
            user = auth_service.register(email="reflect@test.com", password="password123")
            user.is_verified = True
            user.save()
            profile = ProfileClientService.get_profile(user.id)
            assert profile["can_become_artisan"] is True

    def test_cannot_become_artisan_reflected_in_profile(self, app):
        with app.app_context():
            user = auth_service.register(email="noreflect@test.com", password="password123")
            profile = ProfileClientService.get_profile(user.id)
            assert profile["can_become_artisan"] is False