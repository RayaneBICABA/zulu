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

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    nom_commercial = db.Column(db.String(200), nullable=False)
    whatsapp_numero = db.Column(db.String(20), nullable=True)
    contact_telephonique = db.Column(db.String(20), nullable=True)
    categorie_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    description = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Numeric(9, 6), nullable=True)
    longitude = db.Column(db.Numeric(9, 6), nullable=True)
    adresse_complete = db.Column(db.String(500), nullable=True)
    is_vendeur_produits = db.Column(db.Boolean, default=False, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=False, nullable=False)

    user = db.relationship("User", foreign_keys=[user_id], backref=db.backref("commerces", lazy="selectin"))
    categorie = db.relationship("Categorie", backref=db.backref("commerces", lazy="selectin"))
    photos = db.relationship("CommercePhoto", backref="commerce", lazy="selectin", cascade="all, delete-orphan")
    horaires = db.relationship("HoraireOuverture", backref="commerce", lazy="selectin", cascade="all, delete-orphan")
    stats = db.relationship("CommerceStats", backref="commerce", uselist=False, lazy="selectin", cascade="all, delete-orphan")
    favoris_recus = db.relationship("Favori", back_populates="commerce", lazy="selectin", cascade="all, delete-orphan")
    vues_recues = db.relationship("VueProfile", back_populates="commerce", lazy="selectin", cascade="all, delete-orphan")
    produit_images = db.relationship("ProduitImage", backref="commerce", lazy="selectin", cascade="all, delete-orphan")
    commentaires = db.relationship("Commentaire", back_populates="commerce", lazy="selectin", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "nom_commercial": self.nom_commercial,
            "whatsapp_numero": self.whatsapp_numero,
            "contact_telephonique": self.contact_telephonique,
            "categorie_id": self.categorie_id,
            "categorie": self.categorie.to_dict() if self.categorie else None,
            "description": self.description,
            "latitude": float(self.latitude) if self.latitude else None,
            "longitude": float(self.longitude) if self.longitude else None,
            "adresse_complete": self.adresse_complete,
            "is_vendeur_produits": self.is_vendeur_produits,
            "is_verified": self.is_verified,
            "is_active": self.is_active,
            "photos": [p.to_dict() for p in self.photos],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class CommerceStats(BaseModel):
    __tablename__ = "commerce_stats"

    commerce_id = db.Column(db.Integer, db.ForeignKey("commerces.id"), unique=True, nullable=False)
    nb_vues_profile = db.Column(db.Integer, default=0, nullable=False)
    nb_favoris = db.Column(db.Integer, default=0, nullable=False)
    nb_commentaires = db.Column(db.Integer, default=0, nullable=False)
    last_vue_at = db.Column(db.DateTime, nullable=True)
    average_rating = db.Column(db.Numeric(3, 2), default=0.00, nullable=False)
    rating_count = db.Column(db.Integer, default=0, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "commerce_id": self.commerce_id,
            "nb_vues_profile": self.nb_vues_profile,
            "nb_favoris": self.nb_favoris,
            "nb_commentaires": self.nb_commentaires,
            "last_vue_at": self.last_vue_at.isoformat() if self.last_vue_at else None,
            "average_rating": float(self.average_rating) if self.average_rating else 0.0,
            "rating_count": self.rating_count,
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


class Favori(BaseModel):
    __tablename__ = "favoris"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    commerce_id = db.Column(db.Integer, db.ForeignKey("commerces.id"), nullable=False)

    user = db.relationship("User", back_populates="favoris")
    commerce = db.relationship("Commerce", back_populates="favoris_recus")

    __table_args__ = (
        db.UniqueConstraint("user_id", "commerce_id", name="uq_favori_user_commerce"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "commerce_id": self.commerce_id,
        }


class VueProfile(BaseModel):
    __tablename__ = "vues_profile"

    commerce_id = db.Column(db.Integer, db.ForeignKey("commerces.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)
    viewed_at = db.Column(db.DateTime, nullable=False)

    commerce = db.relationship("Commerce", back_populates="vues_recues")
    user = db.relationship("User", back_populates="vues_emises")

    def to_dict(self):
        return {
            "id": self.id,
            "commerce_id": self.commerce_id,
            "user_id": self.user_id,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "viewed_at": self.viewed_at.isoformat() if self.viewed_at else None,
        }


class ProduitImage(BaseModel):
    __tablename__ = "produit_images"

    commerce_id = db.Column(db.Integer, db.ForeignKey("commerces.id"), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    ordre = db.Column(db.Integer, default=0, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "commerce_id": self.commerce_id,
            "url": self.url,
            "ordre": self.ordre,
        }
