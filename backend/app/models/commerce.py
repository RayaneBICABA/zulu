import enum
from ..extensions import db
from .base import BaseModel


class JourSemaine(enum.Enum):
    lundi = "lundi"
    mardi = "mardi"
    mercredi = "mercredi"
    jeudi = "jeudi"
    vendredi = "vendredi"
    samedi = "samedi"
    dimanche = "dimanche"


class Commerce(BaseModel):
    __tablename__ = "commerces"

    nom_commercial = db.Column(db.String(200), nullable=False)
    whatsapp_numero = db.Column(db.String(20), nullable=True)
    contact_telephonique = db.Column(db.String(20), nullable=True)
    categorie_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    description = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Numeric(9, 6), nullable=True)
    longitude = db.Column(db.Numeric(9, 6), nullable=True)
    adresse_complete = db.Column(db.String(500), nullable=True)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    categorie = db.relationship("Categorie", backref=db.backref("commerces", lazy="selectin"))
    photos = db.relationship("CommercePhoto", backref="commerce", lazy="selectin", cascade="all, delete-orphan")
    horaires = db.relationship("HoraireOuverture", backref="commerce", lazy="selectin", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "nom_commercial": self.nom_commercial,
            "whatsapp_numero": self.whatsapp_numero,
            "contact_telephonique": self.contact_telephonique,
            "categorie_id": self.categorie_id,
            "description": self.description,
            "latitude": float(self.latitude) if self.latitude else None,
            "longitude": float(self.longitude) if self.longitude else None,
            "adresse_complete": self.adresse_complete,
            "is_verified": self.is_verified,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class CommercePhoto(BaseModel):
    __tablename__ = "commerce_photos"

    commerce_id = db.Column(db.Integer, db.ForeignKey("commerces.id"), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    alt_text = db.Column(db.String(255), nullable=True)
    ordre = db.Column(db.Integer, default=0, nullable=False)
    is_principale = db.Column(db.Boolean, default=False, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "commerce_id": self.commerce_id,
            "url": self.url,
            "alt_text": self.alt_text,
            "ordre": self.ordre,
            "is_principale": self.is_principale,
        }


class HoraireOuverture(BaseModel):
    __tablename__ = "horaires_ouverture"

    commerce_id = db.Column(db.Integer, db.ForeignKey("commerces.id"), nullable=False)
    jour = db.Column(db.Enum(JourSemaine), nullable=False)
    heure_ouverture = db.Column(db.Time, nullable=True)
    heure_fermeture = db.Column(db.Time, nullable=True)
    est_ferme = db.Column(db.Boolean, default=False, nullable=False)
    est_24h = db.Column(db.Boolean, default=False, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "commerce_id": self.commerce_id,
            "jour": self.jour.value if self.jour else None,
            "heure_ouverture": self.heure_ouverture.isoformat() if self.heure_ouverture else None,
            "heure_fermeture": self.heure_fermeture.isoformat() if self.heure_fermeture else None,
            "est_ferme": self.est_ferme,
            "est_24h": self.est_24h,
        }
