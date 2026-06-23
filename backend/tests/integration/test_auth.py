import pytest


class TestRegister:
    def test_register_returns_201(self, client):
        response = client.post("/api/auth/register", json={
            "email": "new@test.com",
            "password": "password123",
            "first_name": "John",
            "last_name": "Doe",
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data["message"] == "Inscription reussie."
        assert data["user"]["email"] == "new@test.com"

    def test_register_returns_400_on_missing_fields(self, client):
        response = client.post("/api/auth/register", json={"email": "bad@test.com"})
        assert response.status_code == 400

    def test_register_returns_409_on_duplicate_email(self, client):
        client.post("/api/auth/register", json={
            "email": "dup@test.com",
            "password": "password123",
        })
        response = client.post("/api/auth/register", json={
            "email": "dup@test.com",
            "password": "other456",
        })
        assert response.status_code == 409
        assert "existe deja" in response.get_json()["error"]


class TestLogin:
    def test_login_returns_200(self, client):
        client.post("/api/auth/register", json={
            "email": "log@test.com",
            "password": "password123",
        })
        response = client.post("/api/auth/login", json={
            "email": "log@test.com",
            "password": "password123",
        })
        assert response.status_code == 200
        data = response.get_json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert "user" in data

    def test_login_returns_401_on_wrong_credentials(self, client):
        response = client.post("/api/auth/login", json={
            "email": "bad@test.com",
            "password": "wrong",
        })
        assert response.status_code == 401

    def test_login_returns_400_on_missing_fields(self, client):
        response = client.post("/api/auth/login", json={})
        assert response.status_code == 400


class TestMe:
    def test_me_returns_200_with_valid_token(self, client):
        client.post("/api/auth/register", json={
            "email": "me@test.com",
            "password": "password123",
        })
        login = client.post("/api/auth/login", json={
            "email": "me@test.com",
            "password": "password123",
        })
        token = login.get_json()["access_token"]
        response = client.get("/api/auth/me", headers={
            "Authorization": f"Bearer {token}",
        })
        assert response.status_code == 200
        assert response.get_json()["email"] == "me@test.com"

    def test_me_returns_401_without_token(self, client):
        response = client.get("/api/auth/me")
        assert response.status_code == 401


class TestRefresh:
    def test_refresh_returns_200_with_valid_refresh_token(self, client):
        client.post("/api/auth/register", json={
            "email": "ref@test.com",
            "password": "password123",
        })
        login = client.post("/api/auth/login", json={
            "email": "ref@test.com",
            "password": "password123",
        })
        refresh_token = login.get_json()["refresh_token"]
        response = client.post("/api/auth/refresh",
            headers={"Authorization": f"Bearer {refresh_token}"},
        )
        assert response.status_code == 200
        assert "access_token" in response.get_json()

    def test_refresh_returns_401_without_token(self, client):
        response = client.post("/api/auth/refresh")
        assert response.status_code == 401


class TestVerifyEmail:
    def test_verify_email_returns_200(self, client):
        client.post("/api/auth/register", json={
            "email": "verif@test.com",
            "password": "password123",
        })
        from app.services.email_service import generate_verification_token
        token = generate_verification_token("verif@test.com")
        response = client.post("/api/auth/verify-email", json={"token": token})
        assert response.status_code == 200
        assert response.get_json()["message"] == "Email verifie avec succes."

    def test_verify_email_returns_400_on_invalid_token(self, client):
        response = client.post("/api/auth/verify-email", json={"token": "bad"})
        assert response.status_code == 400

    def test_verify_email_returns_400_without_token(self, client):
        response = client.post("/api/auth/verify-email", json={})
        assert response.status_code == 400


class TestForgotPassword:
    def test_forgot_password_returns_200(self, client):
        client.post("/api/auth/register", json={
            "email": "fp@test.com",
            "password": "password123",
        })
        response = client.post("/api/auth/forgot-password", json={
            "email": "fp@test.com",
        })
        assert response.status_code == 200

    def test_forgot_password_returns_200_even_on_unknown_email(self, client):
        response = client.post("/api/auth/forgot-password", json={
            "email": "unknown@test.com",
        })
        assert response.status_code == 200

    def test_forgot_password_returns_400_without_email(self, client):
        response = client.post("/api/auth/forgot-password", json={})
        assert response.status_code == 400


class TestResetPassword:
    def test_reset_password_returns_200(self, client):
        client.post("/api/auth/register", json={
            "email": "rp@test.com",
            "password": "password123",
        })
        from app.services.email_service import generate_reset_token
        token = generate_reset_token("rp@test.com")
        response = client.post("/api/auth/reset-password", json={
            "token": token,
            "password": "newpass456",
        })
        assert response.status_code == 200

    def test_reset_password_returns_400_on_invalid_token(self, client):
        response = client.post("/api/auth/reset-password", json={
            "token": "bad",
            "password": "newpass456",
        })
        assert response.status_code == 400

    def test_reset_password_returns_400_without_fields(self, client):
        response = client.post("/api/auth/reset-password", json={})
        assert response.status_code == 400
