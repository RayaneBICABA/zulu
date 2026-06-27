import pytest
from app.models.commerce_avis import CommerceAvis


@pytest.fixture
def user_token(client):
    client.post("/api/auth/register", json={
        "email": "detail-route@test.com",
        "password": "password123",
    })
    login = client.post("/api/auth/login", json={
        "email": "detail-route@test.com",
        "password": "password123",
    })
    return login.get_json()["access_token"]


class TestCommerceDetailRoute:
    def test_blueprint_can_be_registered_locally(self, app, client, user_token):
        from app.routes.commerce_detail import commerce_detail_bp

        if "commerce_detail.get_commerce_detail" not in app.view_functions:
            app.register_blueprint(commerce_detail_bp, url_prefix="/api")

        with app.app_context():
            from app.models.categorie import Categorie
            from app.models.commerce import Commerce
            from app.models.user import User

            user = User.query.filter_by(email="detail-route@test.com").first()
            categorie = Categorie(nom="Detail Route", is_active=True)
            categorie.save()
            commerce = Commerce(
                user_id=user.id,
                nom_commercial="Detail Commerce",
                categorie_id=categorie.id,
                latitude=5.36,
                longitude=-4.0083,
                adresse_complete="Abidjan, Plateau",
                is_active=True,
            )
            commerce.save()
            commerce_id = commerce.id

        response = client.get(f"/api/commerces/{commerce_id}/detail?latitude=5.35&longitude=-4.00")

        assert response.status_code == 200
        data = response.get_json()
        assert data["nom_commercial"] == "Detail Commerce"
        assert data["quartier"] == "Plateau"
        assert "distance_km" in data["localisation"]
