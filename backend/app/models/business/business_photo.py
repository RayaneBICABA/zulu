from ..base import BaseModel
from ...extensions import db


class BusinessPhoto(BaseModel):
    """
    Stocke les chemins ou URLs des images illustrant le local de l'artisan.
    """

    __tablename__ = "business_photos"

    # ------------------------------------------------------------------
    # Informations générales
    # ------------------------------------------------------------------

    image_url = db.Column(
        db.String(500), 
        nullable=False
    )
    
    # Photo principale à afficher sur la carte de l'annuaire
    is_primary = db.Column(
        db.Boolean, 
        default=False, 
        nullable=False
    )
    
    # Ordre d'affichage (ex: 0, 1, 2 pour trier les 3 photos)
    sort_order = db.Column(
        db.Integer, 
        default=0, 
        nullable=False
    )

    # ------------------------------------------------------------------
    # Relations
    # ------------------------------------------------------------------

    business_id = db.Column(
        db.Integer, 
        db.ForeignKey("businesses.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )
    
    business = db.relationship(
        "Business", 
        back_populates="photos"
    )

    def __repr__(self):
        return f"<BusinessPhoto {self.id} for Business {self.business_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "is_primary": self.is_primary,
            "sort_order": self.sort_order,
            "business_id": self.business_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }