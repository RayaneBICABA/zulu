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


class TestGetArtisanHome:
    def test_returns_bienvenue_message(self, app):
        with app.app_context():
            from app.models.commerce import CommerceStats, CommercePhoto, ProduitImage
            user = auth_service.register(email="artisan@home.com", password="password123")
            user.first_name = "Kofi"
            user.save()
            cat = Categorie(nom="Coiffure", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="Salon Kofi", categorie_id=cat.id, latitude=5.36, longitude=-4.0083)
            commerce.save()
            stats = CommerceStats(commerce_id=commerce.id)
            stats.save()
            result = commerce_service.get_artisan_home(user.id)
            assert result["message"] == "Bienvenue, Kofi"
            assert result["commerce"]["id"] == commerce.id
            assert result["commerce"]["stats"]["nb_vues_profile"] == 0
            assert result["geolocalisation_url"] is not None
            assert "wa.me" in result["geolocalisation_url"]

    def test_returns_email_as_fallback_name(self, app):
        with app.app_context():
            user = auth_service.register(email="sansnom@test.com", password="password123")
            cat = Categorie(nom="Jardinage", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="Jardin", categorie_id=cat.id)
            commerce.save()
            result = commerce_service.get_artisan_home(user.id)
            assert result["message"] == "Bienvenue, sansnom"

    def test_raises_when_no_commerce(self, app):
        with app.app_context():
            user = auth_service.register(email="empty@test.com", password="password123")
            with pytest.raises(ValueError, match="Aucun commerce"):
                commerce_service.get_artisan_home(user.id)

    def test_includes_produit_images(self, app):
        with app.app_context():
            from app.models.commerce import ProduitImage
            user = auth_service.register(email="prod@test.com", password="password123")
            cat = Categorie(nom="Bijoux", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="Bijoux Pro", categorie_id=cat.id)
            commerce.save()
            img = ProduitImage(commerce_id=commerce.id, url="http://img.jpg", ordre=1)
            img.save()
            result = commerce_service.get_artisan_home(user.id)
            assert len(result["commerce"]["produit_images"]) == 1


class TestRecordVue:
    def test_records_vue(self, app):
        with app.app_context():
            from app.models.commerce import CommerceStats, VueProfile
            user = auth_service.register(email="vu@test.com", password="password123")
            cat = Categorie(nom="Vente", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="Boutique", categorie_id=cat.id)
            commerce.save()
            result = commerce_service.record_vue(commerce.id, ip_address="192.168.1.1", user_agent="Mozilla")
            assert result["counted"] is True
            stats = CommerceStats.query.filter_by(commerce_id=commerce.id).first()
            assert stats.nb_vues_profile == 1

    def test_anti_spam_blocks_duplicate(self, app):
        with app.app_context():
            user = auth_service.register(email="spam@test.com", password="password123")
            cat = Categorie(nom="Fleurs", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="Fleuriste", categorie_id=cat.id)
            commerce.save()
            commerce_service.record_vue(commerce.id, ip_address="10.0.0.1")
            result = commerce_service.record_vue(commerce.id, ip_address="10.0.0.1")
            assert result["counted"] is False

    def test_raises_on_unknown_commerce(self, app):
        with app.app_context():
            with pytest.raises(ValueError, match="Commerce introuvable"):
                commerce_service.record_vue(9999, ip_address="10.0.0.1")

    def test_allows_different_ip(self, app):
        with app.app_context():
            from app.models.commerce import CommerceStats
            user = auth_service.register(email="diff@test.com", password="password123")
            cat = Categorie(nom="Art", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="Gallery", categorie_id=cat.id)
            commerce.save()
            commerce_service.record_vue(commerce.id, ip_address="10.0.0.1")
            commerce_service.record_vue(commerce.id, ip_address="10.0.0.2")
            stats = CommerceStats.query.filter_by(commerce_id=commerce.id).first()
            assert stats.nb_vues_profile == 2


class TestAddFavori:
    def test_adds_favori(self, app):
        with app.app_context():
            from app.models.commerce import CommerceStats
            user = auth_service.register(email="fav@test.com", password="password123")
            cat = Categorie(nom="Mode", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="Boutique", categorie_id=cat.id)
            commerce.save()
            result = commerce_service.add_favori(user.id, commerce.id)
            assert "favori" in result
            stats = CommerceStats.query.filter_by(commerce_id=commerce.id).first()
            assert stats.nb_favoris == 1

    def test_raises_on_duplicate(self, app):
        with app.app_context():
            user = auth_service.register(email="dup@test.com", password="password123")
            cat = Categorie(nom="Livres", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="Librairie", categorie_id=cat.id)
            commerce.save()
            commerce_service.add_favori(user.id, commerce.id)
            with pytest.raises(ValueError, match="deja dans vos favoris"):
                commerce_service.add_favori(user.id, commerce.id)

    def test_raises_on_unknown_commerce(self, app):
        with app.app_context():
            user = auth_service.register(email="noexist@test.com", password="password123")
            with pytest.raises(ValueError, match="Commerce introuvable"):
                commerce_service.add_favori(user.id, 9999)


class TestRemoveFavori:
    def test_removes_favori(self, app):
        with app.app_context():
            from app.models.commerce import CommerceStats
            user = auth_service.register(email="rmfav@test.com", password="password123")
            cat = Categorie(nom="Sport", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="SportShop", categorie_id=cat.id)
            commerce.save()
            commerce_service.add_favori(user.id, commerce.id)
            result = commerce_service.remove_favori(user.id, commerce.id)
            assert "Retire" in result["message"]
            stats = CommerceStats.query.filter_by(commerce_id=commerce.id).first()
            assert stats.nb_favoris == 0

    def test_raises_on_not_found(self, app):
        with app.app_context():
            user = auth_service.register(email="norem@test.com", password="password123")
            with pytest.raises(ValueError, match="Favori introuvable"):
                commerce_service.remove_favori(user.id, 9999)


class TestListFavoris:
    def test_returns_favoris(self, app):
        with app.app_context():
            user = auth_service.register(email="listfav@test.com", password="password123")
            cat = Categorie(nom="Musique", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="Studio", categorie_id=cat.id)
            commerce.save()
            commerce_service.add_favori(user.id, commerce.id)
            result = commerce_service.list_favoris(user.id)
            assert len(result) == 1
            assert "commerce" in result[0]

    def test_returns_empty_list(self, app):
        with app.app_context():
            user = auth_service.register(email="emptyfav@test.com", password="password123")
            result = commerce_service.list_favoris(user.id)
            assert result == []


class TestUploadProduitImage:
    def test_uploads_image(self, app):
        with app.app_context():
            user = auth_service.register(email="prodimg@test.com", password="password123")
            cat = Categorie(nom="Alimentation", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="Maraicher", categorie_id=cat.id, is_vendeur_produits=True)
            commerce.save()
            mock_file = MagicMock()
            mock_file.content_type = "image/jpeg"
            mock_file.seek = MagicMock()
            mock_file.tell = MagicMock(return_value=1024)
            with patch("app.services.commerce_service.cloudinary.uploader.upload") as mock_upload:
                mock_upload.return_value = {"secure_url": "https://res.cloudinary.com/test/prod.jpg"}
                result = commerce_service.upload_produit_image(commerce.id, user.id, mock_file)
                assert result["url"] == "https://res.cloudinary.com/test/prod.jpg"
                assert result["ordre"] == 1

    def test_raises_on_non_vendeur(self, app):
        with app.app_context():
            user = auth_service.register(email="nonvendeur@test.com", password="password123")
            cat = Categorie(nom="Fleuriste", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="Fleurs", categorie_id=cat.id, is_vendeur_produits=False)
            commerce.save()
            mock_file = MagicMock()
            mock_file.content_type = "image/jpeg"
            mock_file.seek = MagicMock()
            mock_file.tell = MagicMock(return_value=1024)
            with pytest.raises(ValueError, match="n'est pas vendeur"):
                commerce_service.upload_produit_image(commerce.id, user.id, mock_file)

    def test_raises_on_max_images(self, app):
        with app.app_context():
            from app.models.commerce import ProduitImage
            user = auth_service.register(email="maxprod@test.com", password="password123")
            cat = Categorie(nom="Tissus", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="TissusPro", categorie_id=cat.id, is_vendeur_produits=True)
            commerce.save()
            for i in range(5):
                img = ProduitImage(commerce_id=commerce.id, url=f"http://img{i}.jpg", ordre=i + 1)
                img.save()
            mock_file = MagicMock()
            mock_file.content_type = "image/jpeg"
            mock_file.seek = MagicMock()
            mock_file.tell = MagicMock(return_value=1024)
            with pytest.raises(ValueError, match="Maximum 5"):
                commerce_service.upload_produit_image(commerce.id, user.id, mock_file)


class TestDeleteProduitImage:
    def test_deletes_image(self, app):
        with app.app_context():
            from app.models.commerce import ProduitImage
            user = auth_service.register(email="delprod@test.com", password="password123")
            cat = Categorie(nom="Cuir", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="Maroquinerie", categorie_id=cat.id)
            commerce.save()
            img = ProduitImage(commerce_id=commerce.id, url="http://img.jpg", ordre=1)
            img.save()
            img_id = img.id
            result = commerce_service.delete_produit_image(commerce.id, img_id, user.id)
            assert "supprimee" in result["message"]
            assert ProduitImage.query.get(img_id) is None

    def test_raises_on_wrong_owner(self, app):
        with app.app_context():
            from app.models.commerce import ProduitImage
            user = auth_service.register(email="ownerprod@test.com", password="password123")
            cat = Categorie(nom="Poterie", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="Potier", categorie_id=cat.id)
            commerce.save()
            img = ProduitImage(commerce_id=commerce.id, url="http://img.jpg", ordre=1)
            img.save()
            other = auth_service.register(email="otherprod@test.com", password="password123")
            with pytest.raises(ValueError, match="Acces refuse"):
                commerce_service.delete_produit_image(commerce.id, img.id, other.id)


class TestBuildGeolocalisationUrl:
    def test_returns_url_with_coords(self, app):
        with app.app_context():
            user = auth_service.register(email="geo@test.com", password="password123")
            cat = Categorie(nom="Restaurant", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="Chez Tanti", categorie_id=cat.id, latitude=5.36, longitude=-4.0083)
            commerce.save()
            url = commerce_service.build_geolocalisation_url(commerce.id)
            assert "wa.me" in url
            assert "maps.google.com" in url
            assert "5.36" in url

    def test_returns_none_when_no_coords(self, app):
        with app.app_context():
            user = auth_service.register(email="nogeo@test.com", password="password123")
            cat = Categorie(nom="Bijoux", is_active=True)
            cat.save()
            commerce = Commerce(user_id=user.id, nom_commercial="BijouxGeo", categorie_id=cat.id)
            commerce.save()
            url = commerce_service.build_geolocalisation_url(commerce.id)
            assert url is None


class TestGetArtisanProfile:
    def test_returns_profile_with_commerce(self, app):
        with app.app_context():
            user = auth_service.register(email="profile@test.com", password="password123")
            user.first_name = "Ali"
            user.last_name = "Kone"
            user.save()
            cat = Categorie(nom="Tapis", is_active=True)
            cat.save()
            commerce = Commerce(
                user_id=user.id, nom_commercial="Tapisserie Ali",
                categorie_id=cat.id,
                whatsapp_numero="+22607070707",
                contact_telephonique="+22601010101",
                is_active=True,
            )
            commerce.save()
            result = commerce_service.get_artisan_profile(user.id)
            assert result["user"]["id"] == user.id
            assert result["user"]["first_name"] == "Ali"
            assert result["user"]["last_name"] == "Kone"
            assert result["user"]["email"] == "profile@test.com"
            assert result["nb_commerces_actifs"] == 1
            assert len(result["commerces"]) == 1
            assert result["commerces"][0]["nom_commercial"] == "Tapisserie Ali"
            assert result["commerces"][0]["whatsapp_numero"] == "+22607070707"
            assert result["commerces"][0]["is_active"] is True

    def test_returns_empty_commerces_list(self, app):
        with app.app_context():
            user = auth_service.register(email="nocommerce@test.com", password="password123")
            result = commerce_service.get_artisan_profile(user.id)
            assert result["nb_commerces_actifs"] == 0
            assert result["commerces"] == []
            assert result["user"]["email"] == "nocommerce@test.com"

    def test_returns_multiple_commerces(self, app):
        with app.app_context():
            user = auth_service.register(email="multi@test.com", password="password123")
            cat = Categorie(nom="Multi", is_active=True)
            cat.save()
            c1 = Commerce(user_id=user.id, nom_commercial="Commerce 1", categorie_id=cat.id)
            c1.save()
            c2 = Commerce(user_id=user.id, nom_commercial="Commerce 2", categorie_id=cat.id)
            c2.save()
            result = commerce_service.get_artisan_profile(user.id)
            assert result["nb_commerces_actifs"] == 0
            assert len(result["commerces"]) == 2
            names = {c["nom_commercial"] for c in result["commerces"]}
            assert names == {"Commerce 1", "Commerce 2"}

    def test_counts_only_active_commerces(self, app):
        with app.app_context():
            user = auth_service.register(email="mix@test.com", password="password123")
            cat = Categorie(nom="Mix", is_active=True)
            cat.save()
            c1 = Commerce(user_id=user.id, nom_commercial="Actif", categorie_id=cat.id, is_active=True)
            c1.save()
            c2 = Commerce(user_id=user.id, nom_commercial="Inactif", categorie_id=cat.id, is_active=False)
            c2.save()
            result = commerce_service.get_artisan_profile(user.id)
            assert result["nb_commerces_actifs"] == 1
            assert len(result["commerces"]) == 2

    def test_raises_on_unknown_user(self, app):
        with app.app_context():
            with pytest.raises(ValueError, match="Utilisateur introuvable"):
                commerce_service.get_artisan_profile(9999)
