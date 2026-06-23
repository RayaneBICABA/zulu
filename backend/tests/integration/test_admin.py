import pytest


@pytest.fixture
def admin_token(client):
    client.post("/api/auth/register", json={
        "email": "admin@test.com",
        "password": "password123",
    })
    login = client.post("/api/auth/login", json={
        "email": "admin@test.com",
        "password": "password123",
    })
    token = login.get_json()["access_token"]

    from app.services import role_service
    from app import create_app
    from app.extensions import db as _db
    with client.application.app_context():
        role_service.create_role("admin")
        from app.models.user import User
        user = User.query.filter_by(email="admin@test.com").first()
        role_service.assign_role(user.id, "admin")

    return token


@pytest.fixture
def user_token(client):
    client.post("/api/auth/register", json={
        "email": "user@test.com",
        "password": "password123",
    })
    login = client.post("/api/auth/login", json={
        "email": "user@test.com",
        "password": "password123",
    })
    return login.get_json()["access_token"]


class TestRoles:
    def test_list_roles_returns_200_for_admin(self, client, admin_token):
        response = client.get("/api/admin/roles", headers={
            "Authorization": f"Bearer {admin_token}",
        })
        assert response.status_code == 200
        assert isinstance(response.get_json(), list)

    def test_list_roles_returns_403_for_non_admin(self, client, user_token):
        response = client.get("/api/admin/roles", headers={
            "Authorization": f"Bearer {user_token}",
        })
        assert response.status_code == 403

    def test_list_roles_returns_401_without_token(self, client):
        response = client.get("/api/admin/roles")
        assert response.status_code == 401

    def test_create_role_returns_201(self, client, admin_token):
        response = client.post("/api/admin/roles", json={
            "name": "moderator",
            "description": "Moderator role",
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 201
        assert response.get_json()["name"] == "moderator"

    def test_create_role_returns_400_on_missing_name(self, client, admin_token):
        response = client.post("/api/admin/roles", json={},
                               headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 400

    def test_create_role_returns_409_on_duplicate(self, client, admin_token):
        client.post("/api/admin/roles", json={"name": "editor"},
                    headers={"Authorization": f"Bearer {admin_token}"})
        response = client.post("/api/admin/roles", json={"name": "editor"},
                               headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 409


class TestPermissions:
    def test_list_permissions_returns_200(self, client, admin_token):
        response = client.get("/api/admin/permissions", headers={
            "Authorization": f"Bearer {admin_token}",
        })
        assert response.status_code == 200

    def test_create_permission_returns_201(self, client, admin_token):
        response = client.post("/api/admin/permissions", json={
            "codename": "users:read",
            "name": "Lire les utilisateurs",
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 201

    def test_create_permission_returns_409_on_duplicate(self, client, admin_token):
        client.post("/api/admin/permissions", json={"codename": "dup"},
                    headers={"Authorization": f"Bearer {admin_token}"})
        response = client.post("/api/admin/permissions", json={"codename": "dup"},
                               headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 409


class TestUserRoleAssignment:
    def test_assign_role_to_user_returns_200(self, client, admin_token, user_token):
        login = client.post("/api/auth/login", json={
            "email": "user@test.com",
            "password": "password123",
        })
        user_id = login.get_json()["user"]["id"]

        client.post("/api/admin/roles", json={"name": "user"},
                    headers={"Authorization": f"Bearer {admin_token}"})

        response = client.post(f"/api/admin/users/{user_id}/roles", json={
            "role_name": "user",
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        assert "Role assigne" in response.get_json()["message"]

    def test_remove_role_returns_200(self, client, admin_token, user_token):
        login = client.post("/api/auth/login", json={
            "email": "user@test.com",
            "password": "password123",
        })
        user_id = login.get_json()["user"]["id"]

        client.post("/api/admin/roles", json={"name": "user"},
                    headers={"Authorization": f"Bearer {admin_token}"})
        client.post(f"/api/admin/users/{user_id}/roles", json={"role_name": "user"},
                    headers={"Authorization": f"Bearer {admin_token}"})

        response = client.delete(f"/api/admin/users/{user_id}/roles", json={
            "role_name": "user",
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        assert "Role retire" in response.get_json()["message"]

    def test_get_user_roles_returns_200(self, client, admin_token, user_token):
        login = client.post("/api/auth/login", json={
            "email": "user@test.com",
            "password": "password123",
        })
        user_id = login.get_json()["user"]["id"]

        response = client.get(f"/api/admin/users/{user_id}/roles", headers={
            "Authorization": f"Bearer {admin_token}",
        })
        assert response.status_code == 200

    def test_get_user_roles_returns_404_on_unknown_user(self, client, admin_token):
        response = client.get("/api/admin/users/9999/roles", headers={
            "Authorization": f"Bearer {admin_token}",
        })
        assert response.status_code == 404


class TestPermissionAssignment:
    def test_assign_permission_to_role_returns_200(self, client, admin_token):
        client.post("/api/admin/roles", json={"name": "editor"},
                    headers={"Authorization": f"Bearer {admin_token}"})
        client.post("/api/admin/permissions", json={"codename": "posts:edit"},
                    headers={"Authorization": f"Bearer {admin_token}"})

        response = client.post("/api/admin/roles/editor/permissions", json={
            "permission_codename": "posts:edit",
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        assert "Permission assignee" in response.get_json()["message"]

    def test_assign_permission_returns_400_on_unknown_role(self, client, admin_token):
        response = client.post("/api/admin/roles/ghost/permissions", json={
            "permission_codename": "anything",
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 400
