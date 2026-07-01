import cloudinary
import cloudinary.uploader
from datetime import datetime, timedelta, timezone
from urllib.parse import quote
from ..extensions import db
from ..models.commerce import (
    Commerce, CommercePhoto, CommerceStats, HoraireOuverture,
    JourSemaine, Favori, VueProfile, ProduitImage,
)
from ..models.commentaire import Commentaire
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

    def list_public_commerces(self, search=None, categorie_id=None, page=1, per_page=20):
        query = Commerce.query.filter_by(is_active=True)

        if search:
            term = f"%{search}%"
            query = query.outerjoin(Categorie).filter(
                db.or_(
                    Commerce.nom_commercial.ilike(term),
                    Commerce.description.ilike(term),
                    Categorie.nom.ilike(term),
                )
            )

        if categorie_id:
            query = query.filter_by(categorie_id=categorie_id)

        query = query.order_by(Commerce.created_at.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        results = []
        for c in pagination.items:
            photo = next((p.url for p in c.photos if p.is_principale), None)
            if not photo and c.photos:
                photo = c.photos[0].url
            stats = c.stats
            results.append({
                "id": c.id,
                "nom_commercial": c.nom_commercial,
                "description": c.description,
                "categorie": c.categorie.to_dict() if c.categorie else None,
                "adresse_complete": c.adresse_complete,
                "latitude": float(c.latitude) if c.latitude else None,
                "longitude": float(c.longitude) if c.longitude else None,
                "photo_principale": photo,
                "is_verified": c.is_verified,
                "average_rating": float(stats.average_rating) if stats and stats.average_rating else 0.0,
                "rating_count": stats.rating_count if stats else 0,
                "nb_favoris": stats.nb_favoris if stats else 0,
                "nb_commentaires": stats.nb_commentaires if stats else 0,
            })

        return {
            "commerces": results,
            "total": pagination.total,
            "page": pagination.page,
            "per_page": pagination.per_page,
            "pages": pagination.pages,
        }

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

        user = User.query.get(user_id)
        if user and not user.active_commerce_id:
            user.active_commerce_id = commerce.id
            user.save()

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

        auto_published = False
        if not commerce.is_active:
            nb_commerces = Commerce.query.filter_by(user_id=user_id).count()
            if nb_commerces == 1:
                commerce.is_active = True
                commerce.save()
                auto_published = True

        return {"photos": uploaded, "auto_published": auto_published}

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
        if commerce.user_id != user_id and not commerce.is_active:
            raise ValueError("Commerce introuvable.")

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

    def update_category(self, categorie_id, data):
        cat = Categorie.query.get(categorie_id)
        if not cat:
            raise ValueError("Categorie introuvable.")
        if "nom" in data and data["nom"] != cat.nom:
            if Categorie.query.filter_by(nom=data["nom"]).first():
                raise ValueError("Ce nom de categorie existe deja.")
            cat.nom = data["nom"]
        if "is_active" in data:
            cat.is_active = data["is_active"]
        cat.save()
        return cat.to_dict()

    def delete_category(self, categorie_id):
        cat = Categorie.query.get(categorie_id)
        if not cat:
            raise ValueError("Categorie introuvable.")
        cat.is_active = False
        cat.save()
        return {"message": "Categorie desactivee."}

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
                "active_commerce_id": user.active_commerce_id,
            },
            "commerces": [
                {
                    "id": c.id,
                    "nom_commercial": c.nom_commercial,
                    "whatsapp_numero": c.whatsapp_numero,
                    "contact_telephonique": c.contact_telephonique,
                    "is_active": c.is_active,
                    "is_active_commerce": c.id == user.active_commerce_id,
                }
                for c in commerces
            ],
            "nb_commerces_actifs": sum(1 for c in commerces if c.is_active),
        }

    def get_artisan_home(self, user_id):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("Utilisateur introuvable.")

        commerce = None
        if user.active_commerce_id:
            commerce = Commerce.query.get(user.active_commerce_id)
            if not commerce or commerce.user_id != user_id:
                commerce = None

        if not commerce:
            commerce = Commerce.query.filter_by(user_id=user_id).first()
            if commerce:
                user.active_commerce_id = commerce.id
                user.save()

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

        first_name = user.first_name or user.email.split("@")[0]
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

    def create_commentaire(self, user_id, commerce_id, data):
        commerce = Commerce.query.get(commerce_id)
        if not commerce:
            raise ValueError("Commerce introuvable.")
        if not commerce.is_active:
            raise ValueError("Ce commerce n'est pas encore publie.")
        if commerce.user_id == user_id:
            raise ValueError("Vous ne pouvez pas commenter votre propre commerce.")

        commentaire = Commentaire(
            commerce_id=commerce_id,
            auteur_id=user_id,
            contenu=data["contenu"],
        )
        db.session.add(commentaire)

        stats = CommerceStats.query.filter_by(commerce_id=commerce_id).first()
        if not stats:
            stats = CommerceStats(commerce_id=commerce_id)
            db.session.add(stats)
        stats.nb_commentaires = (stats.nb_commentaires or 0) + 1

        db.session.commit()

        try:
            from app.services.ai_service import analyze_and_update_rating
            analyze_and_update_rating(commerce_id)
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(f"[AI] Rating update failed: {e}")

        return commentaire.to_dict()

    def list_commentaires(self, commerce_id):
        commerce = Commerce.query.get(commerce_id)
        if not commerce:
            raise ValueError("Commerce introuvable.")

        commentaires = (
            Commentaire.query
            .filter_by(commerce_id=commerce_id, is_visible=True)
            .order_by(Commentaire.created_at.desc())
            .all()
        )

        result = []
        for c in commentaires:
            auteur = User.query.get(c.auteur_id)
            result.append({
                "id": c.id,
                "contenu": c.contenu,
                "created_at": c.created_at.isoformat() if c.created_at else None,
                "auteur": {
                    "id": auteur.id,
                    "first_name": auteur.first_name,
                    "last_name": auteur.last_name,
                } if auteur else None,
            })

        return {
            "commentaires": result,
            "nb_commentaires": len(result),
        }

    def delete_commentaire(self, user_id, commentaire_id):
        commentaire = Commentaire.query.get(commentaire_id)
        if not commentaire:
            raise ValueError("Commentaire introuvable.")
        if commentaire.auteur_id != user_id:
            raise ValueError("Acces refuse.")

        commerce_id = commentaire.commerce_id
        commentaire.delete()

        stats = CommerceStats.query.filter_by(commerce_id=commerce_id).first()
        if stats and stats.nb_commentaires > 0:
            stats.nb_commentaires -= 1
            stats.save()

        try:
            from app.services.ai_service import analyze_and_update_rating
            analyze_and_update_rating(commerce_id)
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(f"[AI] Rating update failed: {e}")

        return {"message": "Commentaire supprime."}

    def switch_commerce(self, user_id, commerce_id):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("Utilisateur introuvable.")

        commerce = Commerce.query.get(commerce_id)
        if not commerce:
            raise ValueError("Commerce introuvable.")
        if commerce.user_id != user_id:
            raise ValueError("Acces refuse.")

        user.active_commerce_id = commerce.id
        user.save()

        return {
            "message": f"Commerce '{commerce.nom_commercial}' active.",
            "active_commerce_id": commerce.id,
        }

    def get_commerces_cards(self, user_id):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("Utilisateur introuvable.")

        commerces = Commerce.query.filter_by(user_id=user_id).all()
        if not commerces:
            return {"cards": []}

        active_id = user.active_commerce_id
        cards = []
        for c in commerces:
            if c.id == active_id:
                continue

            photo = CommercePhoto.query.filter_by(
                commerce_id=c.id, is_principale=True
            ).first()
            if not photo:
                photo = CommercePhoto.query.filter_by(
                    commerce_id=c.id
                ).order_by(CommercePhoto.ordre.asc()).first()

            share_url = None
            if c.is_active:
                share_url = _build_whatsapp_geo_url(
                    c.nom_commercial,
                    c.latitude,
                    c.longitude,
                )

            cards.append({
                "id": c.id,
                "nom_commercial": c.nom_commercial,
                "description": (c.description or "")[:80],
                "first_image_url": photo.url if photo else None,
                "is_active": c.is_active,
                "is_active_commerce": c.id == user.active_commerce_id,
                "share_url": share_url,
                "step": _get_step(c),
            })

        return {"cards": cards}


def _build_whatsapp_geo_url(commerce_name, latitude, longitude):
    if latitude is None or longitude is None:
        return None

    maps_link = f"https://maps.google.com/?q={latitude},{longitude}"
    message = f"Voici la localisation de {commerce_name} sur Google Maps :\n{maps_link}"
    encoded = quote(message)
    return f"https://wa.me/?text={encoded}"
