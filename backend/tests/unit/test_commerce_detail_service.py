from app.models.categorie import Categorie
from app.models.commerce import Commerce, CommercePhoto, HoraireOuverture, JourSemaine, ProduitImage
from app.models.commerce_avis import CommerceAvis
from app.services import auth_service
from app.services.commerce_detail_service import CommerceDetailService


def _create_active_commerce():
    artisan = auth_service.register(email="detail-artisan@test.com", password="password123")
    categorie = Categorie(nom="Restaurant", is_active=True)
    categorie.save()
    commerce = Commerce(
        user_id=artisan.id,
        nom_commercial="Chez Awa",
        contact_telephonique="+22501010101",
        whatsapp_numero="22507070707",
        categorie_id=categorie.id,
        description="Cuisine locale",
        latitude=5.36,
        longitude=-4.0083,
        adresse_complete="Abidjan, Cocody",
        is_active=True,
        is_vendeur_produits=True,
    )
    commerce.save()
    CommercePhoto(commerce_id=commerce.id, url="http://cover.jpg", ordre=1, is_principale=True).save()
    ProduitImage(commerce_id=commerce.id, url="http://produit.jpg", ordre=1).save()
    HoraireOuverture(
        commerce_id=commerce.id,
        jour=JourSemaine.lundi,
        est_24h=True,
    ).save()
    return commerce


class TestCommerceDetailService:
    def test_get_detail_returns_screen_payload(self, app):
        with app.app_context():
            commerce = _create_active_commerce()
            client = auth_service.register(email="client-detail@test.com", password="password123")
            CommerceAvis(commerce_id=commerce.id, user_id=client.id, note=4, commentaire="Tres bon").save()

            result = CommerceDetailService().get_detail(commerce.id, {"latitude": 5.35, "longitude": -4.00})

            assert result["nom_commercial"] == "Chez Awa"
            assert result["categorie"]["nom"] == "Restaurant"
            assert result["quartier"] == "Cocody"
            assert result["couverture"]["url"] == "http://cover.jpg"
            assert result["couverture"]["initiales"] == "CA"
            assert len(result["produit_images"]) == 1
            assert result["note_moyenne"] == 4
            assert result["nombre_avis"] == 1
            assert result["contacts"]["appel_url"] == "tel:+22501010101"
            assert "google.com/maps/dir" in result["contacts"]["itineraire_url"]
            assert result["localisation"]["distance_km"] is not None
            assert len(result["derniers_avis"]) == 1

    def test_create_avis_requires_citizen(self, app):
        with app.app_context():
            commerce = _create_active_commerce()
            client = auth_service.register(email="avis-client@test.com", password="password123")

            result = CommerceDetailService().create_avis(commerce.id, client.id, {
                "note": 5,
                "commentaire": "Excellent",
            })

            assert result["note"] == 5
            assert result["auteur"] == "avis-client"
