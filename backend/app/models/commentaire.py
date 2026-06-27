from ..extensions import db
from .base import BaseModel


class Commentaire(BaseModel):
    __tablename__ = "commentaires"

    commerce_id = db.Column(db.Integer, db.ForeignKey("commerces.id"), nullable=False)
    auteur_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    is_visible = db.Column(db.Boolean, default=True, nullable=False)
    is_moderated = db.Column(db.Boolean, default=False, nullable=False)
    moderated_at = db.Column(db.DateTime, nullable=True)
    moderated_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    commerce = db.relationship("Commerce", back_populates="commentaires")
    auteur = db.relationship("User", back_populates="commentaires_ecrits", foreign_keys=[auteur_id])
    moderateur = db.relationship("User", back_populates="commentaires_moderes", foreign_keys=[moderated_by])

    def to_dict(self):
        return {
            "id": self.id,
            "commerce_id": self.commerce_id,
            "auteur_id": self.auteur_id,
            "contenu": self.contenu,
            "is_visible": self.is_visible,
            "is_moderated": self.is_moderated,
            "moderated_at": self.moderated_at.isoformat() if self.moderated_at else None,
            "moderated_by": self.moderated_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
