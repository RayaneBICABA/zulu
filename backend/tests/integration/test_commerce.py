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
    def test_create_category_returns_201(self, client, user_token):
        response = client.post("/api/categories", json={
            "nom": "Coiffure",
        }, headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 201
        data = response.get_json()
        assert data["nom"] == "Coiffure"

    def test_create_category_returns_400_on_missing_nom(self, client, user_token):
        response = client.post("/api/categories", json={}, headers={
            "Authorization": f"Bearer {user_token}",
        })
        assert response.status_code == 400

    def test_create_category_returns_409_on_duplicate(self, client, user_token, categorie_id):
        response = client.post("/api/categories", json={
            "nom": "Boulangerie",
        }, headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 409

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
            assert len(response.get_json()) == 1

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
    def test_artisan_home_returns_200(self, client, user_token, categorie_id):
        client.post("/api/commerces", json={
            "nom_commercial": "Mon Salon",
            "categorie_id": categorie_id,
        }, headers={"Authorization": f"Bearer {user_token}"})
        response = client.get("/api/artisan/home", headers={
            "Authorization": f"Bearer {user_token}",
        })
        assert response.status_code == 200
        data = response.get_json()
        assert "Bienvenue" in data["message"]
        assert data["commerce"]["nom_commercial"] == "Mon Salon"
        assert "stats" in data["commerce"]
        assert "photos" in data["commerce"]
        assert "horaires" in data["commerce"]
        assert "produit_images" in data["commerce"]

    def test_artisan_home_returns_404_without_commerce(self, client, user_token):
        response = client.get("/api/artisan/home", headers={
            "Authorization": f"Bearer {user_token}",
        })
        assert response.status_code == 404
        assert "Aucun commerce" in response.get_json()["error"]


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
