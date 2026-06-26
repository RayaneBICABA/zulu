from ..extensions import db
from .base import BaseModel


class Categorie(BaseModel):
    __tablename__ = "categories"

    nom = db.Column(db.String(150), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
