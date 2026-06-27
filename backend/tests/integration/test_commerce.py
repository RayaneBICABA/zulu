import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO


@pytest.fixture
def user_token(client):
    client.post("/api/auth/register", json={
        "email": "artisan@test.com",
        "password": "password123",
    })
    login = client.post("/api/auth/login", json={
        "email": "artisan@test.com",
        "password": "password123",
    })
    return login.get_json()["access_token"]


@pytest.fixture
def other_user_token(client):
    client.post("/api/auth/register", json={
        "email": "other@test.com",
        "password": "password123",
    })
    login = client.post("/api/auth/login", json={
        "email": "other@test.com",
        "password": "password123",
    })
    return login.get_json()["access_token"]


@pytest.fixture
def admin_token(client):
    client.post("/api/auth/register", json={
        "email": "admin_com@test.com",
        "password": "password123",
    })
    login = client.post("/api/auth/login", json={
        "email": "admin_com@test.com",
        "password": "password123",
    })
    token = login.get_json()["access_token"]

    from app.services import role_service
    from app.models.user import User
    with client.application.app_context():
        user = User.query.filter_by(email="admin_com@test.com").first()
        role_service.assign_role(user.id, "admin")

    return token


@pytest.fixture
def artisan_user_token(client):
    client.post("/api/auth/register", json={
        "email": "artisan_role@test.com",
        "password": "password123",
    })
    login = client.post("/api/auth/login", json={
        "email": "artisan_role@test.com",
        "password": "password123",
    })
    token = login.get_json()["access_token"]

    from app.services import role_service
    from app.models.user import User
    with client.application.app_context():
        user = User.query.filter_by(email="artisan_role@test.com").first()
        role_service.assign_role(user.id, "artisan")

    return token


@pytest.fixture
def categorie_id(client):
    with client.application.app_context():
        from app.models.categorie import Categorie
        cat = Categorie(nom="Boulangerie", is_active=True)
        cat.save()
        return cat.id


@pytest.fixture
def inactive_categorie_id(client):
    with client.application.app_context():
        from app.models.categorie import Categorie
        cat = Categorie(nom="Inactif", is_active=False)
        cat.save()
        return cat.id


class TestListCategories:
    def test_list_categories_returns_200(self, client, categorie_id):
        response = client.get("/api/categories")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) >= 1
        assert data[0]["nom"] == "Boulangerie"

    def test_list_categories_excludes_inactive(self, client, categorie_id, inactive_categorie_id):
        response = client.get("/api/categories")
        data = response.get_json()
        noms = [c["nom"] for c in data]
        assert "Inactif" not in noms


class TestCreateCategory:
    def test_create_category_returns_201(self, client, admin_token):
        response = client.post("/api/categories", json={
            "nom": "Coiffure",
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 201
        data = response.get_json()
        assert data["nom"] == "Coiffure"

    def test_create_category_returns_400_on_missing_nom(self, client, admin_token):
        response = client.post("/api/categories", json={}, headers={
            "Authorization": f"Bearer {admin_token}",
        })
        assert response.status_code == 400

    def test_create_category_returns_409_on_duplicate(self, client, admin_token, categorie_id):
        response = client.post("/api/categories", json={
            "nom": "Boulangerie",
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 409

    def test_create_category_returns_403_for_non_admin(self, client, user_token):
        response = client.post("/api/categories", json={
            "nom": "Hacker",
        }, headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 403

    def test_create_category_returns_401_without_token(self, client):
        response = client.post("/api/categories", json={
            "nom": "Test",
        })
        assert response.status_code == 401


class TestCreateCommerce:
    def test_create_commerce_returns_201(self, client, user_token, categorie_id):
        response = client.post("/api/commerces", json={
            "nom_commercial": "Boulangerie du Coin",
            "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 201
        data = response.get_json()
        assert data["nom_commercial"] == "Boulangerie du Coin"
        assert data["is_active"] is False
        assert data["step"] == 1

    def test_create_commerce_with_optional_fields(self, client, user_token, categorie_id):
        response = client.post("/api/commerces", json={
            "nom_commercial": "Commerce",
            "categorie_id": categorie_id,
            "whatsapp_numero": "+22507070707",
            "description": "Test",
        }, headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 201
        assert response.get_json()["whatsapp_numero"] == "+22507070707"

    def test_create_commerce_returns_400_on_missing_fields(self, client, user_token):
        response = client.post("/api/commerces", json={}, headers={
            "Authorization": f"Bearer {user_token}",
        })
        assert response.status_code == 400

    def test_create_commerce_returns_400_on_unknown_categorie(self, client, user_token):
        response = client.post("/api/commerces", json={
            "nom_commercial": "Test",
            "categorie_id": 9999,
        }, headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 400

    def test_create_commerce_returns_400_on_inactive_categorie(self, client, user_token, inactive_categorie_id):
        response = client.post("/api/commerces", json={
            "nom_commercial": "Test",
            "categorie_id": inactive_categorie_id,
        }, headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 400

    def test_create_commerce_returns_401_without_token(self, client, categorie_id):
        response = client.post("/api/commerces", json={
            "nom_commercial": "Test",
            "categorie_id": categorie_id,
        })
        assert response.status_code == 401


class TestUpdateLocalisation:
    def _create_commerce(self, client, user_token, categorie_id):
        resp = client.post("/api/commerces", json={
            "nom_commercial": "Test",
            "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {user_token}"})
        return resp.get_json()["id"]

    def _horaires(self):
        return [
            {"jour": "lundi", "heure_ouverture": "08:00", "heure_fermeture": "18:00"},
            {"jour": "mardi", "heure_ouverture": "08:00", "heure_fermeture": "18:00"},
            {"jour": "mercredi", "heure_ouverture": "08:00", "heure_fermeture": "18:00"},
            {"jour": "jeudi", "heure_ouverture": "08:00", "heure_fermeture": "18:00"},
            {"jour": "vendredi", "heure_ouverture": "08:00", "heure_fermeture": "18:00"},
            {"jour": "samedi", "heure_ouverture": "08:00", "heure_fermeture": "13:00"},
            {"jour": "dimanche", "est_ferme": True},
        ]

    def test_update_localisation_returns_200(self, client, user_token, categorie_id):
        commerce_id = self._create_commerce(client, user_token, categorie_id)
        response = client.put(f"/api/commerces/{commerce_id}/localisation", json={
            "latitude": 5.36,
            "longitude": -4.0083,
            "adresse_complete": "Abidjan, Cocody",
            "horaires": self._horaires(),
        }, headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 200
        data = response.get_json()
        assert data["step"] == 2
        assert data["latitude"] == 5.36

    def test_update_localisation_returns_400_on_wrong_horaires_count(self, client, user_token, categorie_id):
        commerce_id = self._create_commerce(client, user_token, categorie_id)
        response = client.put(f"/api/commerces/{commerce_id}/localisation", json={
            "latitude": 5.36,
            "longitude": -4.0083,
            "adresse_complete": "Abidjan",
            "horaires": [{"jour": "lundi"}],
        }, headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 400

    def test_update_localisation_returns_400_on_missing_fields(self, client, user_token, categorie_id):
        commerce_id = self._create_commerce(client, user_token, categorie_id)
        response = client.put(f"/api/commerces/{commerce_id}/localisation", json={}, headers={
            "Authorization": f"Bearer {user_token}",
        })
        assert response.status_code == 400

    def test_update_localisation_returns_400_on_invalid_jour(self, client, user_token, categorie_id):
        commerce_id = self._create_commerce(client, user_token, categorie_id)
        response = client.put(f"/api/commerces/{commerce_id}/localisation", json={
            "latitude": 5.36,
            "longitude": -4.0083,
            "adresse_complete": "Abidjan",
            "horaires": [{"jour": "invalid"}] * 7,
        }, headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 400

    def test_update_localisation_returns_400_on_wrong_owner(self, client, user_token, other_user_token, categorie_id):
        commerce_id = self._create_commerce(client, user_token, categorie_id)
        response = client.put(f"/api/commerces/{commerce_id}/localisation", json={
            "latitude": 5.36,
            "longitude": -4.0083,
            "adresse_complete": "Abidjan",
            "horaires": self._horaires(),
        }, headers={"Authorization": f"Bearer {other_user_token}"})
        assert response.status_code == 400

    def test_update_localisation_returns_401_without_token(self, client, user_token, categorie_id):
        commerce_id = self._create_commerce(client, user_token, categorie_id)
        response = client.put(f"/api/commerces/{commerce_id}/localisation", json={
            "latitude": 5.36,
            "longitude": -4.0083,
            "adresse_complete": "Abidjan",
            "horaires": self._horaires(),
        })
        assert response.status_code == 401


class TestUploadPhotos:
    def _create_commerce_with_location(self, client, user_token, categorie_id):
        resp = client.post("/api/commerces", json={
            "nom_commercial": "Test",
            "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {user_token}"})
        commerce_id = resp.get_json()["id"]
        client.put(f"/api/commerces/{commerce_id}/localisation", json={
            "latitude": 5.36,
            "longitude": -4.0083,
            "adresse_complete": "Abidjan",
            "horaires": [
                {"jour": "lundi"}, {"jour": "mardi"}, {"jour": "mercredi"},
                {"jour": "jeudi"}, {"jour": "vendredi"}, {"jour": "samedi"},
                {"jour": "dimanche", "est_ferme": True},
            ],
        }, headers={"Authorization": f"Bearer {user_token}"})
        return commerce_id

    def test_upload_photos_returns_201(self, client, user_token, categorie_id):
        commerce_id = self._create_commerce_with_location(client, user_token, categorie_id)
        with patch("app.services.commerce_service.cloudinary.uploader.upload") as mock_upload:
            mock_upload.return_value = {"secure_url": "https://res.cloudinary.com/test/image.jpg"}
            data = BytesIO(b"fake image data")
            response = client.post(f"/api/commerces/{commerce_id}/photos",
                data={"photos": (data, "test.jpg")},
                content_type="multipart/form-data",
                headers={"Authorization": f"Bearer {user_token}"},
            )
            assert response.status_code == 201
            body = response.get_json()
            assert len(body["photos"]) == 1
            assert "auto_published" in body

    def test_upload_photos_returns_400_without_files(self, client, user_token, categorie_id):
        commerce_id = self._create_commerce_with_location(client, user_token, categorie_id)
        response = client.post(f"/api/commerces/{commerce_id}/photos",
            data={},
            content_type="multipart/form-data",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 400

    def test_upload_photos_returns_401_without_token(self, client, user_token, categorie_id):
        commerce_id = self._create_commerce_with_location(client, user_token, categorie_id)
        data = BytesIO(b"fake image data")
        response = client.post(f"/api/commerces/{commerce_id}/photos",
            data={"photos": (data, "test.jpg")},
            content_type="multipart/form-data",
        )
        assert response.status_code == 401


class TestDeletePhoto:
    def test_delete_photo_returns_200(self, client, user_token, categorie_id):
        resp = client.post("/api/commerces", json={
            "nom_commercial": "Test",
            "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {user_token}"})
        commerce_id = resp.get_json()["id"]

        with client.application.app_context():
            from app.models.commerce import CommercePhoto
            photo = CommercePhoto(commerce_id=commerce_id, url="http://test.jpg", ordre=1)
            photo.save()
            photo_id = photo.id

        response = client.delete(f"/api/commerces/{commerce_id}/photos/{photo_id}", headers={
            "Authorization": f"Bearer {user_token}",
        })
        assert response.status_code == 200
        assert "supprimee" in response.get_json()["message"]

    def test_delete_photo_returns_400_on_wrong_owner(self, client, user_token, other_user_token, categorie_id):
        resp = client.post("/api/commerces", json={
            "nom_commercial": "Test",
            "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {user_token}"})
        commerce_id = resp.get_json()["id"]

        with client.application.app_context():
            from app.models.commerce import CommercePhoto
            photo = CommercePhoto(commerce_id=commerce_id, url="http://test.jpg", ordre=1)
            photo.save()
            photo_id = photo.id

        response = client.delete(f"/api/commerces/{commerce_id}/photos/{photo_id}", headers={
            "Authorization": f"Bearer {other_user_token}",
        })
        assert response.status_code == 400


class TestPublish:
    def test_publish_returns_200_when_complete(self, client, user_token, categorie_id):
        resp = client.post("/api/commerces", json={
            "nom_commercial": "Test",
            "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {user_token}"})
        commerce_id = resp.get_json()["id"]

        client.put(f"/api/commerces/{commerce_id}/localisation", json={
            "latitude": 5.36,
            "longitude": -4.0083,
            "adresse_complete": "Abidjan",
            "horaires": [
                {"jour": "lundi"}, {"jour": "mardi"}, {"jour": "mercredi"},
                {"jour": "jeudi"}, {"jour": "vendredi"}, {"jour": "samedi"},
                {"jour": "dimanche", "est_ferme": True},
            ],
        }, headers={"Authorization": f"Bearer {user_token}"})

        with client.application.app_context():
            from app.models.commerce import CommercePhoto
            photo = CommercePhoto(commerce_id=commerce_id, url="http://test.jpg", ordre=1)
            photo.save()

        response = client.patch(f"/api/commerces/{commerce_id}/publish", headers={
            "Authorization": f"Bearer {user_token}",
        })
        assert response.status_code == 200
        assert response.get_json()["is_active"] is True

    def test_publish_returns_400_on_missing_location(self, client, user_token, categorie_id):
        resp = client.post("/api/commerces", json={
            "nom_commercial": "Test",
            "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {user_token}"})
        commerce_id = resp.get_json()["id"]

        response = client.patch(f"/api/commerces/{commerce_id}/publish", headers={
            "Authorization": f"Bearer {user_token}",
        })
        assert response.status_code == 400
        assert "Etape 2" in response.get_json()["error"]

    def test_publish_returns_400_on_missing_photos(self, client, user_token, categorie_id):
        resp = client.post("/api/commerces", json={
            "nom_commercial": "Test",
            "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {user_token}"})
        commerce_id = resp.get_json()["id"]

        client.put(f"/api/commerces/{commerce_id}/localisation", json={
            "latitude": 5.36,
            "longitude": -4.0083,
            "adresse_complete": "Abidjan",
            "horaires": [
                {"jour": "lundi"}, {"jour": "mardi"}, {"jour": "mercredi"},
                {"jour": "jeudi"}, {"jour": "vendredi"}, {"jour": "samedi"},
                {"jour": "dimanche", "est_ferme": True},
            ],
        }, headers={"Authorization": f"Bearer {user_token}"})

        response = client.patch(f"/api/commerces/{commerce_id}/publish", headers={
            "Authorization": f"Bearer {user_token}",
        })
        assert response.status_code == 400
        assert "Etape 3" in response.get_json()["error"]


class TestGetCommerce:
    def test_get_commerce_returns_200(self, client, user_token, categorie_id):
        resp = client.post("/api/commerces", json={
            "nom_commercial": "Test",
            "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {user_token}"})
        commerce_id = resp.get_json()["id"]

        response = client.get(f"/api/commerces/{commerce_id}", headers={
            "Authorization": f"Bearer {user_token}",
        })
        assert response.status_code == 200
        assert response.get_json()["step"] == 1

    def test_get_commerce_returns_400_on_wrong_owner(self, client, user_token, other_user_token, categorie_id):
        resp = client.post("/api/commerces", json={
            "nom_commercial": "Test",
            "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {user_token}"})
        commerce_id = resp.get_json()["id"]

        response = client.get(f"/api/commerces/{commerce_id}", headers={
            "Authorization": f"Bearer {other_user_token}",
        })
        assert response.status_code == 400


class TestArtisanHome:
    def test_artisan_home_returns_200(self, client, artisan_user_token, categorie_id):
        client.post("/api/commerces", json={
            "nom_commercial": "Mon Salon",
            "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {artisan_user_token}"})
        response = client.get("/api/artisan/home", headers={
            "Authorization": f"Bearer {artisan_user_token}",
        })
        assert response.status_code == 200
        data = response.get_json()
        assert "Bienvenue" in data["message"]
        assert data["commerce"]["nom_commercial"] == "Mon Salon"
        assert "stats" in data["commerce"]
        assert "photos" in data["commerce"]
        assert "horaires" in data["commerce"]
        assert "produit_images" in data["commerce"]

    def test_artisan_home_returns_404_without_commerce(self, client, artisan_user_token):
        response = client.get("/api/artisan/home", headers={
            "Authorization": f"Bearer {artisan_user_token}",
        })
        assert response.status_code == 404
        assert "Aucun commerce" in response.get_json()["error"]

    def test_artisan_home_returns_403_for_client(self, client, user_token):
        response = client.get("/api/artisan/home", headers={
            "Authorization": f"Bearer {user_token}",
        })
        assert response.status_code == 403


class TestRecordVue:
    def test_record_vue_returns_201(self, client, user_token, categorie_id):
        resp = client.post("/api/commerces", json={
            "nom_commercial": "Vue Test",
            "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {user_token}"})
        commerce_id = resp.get_json()["id"]

        response = client.post(f"/api/commerces/{commerce_id}/vues")
        assert response.status_code == 201
        data = response.get_json()
        assert data["counted"] is True

    def test_record_vue_anti_spam(self, client, user_token, categorie_id):
        resp = client.post("/api/commerces", json={
            "nom_commercial": "Spam Test",
            "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {user_token}"})
        commerce_id = resp.get_json()["id"]

        client.post(f"/api/commerces/{commerce_id}/vues")
        response = client.post(f"/api/commerces/{commerce_id}/vues")
        assert response.status_code == 201
        assert response.get_json()["counted"] is False

    def test_record_vue_returns_400_on_unknown(self, client):
        response = client.post("/api/commerces/9999/vues")
        assert response.status_code == 400


class TestFavoris:
    def test_add_favori_returns_201(self, client, user_token, categorie_id):
        resp = client.post("/api/commerces", json={
            "nom_commercial": "Fav Test",
            "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {user_token}"})
        commerce_id = resp.get_json()["id"]

        response = client.post(f"/api/commerces/{commerce_id}/favoris", headers={
            "Authorization": f"Bearer {user_token}",
        })
        assert response.status_code == 201
        assert "favori" in response.get_json()

    def test_add_favori_returns_400_on_duplicate(self, client, user_token, categorie_id):
        resp = client.post("/api/commerces", json={
            "nom_commercial": "Dup Fav",
            "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {user_token}"})
        commerce_id = resp.get_json()["id"]

        client.post(f"/api/commerces/{commerce_id}/favoris", headers={
            "Authorization": f"Bearer {user_token}",
        })
        response = client.post(f"/api/commerces/{commerce_id}/favoris", headers={
            "Authorization": f"Bearer {user_token}",
        })
        assert response.status_code == 400
        assert "deja" in response.get_json()["error"]

    def test_remove_favori_returns_200(self, client, user_token, categorie_id):
        resp = client.post("/api/commerces", json={
            "nom_commercial": "Rm Fav",
            "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {user_token}"})
        commerce_id = resp.get_json()["id"]

        client.post(f"/api/commerces/{commerce_id}/favoris", headers={
            "Authorization": f"Bearer {user_token}",
        })
        response = client.delete(f"/api/commerces/{commerce_id}/favoris", headers={
            "Authorization": f"Bearer {user_token}",
        })
        assert response.status_code == 200
        assert "Retire" in response.get_json()["message"]

    def test_list_favoris_returns_200(self, client, user_token, categorie_id):
        resp = client.post("/api/commerces", json={
            "nom_commercial": "List Fav",
            "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {user_token}"})
        commerce_id = resp.get_json()["id"]

        client.post(f"/api/commerces/{commerce_id}/favoris", headers={
            "Authorization": f"Bearer {user_token}",
        })
        response = client.get("/api/favoris", headers={
            "Authorization": f"Bearer {user_token}",
        })
        assert response.status_code == 200
        assert len(response.get_json()) >= 1


class TestProduitImages:
    def _create_vendeur_commerce(self, client, user_token, categorie_id):
        resp = client.post("/api/commerces", json={
            "nom_commercial": "Vendeur",
            "categorie_id": categorie_id,
            "is_vendeur_produits": True,
        }, headers={"Authorization": f"Bearer {user_token}"})
        return resp.get_json()["id"]

    def test_upload_produit_image_returns_201(self, client, user_token, categorie_id):
        commerce_id = self._create_vendeur_commerce(client, user_token, categorie_id)
        with patch("app.services.commerce_service.cloudinary.uploader.upload") as mock_upload:
            mock_upload.return_value = {"secure_url": "https://res.cloudinary.com/test/prod.jpg"}
            data = BytesIO(b"fake image data")
            response = client.post(f"/api/commerces/{commerce_id}/produit-images",
                data={"image": (data, "prod.jpg")},
                content_type="multipart/form-data",
                headers={"Authorization": f"Bearer {user_token}"},
            )
            assert response.status_code == 201
            assert response.get_json()["ordre"] == 1

    def test_upload_produit_image_returns_403_for_non_vendeur(self, client, user_token, categorie_id):
        resp = client.post("/api/commerces", json={
            "nom_commercial": "Non Vendeur",
            "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {user_token}"})
        commerce_id = resp.get_json()["id"]

        with patch("app.services.commerce_service.cloudinary.uploader.upload") as mock_upload:
            mock_upload.return_value = {"secure_url": "https://test.jpg"}
            data = BytesIO(b"fake image")
            response = client.post(f"/api/commerces/{commerce_id}/produit-images",
                data={"image": (data, "prod.jpg")},
                content_type="multipart/form-data",
                headers={"Authorization": f"Bearer {user_token}"},
            )
            assert response.status_code == 403

    def test_delete_produit_image_returns_200(self, client, user_token, categorie_id):
        commerce_id = self._create_vendeur_commerce(client, user_token, categorie_id)
        with client.application.app_context():
            from app.models.commerce import ProduitImage
            img = ProduitImage(commerce_id=commerce_id, url="http://test.jpg", ordre=1)
            img.save()
            img_id = img.id

        response = client.delete(f"/api/commerces/{commerce_id}/produit-images/{img_id}", headers={
            "Authorization": f"Bearer {user_token}",
        })
        assert response.status_code == 200
        assert "supprimee" in response.get_json()["message"]


class TestGeolocalisation:
    def test_geolocalisation_returns_200(self, client, user_token, categorie_id):
        resp = client.post("/api/commerces", json={
            "nom_commercial": "Geo Test",
            "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {user_token}"})
        commerce_id = resp.get_json()["id"]

        client.put(f"/api/commerces/{commerce_id}/localisation", json={
            "latitude": 5.36,
            "longitude": -4.0083,
            "adresse_complete": "Abidjan",
            "horaires": [
                {"jour": "lundi"}, {"jour": "mardi"}, {"jour": "mercredi"},
                {"jour": "jeudi"}, {"jour": "vendredi"}, {"jour": "samedi"},
                {"jour": "dimanche", "est_ferme": True},
            ],
        }, headers={"Authorization": f"Bearer {user_token}"})

        response = client.get(f"/api/commerces/{commerce_id}/geolocalisation", headers={
            "Authorization": f"Bearer {user_token}",
        })
        assert response.status_code == 200
        url = response.get_json()["geolocalisation_url"]
        assert "wa.me" in url
        assert "maps.google.com" in url

    def test_geolocalisation_returns_none_without_coords(self, client, user_token, categorie_id):
        resp = client.post("/api/commerces", json={
            "nom_commercial": "No Geo",
            "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {user_token}"})
        commerce_id = resp.get_json()["id"]

        response = client.get(f"/api/commerces/{commerce_id}/geolocalisation", headers={
            "Authorization": f"Bearer {user_token}",
        })
        assert response.status_code == 200
        assert response.get_json()["geolocalisation_url"] is None


class TestArtisanProfile:
    def test_profile_returns_200(self, client, artisan_user_token, categorie_id):
        client.post("/api/commerces", json={
            "nom_commercial": "Mon Atelier",
            "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {artisan_user_token}"})

        response = client.get("/api/artisan/profile", headers={
            "Authorization": f"Bearer {artisan_user_token}",
        })
        assert response.status_code == 200
        data = response.get_json()
        assert "user" in data
        assert "commerces" in data
        assert "nb_commerces_actifs" in data
        assert data["user"]["email"] == "artisan_role@test.com"
        assert data["nb_commerces_actifs"] == 0
        assert len(data["commerces"]) == 1
        assert data["commerces"][0]["nom_commercial"] == "Mon Atelier"

    def test_profile_returns_200_without_commerce(self, client, artisan_user_token):
        response = client.get("/api/artisan/profile", headers={
            "Authorization": f"Bearer {artisan_user_token}",
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data["nb_commerces_actifs"] == 0
        assert data["commerces"] == []
        assert data["user"]["email"] == "artisan_role@test.com"

    def test_profile_returns_401_without_token(self, client):
        response = client.get("/api/artisan/profile")
        assert response.status_code == 401

    def test_profile_returns_403_for_client(self, client, user_token):
        response = client.get("/api/artisan/profile", headers={
            "Authorization": f"Bearer {user_token}",
        })
        assert response.status_code == 403

    def test_profile_includes_whatsapp_and_telephone(self, client, artisan_user_token, categorie_id):
        client.post("/api/commerces", json={
            "nom_commercial": "Contact Test",
            "categorie_id": categorie_id,
            "whatsapp_numero": "+22607070707",
            "contact_telephonique": "+22601010101",
        }, headers={"Authorization": f"Bearer {artisan_user_token}"})

        response = client.get("/api/artisan/profile", headers={
            "Authorization": f"Bearer {artisan_user_token}",
        })
        data = response.get_json()
        assert data["commerces"][0]["whatsapp_numero"] == "+22607070707"
        assert data["commerces"][0]["contact_telephonique"] == "+22601010101"

    def test_profile_returns_multiple_commerces(self, client, artisan_user_token, categorie_id):
        client.post("/api/commerces", json={
            "nom_commercial": "Commerce A",
            "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {artisan_user_token}"})
        client.post("/api/commerces", json={
            "nom_commercial": "Commerce B",
            "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {artisan_user_token}"})

        response = client.get("/api/artisan/profile", headers={
            "Authorization": f"Bearer {artisan_user_token}",
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data["nb_commerces_actifs"] == 0
        assert len(data["commerces"]) == 2


class TestCommentaires:
    @pytest.fixture
    def artisan_token(self, client):
        client.post("/api/auth/register", json={
            "email": "artisan_comm@test.com",
            "password": "password123",
        })
        login = client.post("/api/auth/login", json={
            "email": "artisan_comm@test.com",
            "password": "password123",
        })
        return login.get_json()["access_token"]

    @pytest.fixture
    def client_token(self, client):
        client.post("/api/auth/register", json={
            "email": "client_comm@test.com",
            "password": "password123",
        })
        login = client.post("/api/auth/login", json={
            "email": "client_comm@test.com",
            "password": "password123",
        })
        return login.get_json()["access_token"]

    @pytest.fixture
    def other_token(self, client):
        client.post("/api/auth/register", json={
            "email": "other_comm@test.com",
            "password": "password123",
        })
        login = client.post("/api/auth/login", json={
            "email": "other_comm@test.com",
            "password": "password123",
        })
        return login.get_json()["access_token"]

    @pytest.fixture
    def active_commerce_id(self, client, artisan_token, categorie_id):
        resp = client.post("/api/commerces", json={
            "nom_commercial": "Commerce Avis",
            "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {artisan_token}"})
        commerce_id = resp.get_json()["id"]
        client.put(f"/api/commerces/{commerce_id}/localisation", json={
            "latitude": 12.37, "longitude": -1.52,
            "adresse_complete": "Ouaga",
            "horaires": [
                {"jour": "lundi", "heure_ouverture": "08:00", "heure_fermeture": "18:00"},
                {"jour": "mardi", "heure_ouverture": "08:00", "heure_fermeture": "18:00"},
                {"jour": "mercredi", "heure_ouverture": "08:00", "heure_fermeture": "18:00"},
                {"jour": "jeudi", "heure_ouverture": "08:00", "heure_fermeture": "18:00"},
                {"jour": "vendredi", "heure_ouverture": "08:00", "heure_fermeture": "18:00"},
                {"jour": "samedi", "heure_ouverture": "08:00", "heure_fermeture": "13:00"},
                {"jour": "dimanche", "est_ferme": True},
            ],
        }, headers={"Authorization": f"Bearer {artisan_token}"})
        from app import db
        from app.models.commerce import Commerce
        commerce = db.session.get(Commerce, commerce_id)
        commerce.is_active = True
        db.session.commit()
        return commerce_id

    def test_create_commentaire_returns_201(self, client, client_token, active_commerce_id):
        response = client.post(f"/api/commerces/{active_commerce_id}/commentaires", json={
            "contenu": "Excellent travail, je recommande !",
        }, headers={"Authorization": f"Bearer {client_token}"})
        assert response.status_code == 201
        data = response.get_json()
        assert data["contenu"] == "Excellent travail, je recommande !"
        assert "id" in data

    def test_list_commentaires_returns_200(self, client, client_token, active_commerce_id):
        client.post(f"/api/commerces/{active_commerce_id}/commentaires", json={
            "contenu": "Bon service",
        }, headers={"Authorization": f"Bearer {client_token}"})

        response = client.get(f"/api/commerces/{active_commerce_id}/commentaires")
        assert response.status_code == 200
        data = response.get_json()
        assert data["nb_commentaires"] == 1
        assert data["commentaires"][0]["contenu"] == "Bon service"
        assert "auteur" in data["commentaires"][0]

    def test_create_commentaire_returns_401_without_token(self, client, active_commerce_id):
        response = client.post(f"/api/commerces/{active_commerce_id}/commentaires", json={
            "contenu": "No auth",
        })
        assert response.status_code == 401

    def test_create_commentaire_returns_403_for_owner(self, client, artisan_token, active_commerce_id):
        response = client.post(f"/api/commerces/{active_commerce_id}/commentaires", json={
            "contenu": "Self comment",
        }, headers={"Authorization": f"Bearer {artisan_token}"})
        assert response.status_code == 403

    def test_delete_commentaire_returns_200(self, client, client_token, active_commerce_id):
        resp = client.post(f"/api/commerces/{active_commerce_id}/commentaires", json={
            "contenu": "A supprimer",
        }, headers={"Authorization": f"Bearer {client_token}"})
        comment_id = resp.get_json()["id"]

        response = client.delete(
            f"/api/commerces/{active_commerce_id}/commentaires/{comment_id}",
            headers={"Authorization": f"Bearer {client_token}"},
        )
        assert response.status_code == 200
        assert response.get_json()["message"] == "Commentaire supprime."

    def test_create_commentaire_returns_400_on_inactive_commerce(self, client, client_token, artisan_token, categorie_id):
        resp = client.post("/api/commerces", json={
            "nom_commercial": "Draft Commerce",
            "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {artisan_token}"})
        draft_id = resp.get_json()["id"]

        response = client.post(f"/api/commerces/{draft_id}/commentaires", json={
            "contenu": "Comment on draft",
        }, headers={"Authorization": f"Bearer {client_token}"})
        assert response.status_code == 400
        assert "publie" in response.get_json()["error"]

    def test_create_commentaire_returns_400_on_empty_contenu(self, client, client_token, active_commerce_id):
        response = client.post(f"/api/commerces/{active_commerce_id}/commentaires", json={
            "contenu": "",
        }, headers={"Authorization": f"Bearer {client_token}"})
        assert response.status_code == 400

    def test_create_commentaire_returns_400_on_long_contenu(self, client, client_token, active_commerce_id):
        response = client.post(f"/api/commerces/{active_commerce_id}/commentaires", json={
            "contenu": "x" * 2001,
        }, headers={"Authorization": f"Bearer {client_token}"})
        assert response.status_code == 400

    def test_list_commentaires_returns_404_on_unknown_commerce(self, client):
        response = client.get("/api/commerces/9999/commentaires")
        assert response.status_code == 404

    def test_delete_commentaire_returns_403_for_wrong_owner(self, client, client_token, other_token, active_commerce_id):
        resp = client.post(f"/api/commerces/{active_commerce_id}/commentaires", json={
            "contenu": "Not yours",
        }, headers={"Authorization": f"Bearer {client_token}"})
        comment_id = resp.get_json()["id"]

        response = client.delete(
            f"/api/commerces/{active_commerce_id}/commentaires/{comment_id}",
            headers={"Authorization": f"Bearer {other_token}"},
        )
        assert response.status_code == 403

    def test_delete_commentaire_returns_404_on_unknown_comment(self, client, client_token, active_commerce_id):
        response = client.delete(
            f"/api/commerces/{active_commerce_id}/commentaires/9999",
            headers={"Authorization": f"Bearer {client_token}"},
        )
        assert response.status_code == 404


class TestCommerceRating:
    @pytest.fixture
    def artisan_token(self, client):
        client.post("/api/auth/register", json={
            "email": "artisan_rating@test.com",
            "password": "password123",
        })
        login = client.post("/api/auth/login", json={
            "email": "artisan_rating@test.com",
            "password": "password123",
        })
        return login.get_json()["access_token"]

    @pytest.fixture
    def client_token(self, client):
        client.post("/api/auth/register", json={
            "email": "client_rating@test.com",
            "password": "password123",
        })
        login = client.post("/api/auth/login", json={
            "email": "client_rating@test.com",
            "password": "password123",
        })
        return login.get_json()["access_token"]

    @pytest.fixture
    def active_commerce_id(self, client, artisan_token, categorie_id):
        resp = client.post("/api/commerces", json={
            "nom_commercial": "Commerce Rating",
            "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {artisan_token}"})
        commerce_id = resp.get_json()["id"]
        from app import db
        from app.models.commerce import Commerce
        commerce = db.session.get(Commerce, commerce_id)
        commerce.is_active = True
        db.session.commit()
        return commerce_id

    def test_get_rating_returns_200(self, client, active_commerce_id):
        response = client.get(f"/api/commerces/{active_commerce_id}/rating")
        assert response.status_code == 200
        data = response.get_json()
        assert "average_rating" in data
        assert "rating_count" in data
        assert "etoiles" in data
        assert data["etoiles"]["pleines"] + data["etoiles"]["demies"] + data["etoiles"]["vides"] == 5

    def test_get_rating_returns_404_on_unknown_commerce(self, client):
        response = client.get("/api/commerces/9999/rating")
        assert response.status_code == 404

    def test_rating_updates_after_comment(self, client, client_token, active_commerce_id):
        with patch("app.services.ai_service.analyze_commentaires") as mock_analyze:
            mock_analyze.return_value = (4.50, "Excellent service.")
            client.post(f"/api/commerces/{active_commerce_id}/commentaires", json={
                "contenu": "Excellent !",
            }, headers={"Authorization": f"Bearer {client_token}"})

        response = client.get(f"/api/commerces/{active_commerce_id}/rating")
        data = response.get_json()
        assert data["average_rating"] == 4.5
        assert data["rating_count"] == 1
        assert data["etoiles"]["pleines"] == 4
        assert data["etoiles"]["demies"] == 1
        assert data["etoiles"]["vides"] == 0

    def test_etoiles_computation(self, client, client_token, active_commerce_id):
        with patch("app.services.ai_service.analyze_commentaires") as mock_analyze:
            mock_analyze.return_value = (2.75, "Mixed.")
            client.post(f"/api/commerces/{active_commerce_id}/commentaires", json={
                "contenu": "Moyen",
            }, headers={"Authorization": f"Bearer {client_token}"})

        response = client.get(f"/api/commerces/{active_commerce_id}/rating")
        data = response.get_json()
        assert data["etoiles"]["pleines"] == 3
        assert data["etoiles"]["demies"] == 0
        assert data["etoiles"]["vides"] == 2

    def test_rating_on_commerce_with_zero_comments(self, client, active_commerce_id):
        response = client.get(f"/api/commerces/{active_commerce_id}/rating")
        assert response.status_code == 200
        data = response.get_json()
        assert data["average_rating"] == 0.0
        assert data["rating_count"] == 0
        assert data["etoiles"] == {"pleines": 0, "demies": 0, "vides": 5}

    def test_rating_updates_after_comment_deletion(self, client, client_token, active_commerce_id):
        with patch("app.services.ai_service.analyze_commentaires") as mock_analyze:
            mock_analyze.return_value = (5.00, "Parfait.")
            resp = client.post(f"/api/commerces/{active_commerce_id}/commentaires", json={
                "contenu": "Parfait !",
            }, headers={"Authorization": f"Bearer {client_token}"})
            comment_id = resp.get_json()["id"]

        response = client.get(f"/api/commerces/{active_commerce_id}/rating")
        assert response.get_json()["rating_count"] == 1

        with patch("app.services.ai_service.analyze_commentaires") as mock_analyze:
            mock_analyze.return_value = (0.0, "Aucun commentaire.")
            client.delete(
                f"/api/commerces/{active_commerce_id}/commentaires/{comment_id}",
                headers={"Authorization": f"Bearer {client_token}"},
            )

        response = client.get(f"/api/commerces/{active_commerce_id}/rating")
        data = response.get_json()
        assert data["average_rating"] == 0.0
        assert data["rating_count"] == 0

    def test_comment_saved_even_when_ai_fails(self, client, client_token, active_commerce_id):
        with patch("app.services.ai_service.analyze_and_update_rating", side_effect=Exception("AI down")):
            response = client.post(f"/api/commerces/{active_commerce_id}/commentaires", json={
                "contenu": "Still saved",
            }, headers={"Authorization": f"Bearer {client_token}"})
        assert response.status_code == 201
        assert response.get_json()["contenu"] == "Still saved"


class TestSwitchCommerce:
    def test_switch_commerce_returns_200(self, client, artisan_user_token, categorie_id):
        r1 = client.post("/api/commerces", json={
            "nom_commercial": "Shop A", "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {artisan_user_token}"})
        c1_id = r1.get_json()["id"]
        r2 = client.post("/api/commerces", json={
            "nom_commercial": "Shop B", "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {artisan_user_token}"})
        c2_id = r2.get_json()["id"]

        response = client.patch("/api/artisan/active-commerce", json={
            "commerce_id": c2_id,
        }, headers={"Authorization": f"Bearer {artisan_user_token}"})
        assert response.status_code == 200
        assert response.get_json()["active_commerce_id"] == c2_id

        home = client.get("/api/artisan/home", headers={
            "Authorization": f"Bearer {artisan_user_token}",
        })
        assert home.get_json()["commerce"]["id"] == c2_id

    def test_switch_commerce_returns_403_for_wrong_owner(self, client, artisan_user_token, other_user_token, categorie_id):
        r1 = client.post("/api/commerces", json={
            "nom_commercial": "Not Mine", "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {artisan_user_token}"})
        c_id = r1.get_json()["id"]

        client.post("/api/auth/register", json={
            "email": "switch_other@test.com", "password": "password123",
        })
        login = client.post("/api/auth/login", json={
            "email": "switch_other@test.com", "password": "password123",
        })
        other_token = login.get_json()["access_token"]
        from app.services import role_service
        from app.models.user import User
        with client.application.app_context():
            u = User.query.filter_by(email="switch_other@test.com").first()
            role_service.assign_role(u.id, "artisan")

        response = client.patch("/api/artisan/active-commerce", json={
            "commerce_id": c_id,
        }, headers={"Authorization": f"Bearer {other_token}"})
        assert response.status_code == 403

    def test_switch_commerce_returns_400_on_missing_commerce_id(self, client, artisan_user_token):
        response = client.patch("/api/artisan/active-commerce", json={}, headers={
            "Authorization": f"Bearer {artisan_user_token}",
        })
        assert response.status_code == 400

    def test_switch_commerce_returns_401_without_token(self, client):
        response = client.patch("/api/artisan/active-commerce", json={"commerce_id": 1})
        assert response.status_code == 401

    def test_switch_commerce_returns_403_for_client(self, client, user_token):
        response = client.patch("/api/artisan/active-commerce", json={"commerce_id": 1}, headers={
            "Authorization": f"Bearer {user_token}",
        })
        assert response.status_code == 403

    def test_switch_commerce_returns_404_on_unknown_commerce(self, client, artisan_user_token):
        response = client.patch("/api/artisan/active-commerce", json={"commerce_id": 9999}, headers={
            "Authorization": f"Bearer {artisan_user_token}",
        })
        assert response.status_code == 404


class TestGetCommercesCards:
    def test_cards_returns_200(self, client, artisan_user_token, categorie_id):
        client.post("/api/commerces", json={
            "nom_commercial": "Card A", "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {artisan_user_token}"})
        client.post("/api/commerces", json={
            "nom_commercial": "Card B", "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {artisan_user_token}"})

        response = client.get("/api/artisan/commerces/cards", headers={
            "Authorization": f"Bearer {artisan_user_token}",
        })
        assert response.status_code == 200
        cards = response.get_json()["cards"]
        assert len(cards) == 1

    def test_cards_excludes_active_commerce(self, client, artisan_user_token, categorie_id):
        r1 = client.post("/api/commerces", json={
            "nom_commercial": "Active One", "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {artisan_user_token}"})
        active_id = r1.get_json()["id"]
        client.post("/api/commerces", json={
            "nom_commercial": "Other One", "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {artisan_user_token}"})

        client.patch("/api/artisan/active-commerce", json={
            "commerce_id": active_id,
        }, headers={"Authorization": f"Bearer {artisan_user_token}"})

        response = client.get("/api/artisan/commerces/cards", headers={
            "Authorization": f"Bearer {artisan_user_token}",
        })
        cards = response.get_json()["cards"]
        assert all(c["id"] != active_id for c in cards)

    def test_cards_returns_empty_when_one_commerce(self, client, artisan_user_token, categorie_id):
        client.post("/api/commerces", json={
            "nom_commercial": "Solo", "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {artisan_user_token}"})

        response = client.get("/api/artisan/commerces/cards", headers={
            "Authorization": f"Bearer {artisan_user_token}",
        })
        assert response.status_code == 200
        assert response.get_json()["cards"] == []

    def test_cards_returns_401_without_token(self, client):
        response = client.get("/api/artisan/commerces/cards")
        assert response.status_code == 401

    def test_cards_returns_403_for_client(self, client, user_token):
        response = client.get("/api/artisan/commerces/cards", headers={
            "Authorization": f"Bearer {user_token}",
        })
        assert response.status_code == 403
