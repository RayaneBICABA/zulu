import pytest
from app.services import auth_service
from app.models.user import User


class TestRegister:
    def test_register_creates_user(self, app):
        with app.app_context():
            user = auth_service.register(
                email="test@test.com",
                password="password123",
                first_name="John",
                last_name="Doe",
            )
            assert user.id is not None
            assert user.email == "test@test.com"
            assert user.first_name == "John"
            assert user.last_name == "Doe"
            assert user.check_password("password123") is True
            assert user.is_verified is False
            assert user.is_active is True

    def test_register_raises_on_duplicate_email(self, app):
        with app.app_context():
            auth_service.register(email="dup@test.com", password="password123")
            with pytest.raises(ValueError, match="Un compte avec cet email existe deja"):
                auth_service.register(email="dup@test.com", password="other456")


class TestLogin:
    def test_login_returns_tokens(self, app):
        with app.app_context():
            auth_service.register(email="log@test.com", password="password123")
            result = auth_service.login("log@test.com", "password123")
            assert "access_token" in result
            assert "refresh_token" in result
            assert "user" in result
            assert result["user"]["email"] == "log@test.com"

    def test_login_raises_on_wrong_password(self, app):
        with app.app_context():
            auth_service.register(email="wp@test.com", password="password123")
            with pytest.raises(ValueError, match="Email ou mot de passe incorrect"):
                auth_service.login("wp@test.com", "wrongpass")

    def test_login_raises_on_unknown_email(self, app):
        with app.app_context():
            with pytest.raises(ValueError, match="Email ou mot de passe incorrect"):
                auth_service.login("nobody@test.com", "password123")

    def test_login_raises_on_inactive_user(self, app):
        with app.app_context():
            user = auth_service.register(email="inact@test.com", password="password123")
            user.is_active = False
            user.save()
            with pytest.raises(ValueError, match="Ce compte est desactive"):
                auth_service.login("inact@test.com", "password123")


class TestVerifyEmail:
    def test_verify_email_marks_user_verified(self, app):
        with app.app_context():
            user = auth_service.register(email="verif@test.com", password="password123")
            from app.services.email_service import generate_verification_token
            token = generate_verification_token(user.email)
            verified = auth_service.verify_email(token)
            assert verified.is_verified is True

    def test_verify_email_raises_on_invalid_token(self, app):
        with app.app_context():
            with pytest.raises(ValueError, match="Token invalide ou expire"):
                auth_service.verify_email("bad-token")


class TestForgotResetPassword:
    def test_forgot_password_sends_email(self, app):
        with app.app_context():
            auth_service.register(email="fp@test.com", password="password123")
            auth_service.forgot_password("fp@test.com")

    def test_forgot_password_silent_on_unknown_email(self, app):
        with app.app_context():
            auth_service.forgot_password("unknown@test.com")

    def test_reset_password_changes_password(self, app):
        with app.app_context():
            user = auth_service.register(email="rp@test.com", password="password123")
            from app.services.email_service import generate_reset_token
            token = generate_reset_token(user.email)
            auth_service.reset_password(token, "newpassword456")
            assert user.check_password("newpassword456") is True

    def test_reset_password_raises_on_invalid_token(self, app):
        with app.app_context():
            with pytest.raises(ValueError, match="Token invalide ou expire"):
                auth_service.reset_password("bad-token", "newpassword456")


class TestMe:
    def test_me_returns_user_data(self, app):
        with app.app_context():
            user = auth_service.register(email="me@test.com", password="password123")
            data = auth_service.me(user.id)
            assert data["email"] == "me@test.com"
            assert data["first_name"] is None

    def test_me_raises_on_unknown_user(self, app):
        with app.app_context():
            with pytest.raises(ValueError, match="Utilisateur introuvable"):
                auth_service.me(9999)


class TestRefresh:
    def test_refresh_returns_new_token(self, app):
        with app.app_context():
            user = auth_service.register(email="ref@test.com", password="password123")
            result = auth_service.refresh(str(user.id))
            assert "access_token" in result

    def test_refresh_raises_on_inactive_user(self, app):
        with app.app_context():
            user = auth_service.register(email="refin@test.com", password="password123")
            user.is_active = False
            user.save()
            with pytest.raises(ValueError, match="Utilisateur introuvable ou desactive"):
                auth_service.refresh(str(user.id))
