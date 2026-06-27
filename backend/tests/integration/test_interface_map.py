import pytest


@pytest.fixture
def user_token(client):
    client.post("/api/auth/register", json={
        "email": "map-artisan@test.com",
        "password": "password123",
    })
    login = client.post("/api/auth/login", json={
        "email": "map-artisan@test.com",
        "password": "password123",
    })
    return login.get_json()["access_token"]


@pytest.fixture
def categorie_id(client):
    with client.application.app_context():
        from app.models.categorie import Categorie
        cat = Categorie(nom="Map", is_active=True)
        cat.save()
        return cat.id


def _horaires():
    return [
        {"jour": "lundi"},
        {"jour": "mardi"},
        {"jour": "mercredi"},
        {"jour": "jeudi"},
        {"jour": "vendredi"},
        {"jour": "samedi"},
        {"jour": "dimanche", "est_ferme": True},
    ]


def _create_active_commerce(client, user_token, categorie_id, nom, latitude, longitude):
    response = client.post("/api/commerces", json={
        "nom_commercial": nom,
        "categorie_id": categorie_id,
    }, headers={"Authorization": f"Bearer {user_token}"})
    commerce_id = response.get_json()["id"]

    client.put(f"/api/commerces/{commerce_id}/localisation", json={
        "latitude": latitude,
        "longitude": longitude,
        "adresse_complete": nom,
        "horaires": _horaires(),
    }, headers={"Authorization": f"Bearer {user_token}"})

    with client.application.app_context():
        from app.models.commerce import Commerce, CommercePhoto
        commerce = Commerce.query.get(commerce_id)
        photo = CommercePhoto(commerce_id=commerce_id, url="http://test.jpg", ordre=1)
        photo.save()
        commerce.is_active = True
        commerce.save()

    return commerce_id


class TestInterfaceMap:
    def test_commerces_proches_returns_nearest_first(self, client, user_token, categorie_id):
        _create_active_commerce(client, user_token, categorie_id, "Proche", 5.36, -4.0083)
        _create_active_commerce(client, user_token, categorie_id, "Loin", 5.50, -4.20)

        response = client.post("/api/map/commerces-proches", json={
            "latitude": 5.35,
            "longitude": -4.00,
            "rayon_km": 50,
        })

        assert response.status_code == 200
        data = response.get_json()
        assert data["count"] == 2
        assert data["commerce_plus_proche"]["nom_commercial"] == "Proche"
        assert data["commerces"][0]["distance_km"] <= data["commerces"][1]["distance_km"]
        assert "google.com/maps/dir" in data["commerces"][0]["itineraire_url"]

    def test_commerces_proches_validates_position(self, client):
        response = client.post("/api/map/commerces-proches", json={
            "latitude": 120,
            "longitude": -4.00,
        })

        assert response.status_code == 400
        assert "latitude" in response.get_json()["error"]
