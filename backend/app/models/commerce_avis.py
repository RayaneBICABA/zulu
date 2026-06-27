from ..extensions import db
from .base import BaseModel


class CommerceAvis(BaseModel):
    __tablename__ = "commerce_avis"

    commerce_id = db.Column(db.Integer, db.ForeignKey("commerces.id"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    note = db.Column(db.Integer, nullable=False)
    commentaire = db.Column(db.Text, nullable=True)

    commerce = db.relationship("Commerce", backref=db.backref("avis", lazy="selectin", cascade="all, delete-orphan"))
    user = db.relationship("User", backref=db.backref("avis_commerces", lazy="selectin", cascade="all, delete-orphan"))

    __table_args__ = (
        db.UniqueConstraint("user_id", "commerce_id", name="uq_avis_user_commerce"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "commerce_id": self.commerce_id,
            "user_id": self.user_id,
            "note": self.note,
            "commentaire": self.commentaire,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
