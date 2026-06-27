from datetime import datetime, timezone
from math import asin, cos, radians, sin, sqrt
from urllib.parse import quote, urlencode
from ..extensions import db
from ..models.commerce import Commerce
from ..models.commerce_avis import CommerceAvis
from ..models.user import User


EARTH_RADIUS_KM = 6371.0
JOURS_ORDRE = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


class CommerceDetailService:

    def get_detail(self, commerce_id, data=None, user_id=None):
        data = data or {}
        commerce = Commerce.query.get(commerce_id)
        if not commerce:
            raise ValueError("Commerce introuvable.")
        if not commerce.is_active:
            raise ValueError("Commerce indisponible.")

        client_latitude = data.get("latitude")
        client_longitude = data.get("longitude")
        avis = CommerceAvis.query.filter_by(commerce_id=commerce.id).order_by(CommerceAvis.created_at.desc()).all()

        return {
            "id": commerce.id,
            "nom_commercial": commerce.nom_commercial,
            "categorie": commerce.categorie.to_dict() if commerce.categorie else None,
            "quartier": _extract_quartier(commerce.adresse_complete),
            "description": commerce.description,
            "couverture": _build_couverture(commerce),
            "produit_images": _build_produit_images(commerce),
            "note_moyenne": _get_note_moyenne(avis),
            "nombre_avis": len(avis),
            "contacts": _build_contacts(commerce, client_latitude, client_longitude),
            "localisation": _build_localisation(commerce, client_latitude, client_longitude),
            "horaires": _build_horaires(commerce),
            "derniers_avis": [_build_avis_item(a) for a in avis[:3]],
            "peut_laisser_avis": _can_leave_avis(user_id, commerce.id),
        }

    def create_avis(self, commerce_id, user_id, data):
        commerce = Commerce.query.get(commerce_id)
        if not commerce:
            raise ValueError("Commerce introuvable.")
        if not commerce.is_active:
            raise ValueError("Commerce indisponible.")

        user = User.query.get(user_id)
        if not user:
            raise ValueError("Utilisateur introuvable.")
        if not _is_citoyen(user):
            raise ValueError("Seuls les citoyens connectes peuvent laisser un avis.")
        if commerce.user_id == user.id:
            raise ValueError("Vous ne pouvez pas noter votre propre commerce.")

        existing = CommerceAvis.query.filter_by(commerce_id=commerce.id, user_id=user.id).first()
        if existing:
            raise ValueError("Vous avez deja laisse un avis pour ce commerce.")

        avis = CommerceAvis(
            commerce_id=commerce.id,
            user_id=user.id,
            note=data["note"],
            commentaire=data.get("commentaire"),
        )
        db.session.add(avis)
        db.session.commit()
        return _build_avis_item(avis)


def _build_couverture(commerce):
    photos = sorted(commerce.photos, key=lambda p: (not p.is_principale, p.ordre))
    photo = photos[0] if photos else None
    return {
        "url": photo.url if photo else None,
        "alt_text": photo.alt_text if photo else None,
        "initiales": _get_initiales(commerce.nom_commercial),
    }


def _build_produit_images(commerce):
    return [
        {
            "id": image.id,
            "url": image.url,
            "ordre": image.ordre,
        }
        for image in sorted(commerce.produit_images, key=lambda img: img.ordre)
    ]


def _build_contacts(commerce, client_latitude=None, client_longitude=None):
    return {
        "telephone": commerce.contact_telephonique,
        "appel_url": f"tel:{commerce.contact_telephonique}" if commerce.contact_telephonique else None,
        "whatsapp_numero": commerce.whatsapp_numero,
        "whatsapp_url": _build_whatsapp_url(commerce.whatsapp_numero, commerce.nom_commercial),
        "itineraire_url": _build_itineraire_url(
            commerce.latitude,
            commerce.longitude,
            client_latitude,
            client_longitude,
        ),
    }


def _build_localisation(commerce, client_latitude=None, client_longitude=None):
    distance_km = None
    if (
        client_latitude is not None
        and client_longitude is not None
        and commerce.latitude is not None
        and commerce.longitude is not None
    ):
        distance_km = round(_distance_km(
            client_latitude,
            client_longitude,
            float(commerce.latitude),
            float(commerce.longitude),
        ), 2)

    return {
        "adresse_complete": commerce.adresse_complete,
        "quartier": _extract_quartier(commerce.adresse_complete),
        "latitude": float(commerce.latitude) if commerce.latitude else None,
        "longitude": float(commerce.longitude) if commerce.longitude else None,
        "distance_km": distance_km,
    }


def _build_horaires(commerce):
    now = datetime.now()
    current_day = JOURS_ORDRE[now.weekday()]
    horaires = sorted(commerce.horaires, key=lambda h: JOURS_ORDRE.index(h.jour.value))
    today = next((h for h in horaires if h.jour.value == current_day), None)

    return {
        "statut": _get_statut_ouverture(today, now),
        "jour_actuel": current_day,
        "items": [h.to_dict() for h in horaires],
    }


def _get_statut_ouverture(horaire, now):
    if not horaire or horaire.est_ferme:
        return {"is_open": False, "label": "Ferme"}
    if horaire.est_24h:
        return {"is_open": True, "label": "Ouvert 24h/24"}
    if not horaire.heure_ouverture or not horaire.heure_fermeture:
        return {"is_open": False, "label": "Horaires indisponibles"}

    current_time = now.time()
    is_open = horaire.heure_ouverture <= current_time <= horaire.heure_fermeture
    label = "Ouvert" if is_open else "Ferme"
    return {
        "is_open": is_open,
        "label": label,
        "heure_ouverture": horaire.heure_ouverture.isoformat(),
        "heure_fermeture": horaire.heure_fermeture.isoformat(),
    }


def _build_avis_item(avis):
    user = avis.user
    auteur = "Utilisateur"
    if user:
        full_name = " ".join([name for name in [user.first_name, user.last_name] if name])
        auteur = full_name or user.email.split("@")[0]

    return {
        "id": avis.id,
        "commerce_id": avis.commerce_id,
        "user_id": avis.user_id,
        "auteur": auteur,
        "note": avis.note,
        "commentaire": avis.commentaire,
        "date_relative": _date_relative(avis.created_at),
        "created_at": avis.created_at.isoformat() if avis.created_at else None,
    }


def _can_leave_avis(user_id, commerce_id):
    if not user_id:
        return False
    user = User.query.get(user_id)
    if not user or not _is_citoyen(user):
        return False
    commerce = Commerce.query.get(commerce_id)
    if commerce and commerce.user_id == user.id:
        return False
    return CommerceAvis.query.filter_by(commerce_id=commerce_id, user_id=user.id).first() is None


def _is_citoyen(user):
    role_names = {role.name.lower() for role in user.roles}
    return user.is_active and ("client" in role_names or "citizen" in role_names) and "artisan" not in role_names and "admin" not in role_names


def _get_note_moyenne(avis):
    if not avis:
        return 0
    return round(sum(a.note for a in avis) / len(avis), 1)


def _get_initiales(name):
    parts = [part for part in (name or "").strip().split(" ") if part]
    if not parts:
        return "?"
    return "".join(part[0].upper() for part in parts[:2])


def _extract_quartier(adresse):
    if not adresse:
        return None
    parts = [part.strip() for part in adresse.split(",") if part.strip()]
    if len(parts) >= 2:
        return parts[-1]
    return parts[0] if parts else None


def _build_whatsapp_url(phone, commerce_name):
    if not phone:
        return None
    message = quote(f"Bonjour, je viens de Zulu et je souhaite avoir des informations sur {commerce_name}.")
    return f"https://wa.me/{phone}?text={message}"


def _build_itineraire_url(destination_lat, destination_lon, origin_lat=None, origin_lon=None):
    if destination_lat is None or destination_lon is None:
        return None

    params = {
        "api": "1",
        "destination": f"{float(destination_lat)},{float(destination_lon)}",
        "travelmode": "driving",
    }
    if origin_lat is not None and origin_lon is not None:
        params["origin"] = f"{origin_lat},{origin_lon}"

    return f"https://www.google.com/maps/dir/?{urlencode(params)}"


def _distance_km(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return EARTH_RADIUS_KM * c


def _date_relative(date):
    if not date:
        return None

    now = datetime.now(timezone.utc)
    if date.tzinfo is None:
        date = date.replace(tzinfo=timezone.utc)

    delta = now - date
    if delta.days >= 365:
        years = delta.days // 365
        return f"il y a {years} an" if years == 1 else f"il y a {years} ans"
    if delta.days >= 30:
        months = delta.days // 30
        return f"il y a {months} mois"
    if delta.days >= 1:
        return "hier" if delta.days == 1 else f"il y a {delta.days} jours"

    hours = delta.seconds // 3600
    if hours >= 1:
        return f"il y a {hours} heure" if hours == 1 else f"il y a {hours} heures"

    minutes = delta.seconds // 60
    if minutes >= 1:
        return f"il y a {minutes} minute" if minutes == 1 else f"il y a {minutes} minutes"

    return "a l'instant"
