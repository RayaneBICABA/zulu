from ..base import BaseModel
from ...extensions import db


class Business(BaseModel):
    """
    Représente un commerce enregistré sur la plateforme Zulu.
    """

    __tablename__ = "businesses"

    # ------------------------------------------------------------------
    # Informations générales
    # ------------------------------------------------------------------

    business_name = db.Column(
        db.String(150),
        nullable=False,
        index=True
    )

    slug = db.Column(
        db.String(180),
        nullable=False,
        unique=True,
        index=True
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    whatsapp = db.Column(
        db.String(20),
        nullable=False
    )

    address_description = db.Column(
        db.String(255),
        nullable=False
    )

    # ------------------------------------------------------------------
    # Localisation
    # ------------------------------------------------------------------

    latitude = db.Column(
        db.Float,
        nullable=False
    )

    longitude = db.Column(
        db.Float,
        nullable=False
    )

    # Rayon de visibilité (mètres)
    service_radius = db.Column(
        db.Integer,
        default=5000,
        nullable=False
    )

    # ------------------------------------------------------------------
    # Etat du commerce
    # ------------------------------------------------------------------

    status = db.Column(
        db.String(20),
        default="pending",
        nullable=False,
        index=True
    )
    """
    pending
    approved
    rejected
    suspended
    """

    is_visible = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    is_featured = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    is_verified = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    average_rating = db.Column(
        db.Float,
        default=0,
        nullable=False
    )

    total_reviews = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    total_views = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    total_calls = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    # ------------------------------------------------------------------
    # Relations
    # ------------------------------------------------------------------

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False,
        index=True
    )

    owner = db.relationship(
        "User",
        backref=db.backref(
            "businesses",
            lazy="dynamic",
            cascade="all, delete-orphan"
        )
    )

    category = db.relationship(
        "Category",
        backref=db.backref(
            "businesses",
            lazy="dynamic"
        )
    )

    photos = db.relationship(
        "BusinessPhoto",
        back_populates="business",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    hours = db.relationship(
        "BusinessHour",
        back_populates="business",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    def __repr__(self):
        return f"<Business {self.business_name}>"

    @property
    def is_open(self):
        """
        Calculé à partir des horaires.
        """
        return None

    def increment_views(self):
        self.total_views += 1

    def increment_calls(self):
        self.total_calls += 1

    def to_dict(self):
        return {
            "id": self.id,
            "business_name": self.business_name,
            "slug": self.slug,
            "description": self.description,
            "whatsapp": self.whatsapp,
            "address_description": self.address_description,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "service_radius": self.service_radius,
            "status": self.status,
            "is_visible": self.is_visible,
            "is_featured": self.is_featured,
            "is_verified": self.is_verified,
            "average_rating": self.average_rating,
            "total_reviews": self.total_reviews,
            "total_views": self.total_views,
            "total_calls": self.total_calls,
            "owner_id": self.owner_id,
            "category_id": self.category_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }