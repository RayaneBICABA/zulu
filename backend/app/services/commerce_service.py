import cloudinary
import cloudinary.uploader
from datetime import datetime
from ..extensions import db
from ..models.commerce import Commerce, CommercePhoto, HoraireOuverture, JourSemaine
from ..models.categorie import Categorie


ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_FILE_SIZE_MB = 5
MAX_PHOTOS = 3


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
