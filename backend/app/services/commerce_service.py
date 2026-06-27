import cloudinary
import cloudinary.uploader
from datetime import datetime, timedelta, timezone
from urllib.parse import quote
from ..extensions import db
from ..models.commerce import (
    Commerce, CommercePhoto, CommerceStats, HoraireOuverture,
    JourSemaine, Favori, VueProfile, ProduitImage,
)
from ..models.categorie import Categorie
from ..models.user import User


ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_FILE_SIZE_MB = 5
MAX_PHOTOS = 3
MAX_PRODUIT_IMAGES = 5
VIEW_COOLDOWN_HOURS = 24


def _get_step(commerce):
    if commerce.adresse_complete and commerce.latitude is not None:
        has_photos = CommercePhoto.query.filter_by(commerce_id=commerce.id).first() is not None
        if has_photos:
            return 3
        return 2
    return 1


class CommerceService:

    def create_step1(self, user_id, data):
        categorie = Categorie.query.get(data["categorie_id"])
        if not categorie:
            raise ValueError("Categorie introuvable.")
        if not categorie.is_active:
            raise ValueError("Cette categorie est desactivee.")

        commerce = Commerce(
            user_id=user_id,
            nom_commercial=data["nom_commercial"],
            whatsapp_numero=data.get("whatsapp_numero"),
            contact_telephonique=data.get("contact_telephonique"),
            categorie_id=data["categorie_id"],
            description=data.get("description"),
            is_vendeur_produits=data.get("is_vendeur_produits", False),
        )
        commerce.save()
        result = commerce.to_dict()
        result["step"] = 1
        return result

    def update_step2(self, commerce_id, user_id, data):
        commerce = Commerce.query.get(commerce_id)
        if not commerce:
            raise ValueError("Commerce introuvable.")
        if commerce.user_id != user_id:
            raise ValueError("Acces refuse.")

        commerce.latitude = data["latitude"]
        commerce.longitude = data["longitude"]
        commerce.adresse_complete = data["adresse_complete"]

        HoraireOuverture.query.filter_by(commerce_id=commerce.id).delete()

        for h in data["horaires"]:
            horaire = HoraireOuverture(
                commerce_id=commerce.id,
                jour=JourSemaine(h["jour"]),
                heure_ouverture=datetime.strptime(h["heure_ouverture"], "%H:%M").time() if h.get("heure_ouverture") else None,
                heure_fermeture=datetime.strptime(h["heure_fermeture"], "%H:%M").time() if h.get("heure_fermeture") else None,
                est_ferme=h.get("est_ferme", False),
                est_24h=h.get("est_24h", False),
            )
            db.session.add(horaire)

        db.session.commit()
        result = commerce.to_dict()
        result["step"] = 2
        return result

    def upload_photos(self, commerce_id, user_id, files):
        commerce = Commerce.query.get(commerce_id)
        if not commerce:
            raise ValueError("Commerce introuvable.")
        if commerce.user_id != user_id:
            raise ValueError("Acces refuse.")

        existing_count = CommercePhoto.query.filter_by(commerce_id=commerce.id).count()
        if existing_count + len(files) > MAX_PHOTOS:
            raise ValueError(f"Maximum {MAX_PHOTOS} photos autorisees.")

        uploaded = []
        for file in files:
            if file.content_type not in ALLOWED_MIME_TYPES:
                raise ValueError(f"Type non autorise: {file.content_type}. Utilisez JPG, PNG ou WebP.")

            file.seek(0, 2)
            size_mb = file.tell() / (1024 * 1024)
            file.seek(0)
            if size_mb > MAX_FILE_SIZE_MB:
                raise ValueError(f"Fichier trop volumineux: {size_mb:.1f}MB (max {MAX_FILE_SIZE_MB}MB).")

            result = cloudinary.uploader.upload(
                file,
                folder="zulu/commerces",
                resource_type="image",
            )

            is_first = existing_count == 0 and len(uploaded) == 0
            photo = CommercePhoto(
                commerce_id=commerce.id,
                url=result["secure_url"],
                alt_text=f"Photo {existing_count + len(uploaded) + 1}",
                ordre=existing_count + len(uploaded) + 1,
                is_principale=is_first,
            )
            photo.save()
            uploaded.append(photo.to_dict())

        return uploaded

    def delete_photo(self, commerce_id, photo_id, user_id):
        commerce = Commerce.query.get(commerce_id)
        if not commerce:
            raise ValueError("Commerce introuvable.")
        if commerce.user_id != user_id:
            raise ValueError("Acces refuse.")

        photo = CommercePhoto.query.get(photo_id)
        if not photo or photo.commerce_id != commerce.id:
            raise ValueError("Photo introuvable.")

        photo.delete()
        return {"message": "Photo supprimee."}

    def publish(self, commerce_id, user_id):
        commerce = Commerce.query.get(commerce_id)
        if not commerce:
            raise ValueError("Commerce introuvable.")
        if commerce.user_id != user_id:
            raise ValueError("Acces refuse.")

        if not commerce.adresse_complete or commerce.latitude is None:
            raise ValueError("Etape 2 non terminee (localisation manquante).")

        has_photos = CommercePhoto.query.filter_by(commerce_id=commerce.id).first() is not None
        if not has_photos:
            raise ValueError("Etape 3 non terminee (aucune photo).")

        commerce.is_active = True
        commerce.save()
        return commerce.to_dict()

    def get_commerce(self, commerce_id, user_id):
        commerce = Commerce.query.get(commerce_id)
        if not commerce:
            raise ValueError("Commerce introuvable.")
        if commerce.user_id != user_id:
            raise ValueError("Acces refuse.")

        result = commerce.to_dict()
        result["step"] = _get_step(commerce)
        return result

    def list_categories(self):
        return Categorie.query.filter_by(is_active=True).all()

    def create_category(self, data):
        if Categorie.query.filter_by(nom=data["nom"]).first():
            raise ValueError("Cette categorie existe deja.")
        cat = Categorie(nom=data["nom"])
        cat.save()
        return cat.to_dict()

    def get_artisan_profile(self, user_id):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("Utilisateur introuvable.")

        commerces = Commerce.query.filter_by(user_id=user_id).all()

        return {
            "user": {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "is_verified": user.is_verified,
            },
            "commerces": [
                {
                    "id": c.id,
                    "nom_commercial": c.nom_commercial,
                    "whatsapp_numero": c.whatsapp_numero,
                    "contact_telephonique": c.contact_telephonique,
                    "is_active": c.is_active,
                }
                for c in commerces
            ],
            "nb_commerces_actifs": sum(1 for c in commerces if c.is_active),
        }

    def get_artisan_home(self, user_id):
        commerce = Commerce.query.filter_by(user_id=user_id).first()
        if not commerce:
            raise ValueError("Aucun commerce trouve pour cet artisan.")

        stats = CommerceStats.query.filter_by(commerce_id=commerce.id).first()
        if not stats:
            stats = CommerceStats(commerce_id=commerce.id)
            stats.save()

        result = commerce.to_dict()
        result["step"] = _get_step(commerce)
        result["stats"] = stats.to_dict()
        result["categorie"] = commerce.categorie.to_dict() if commerce.categorie else None
        result["photos"] = [p.to_dict() for p in commerce.photos]
        result["horaires"] = [h.to_dict() for h in commerce.horaires]
        result["produit_images"] = sorted(
            [pi.to_dict() for pi in commerce.produit_images],
            key=lambda x: x["ordre"],
        )

        first_name = commerce.user.first_name or commerce.user.email.split("@")[0]
        geolocalisation_url = _build_whatsapp_geo_url(
            commerce.nom_commercial,
            commerce.latitude,
            commerce.longitude,
        )

        return {
            "message": f"Bienvenue, {first_name}",
            "commerce": result,
            "geolocalisation_url": geolocalisation_url,
        }

    def record_vue(self, commerce_id, ip_address=None, user_agent=None, user_id=None):
        commerce = Commerce.query.get(commerce_id)
        if not commerce:
            raise ValueError("Commerce introuvable.")

        if ip_address:
            cooldown = datetime.now(timezone.utc) - timedelta(hours=VIEW_COOLDOWN_HOURS)
            existing = VueProfile.query.filter(
                VueProfile.commerce_id == commerce_id,
                VueProfile.ip_address == ip_address,
                VueProfile.viewed_at >= cooldown,
            ).first()
            if existing:
                return {"message": "Vue deja enregistree.", "counted": False}

        vue = VueProfile(
            commerce_id=commerce_id,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            viewed_at=datetime.now(timezone.utc),
        )
        db.session.add(vue)

        stats = CommerceStats.query.filter_by(commerce_id=commerce_id).first()
        if not stats:
            stats = CommerceStats(commerce_id=commerce_id)
            db.session.add(stats)

        stats.nb_vues_profile = (stats.nb_vues_profile or 0) + 1
        stats.last_vue_at = datetime.now(timezone.utc)

        db.session.commit()
        return {"message": "Vue enregistree.", "counted": True}

    def add_favori(self, user_id, commerce_id):
        commerce = Commerce.query.get(commerce_id)
        if not commerce:
            raise ValueError("Commerce introuvable.")

        existing = Favori.query.filter_by(user_id=user_id, commerce_id=commerce_id).first()
        if existing:
            raise ValueError("Ce commerce est deja dans vos favoris.")

        favori = Favori(user_id=user_id, commerce_id=commerce_id)
        db.session.add(favori)

        stats = CommerceStats.query.filter_by(commerce_id=commerce_id).first()
        if not stats:
            stats = CommerceStats(commerce_id=commerce_id)
            db.session.add(stats)
        stats.nb_favoris = (stats.nb_favoris or 0) + 1

        db.session.commit()
        return {"message": "Ajoute aux favoris.", "favori": favori.to_dict()}

    def remove_favori(self, user_id, commerce_id):
        favori = Favori.query.filter_by(user_id=user_id, commerce_id=commerce_id).first()
        if not favori:
            raise ValueError("Favori introuvable.")

        favori.delete()

        stats = CommerceStats.query.filter_by(commerce_id=commerce_id).first()
        if stats and stats.nb_favoris > 0:
            stats.nb_favoris -= 1
            stats.save()

        return {"message": "Retire des favoris."}

    def list_favoris(self, user_id):
        favoris = Favori.query.filter_by(user_id=user_id).all()
        result = []
        for f in favoris:
            commerce = Commerce.query.get(f.commerce_id)
            if commerce:
                item = f.to_dict()
                item["commerce"] = commerce.to_dict()
                result.append(item)
        return result

    def upload_produit_image(self, commerce_id, user_id, file):
        commerce = Commerce.query.get(commerce_id)
        if not commerce:
            raise ValueError("Commerce introuvable.")
        if commerce.user_id != user_id:
            raise ValueError("Acces refuse.")
        if not commerce.is_vendeur_produits:
            raise ValueError("Ce commerce n'est pas vendeur de produits.")

        existing_count = ProduitImage.query.filter_by(commerce_id=commerce.id).count()
        if existing_count >= MAX_PRODUIT_IMAGES:
            raise ValueError(f"Maximum {MAX_PRODUIT_IMAGES} images de produits autorisees.")

        if file.content_type not in ALLOWED_MIME_TYPES:
            raise ValueError(f"Type non autorise: {file.content_type}. Utilisez JPG, PNG ou WebP.")

        file.seek(0, 2)
        size_mb = file.tell() / (1024 * 1024)
        file.seek(0)
        if size_mb > MAX_FILE_SIZE_MB:
            raise ValueError(f"Fichier trop volumineux: {size_mb:.1f}MB (max {MAX_FILE_SIZE_MB}MB).")

        result = cloudinary.uploader.upload(
            file,
            folder="zulu/produits",
            resource_type="image",
        )

        image = ProduitImage(
            commerce_id=commerce.id,
            url=result["secure_url"],
            ordre=existing_count + 1,
        )
        image.save()
        return image.to_dict()

    def delete_produit_image(self, commerce_id, image_id, user_id):
        commerce = Commerce.query.get(commerce_id)
        if not commerce:
            raise ValueError("Commerce introuvable.")
        if commerce.user_id != user_id:
            raise ValueError("Acces refuse.")

        image = ProduitImage.query.get(image_id)
        if not image or image.commerce_id != commerce.id:
            raise ValueError("Image introuvable.")

        image.delete()
        return {"message": "Image produit supprimee."}

    def build_geolocalisation_url(self, commerce_id, user_id=None):
        commerce = Commerce.query.get(commerce_id)
        if not commerce:
            raise ValueError("Commerce introuvable.")

        return _build_whatsapp_geo_url(
            commerce.nom_commercial,
            commerce.latitude,
            commerce.longitude,
        )


def _build_whatsapp_geo_url(commerce_name, latitude, longitude):
    if latitude is None or longitude is None:
        return None

    maps_link = f"https://maps.google.com/?q={latitude},{longitude}"
    message = f"Voici la localisation de {commerce_name} sur Google Maps :\n{maps_link}"
    encoded = quote(message)
    return f"https://wa.me/?text={encoded}"
