import pytest
from unittest.mock import patch, MagicMock
from app.services import commerce_service, auth_service
from app.models.commerce import Commerce, CommercePhoto, HoraireOuverture, JourSemaine
from app.models.categorie import Categorie


HORAIRES = [
    {"jour": "lundi", "heure_ouverture": "08:00", "heure_fermeture": "18:00"},
    {"jour": "mardi", "heure_ouverture": "08:00", "heure_fermeture": "18:00"},
    {"jour": "mercredi", "heure_ouverture": "08:00", "heure_fermeture": "18:00"},
    {"jour": "jeudi", "heure_ouverture": "08:00", "heure_fermeture": "18:00"},
    {"jour": "vendredi", "heure_ouverture": "08:00", "heure_fermeture": "18:00"},
    {"jour": "samedi", "heure_ouverture": "08:00", "heure_fermeture": "13:00"},
    {"jour": "dimanche", "est_ferme": True},
]


class TestCreateStep1:
    def test_create_step1_creates_commerce(self, app):
        with app.app_context():
            user = auth_service.register(email="artisan@test.com", password="password123")
            cat = Categorie(nom="Boulangerie", is_active=True)
            cat.save()
            result = commerce_service.create_step1(user.id, {
                "nom_commercial": "Mon Commerce",
                "categorie_id": cat.id,
            })
            assert result["id"] is not None
            assert result["nom_commercial"] == "Mon Commerce"
            assert result["categorie_id"] == cat.id
            assert result["is_active"] is False
            assert result["step"] == 1

    def test_create_step1_with_optional_fields(self, app):
        with app.app_context():
            user = auth_service.register(email="artisan2@test.com", password="password123")
            cat = Categorie(nom="Restaurant", is_active=True)
            cat.save()
            result = commerce_service.create_step1(user.id, {
                "nom_commercial": "Commerce Complet",
                "categorie_id": cat.id,
                "whatsapp_numero": "+22507070707",
                "contact_telephonique": "+22501010101",
                "description": "Description test",
            })
            assert result["whatsapp_numero"] == "+22507070707"
            assert result["contact_telephonique"] == "+22501010101"
            assert result["description"] == "Description test"

    def test_create_step1_raises_on_unknown_categorie(self, app):
        with app.app_context():
            user = auth_service.register(email="artisan3@test.com", password="password123")
            with pytest.raises(ValueError, match="Categorie introuvable"):
                commerce_service.create_step1(user.id, {
                    "nom_commercial": "Test",
                    "categorie_id": 9999,
                })

    def test_create_step1_raises_on_inactive_categorie(self, app):
        with app.app_context():
            user = auth_service.register(email="artisan4@test.com", password="password123")
            cat = Categorie(nom="Inactif", is_active=False)
            cat.save()
            with pytest.raises(ValueError, match="desactivee"):
                commerce_service.create_step1(user.id, {
                    "nom_commercial": "Test",
                    "categorie_id": cat.id,
                })


class TestUpdateStep2:
    def test_update_step2_adds_localisation(self, app):
        with app.app_context():
            user = auth_service.register(email="step2@test.com", password="password123")
            cat = Categorie(nom="Coiffure", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="Salon", categorie_id=cat.id)
            commerce.save()
            result = commerce_service.update_step2(commerce.id, user.id, {
                "latitude": 5.3600,
                "longitude": -4.0083,
                "adresse_complete": "Abidjan, Cocody",
                "horaires": HORAIRES,
            })
            assert result["latitude"] == 5.36
            assert result["adresse_complete"] == "Abidjan, Cocody"
            assert result["step"] == 2
            horaires = HoraireOuverture.query.filter_by(commerce_id=commerce.id).all()
            assert len(horaires) == 7

    def test_update_step2_raises_on_wrong_owner(self, app):
        with app.app_context():
            user = auth_service.register(email="owner@test.com", password="password123")
            cat = Categorie(nom="Menuiserie", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="Atelier", categorie_id=cat.id)
            commerce.save()
            other_user = auth_service.register(email="other@test.com", password="password123")
            with pytest.raises(ValueError, match="Acces refuse"):
                commerce_service.update_step2(commerce.id, other_user.id, {
                    "latitude": 5.36,
                    "longitude": -4.0083,
                    "adresse_complete": "Test",
                    "horaires": [{"jour": "lundi"}] * 7,
                })

    def test_update_step2_raises_on_unknown_commerce(self, app):
        with app.app_context():
            user = auth_service.register(email="ghost@test.com", password="password123")
            with pytest.raises(ValueError, match="Commerce introuvable"):
                commerce_service.update_step2(9999, user.id, {
                    "latitude": 5.36,
                    "longitude": -4.0083,
                    "adresse_complete": "Test",
                    "horaires": [{"jour": "lundi"}] * 7,
                })


class TestUploadPhotos:
    def test_upload_photos_adds_photos(self, app):
        with app.app_context():
            user = auth_service.register(email="photo@test.com", password="password123")
            cat = Categorie(nom="Fleuriste", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="Fleurs", categorie_id=cat.id)
            commerce.save()
            mock_file = MagicMock()
            mock_file.content_type = "image/jpeg"
            mock_file.seek = MagicMock()
            mock_file.tell = MagicMock(return_value=1024 * 100)
            with patch("app.services.commerce_service.cloudinary.uploader.upload") as mock_upload:
                mock_upload.return_value = {"secure_url": "https://res.cloudinary.com/test/image.jpg"}
                result = commerce_service.upload_photos(commerce.id, user.id, [mock_file])
                assert len(result) == 1
                assert result[0]["url"] == "https://res.cloudinary.com/test/image.jpg"

    def test_upload_photos_raises_on_too_many(self, app):
        with app.app_context():
            user = auth_service.register(email="toomany@test.com", password="password123")
            cat = Categorie(nom="Peinture", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="Art", categorie_id=cat.id)
            commerce.save()
            for i in range(3):
                photo = CommercePhoto(commerce_id=commerce.id, url=f"http://test{i}.jpg", ordre=i + 1)
                photo.save()
            mock_file = MagicMock()
            mock_file.content_type = "image/jpeg"
            mock_file.seek = MagicMock()
            mock_file.tell = MagicMock(return_value=1024)
            with pytest.raises(ValueError, match="Maximum 3 photos"):
                commerce_service.upload_photos(commerce.id, user.id, [mock_file])

    def test_upload_photos_raises_on_invalid_type(self, app):
        with app.app_context():
            user = auth_service.register(email="pdf@test.com", password="password123")
            cat = Categorie(nom="Sculpture", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="Studio", categorie_id=cat.id)
            commerce.save()
            mock_file = MagicMock()
            mock_file.content_type = "application/pdf"
            mock_file.seek = MagicMock()
            mock_file.tell = MagicMock(return_value=1024)
            with pytest.raises(ValueError, match="Type non autorise"):
                commerce_service.upload_photos(commerce.id, user.id, [mock_file])


class TestDeletePhoto:
    def test_delete_photo_removes_photo(self, app):
        with app.app_context():
            user = auth_service.register(email="delp@test.com", password="password123")
            cat = Categorie(nom="Joaillerie", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="Bijoux", categorie_id=cat.id)
            commerce.save()
            photo = CommercePhoto(commerce_id=commerce.id, url="http://test.jpg", ordre=1)
            photo.save()
            photo_id = photo.id
            result = commerce_service.delete_photo(commerce.id, photo_id, user.id)
            assert "supprimee" in result["message"]
            assert CommercePhoto.query.get(photo_id) is None

    def test_delete_photo_raises_on_wrong_owner(self, app):
        with app.app_context():
            user = auth_service.register(email="owner2@test.com", password="password123")
            cat = Categorie(nom="Tapisserie", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="Tapis", categorie_id=cat.id)
            commerce.save()
            photo = CommercePhoto(commerce_id=commerce.id, url="http://test.jpg", ordre=1)
            photo.save()
            other_user = auth_service.register(email="other2@test.com", password="password123")
            with pytest.raises(ValueError, match="Acces refuse"):
                commerce_service.delete_photo(commerce.id, photo.id, other_user.id)


class TestPublish:
    def test_publish_activates_commerce(self, app):
        with app.app_context():
            user = auth_service.register(email="pub@test.com", password="password123")
            cat = Categorie(nom="Epicier", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="Epicerie", categorie_id=cat.id)
            commerce.save()
            commerce_service.update_step2(commerce.id, user.id, {
                "latitude": 5.36,
                "longitude": -4.0083,
                "adresse_complete": "Abidjan",
                "horaires": HORAIRES,
            })
            mock_file = MagicMock()
            mock_file.content_type = "image/jpeg"
            mock_file.seek = MagicMock()
            mock_file.tell = MagicMock(return_value=1024)
            with patch("app.services.commerce_service.cloudinary.uploader.upload") as mock_upload:
                mock_upload.return_value = {"secure_url": "https://test.jpg"}
                commerce_service.upload_photos(commerce.id, user.id, [mock_file])
            result = commerce_service.publish(commerce.id, user.id)
            assert result["is_active"] is True

    def test_publish_raises_on_missing_localisation(self, app):
        with app.app_context():
            user = auth_service.register(email="noloc@test.com", password="password123")
            cat = Categorie(nom="Boucherie", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="Boucherie", categorie_id=cat.id)
            commerce.save()
            with pytest.raises(ValueError, match="Etape 2 non terminee"):
                commerce_service.publish(commerce.id, user.id)

    def test_publish_raises_on_missing_photos(self, app):
        with app.app_context():
            user = auth_service.register(email="nophoto@test.com", password="password123")
            cat = Categorie(nom="Poissonnerie", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="Poisson", categorie_id=cat.id)
            commerce.save()
            commerce_service.update_step2(commerce.id, user.id, {
                "latitude": 5.36,
                "longitude": -4.0083,
                "adresse_complete": "Abidjan",
                "horaires": HORAIRES,
            })
            with pytest.raises(ValueError, match="Etape 3 non terminee"):
                commerce_service.publish(commerce.id, user.id)


class TestGetCommerce:
    def test_get_commerce_returns_data(self, app):
        with app.app_context():
            user = auth_service.register(email="get@test.com", password="password123")
            cat = Categorie(nom="Optique", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="Lunettes", categorie_id=cat.id)
            commerce.save()
            result = commerce_service.get_commerce(commerce.id, user.id)
            assert result["id"] == commerce.id
            assert result["step"] == 1

    def test_get_commerce_raises_on_wrong_owner(self, app):
        with app.app_context():
            user = auth_service.register(email="own@test.com", password="password123")
            cat = Categorie(nom="Papeterie", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="Papeterie", categorie_id=cat.id)
            commerce.save()
            other_user = auth_service.register(email="stranger@test.com", password="password123")
            with pytest.raises(ValueError, match="Acces refuse"):
                commerce_service.get_commerce(commerce.id, other_user.id)


class TestListCategories:
    def test_list_categories_returns_active_only(self, app):
        with app.app_context():
            Categorie(nom="Active", is_active=True).save()
            Categorie(nom="Inactive", is_active=False).save()
            result = commerce_service.list_categories()
            assert len(result) == 1
            assert result[0].nom == "Active"


class TestCreateCategory:
    def test_create_category(self, app):
        with app.app_context():
            result = commerce_service.create_category({"nom": "Jardinage"})
            assert result["nom"] == "Jardinage"

    def test_create_category_raises_on_duplicate(self, app):
        with app.app_context():
            commerce_service.create_category({"nom": "Doublon"})
            with pytest.raises(ValueError, match="existe deja"):
                commerce_service.create_category({"nom": "Doublon"})
