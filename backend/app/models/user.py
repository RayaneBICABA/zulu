from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    firebase_uid = db.Column(db.String(255), unique=True, nullable=True, index=True)
    password_hash = db.Column(db.String(255), nullable=True)
    first_name = db.Column(db.String(150), nullable=True)
    last_name = db.Column(db.String(150), nullable=True)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    active_commerce_id = db.Column(db.Integer, db.ForeignKey("commerces.id"), nullable=True)

    roles = db.relationship("Role", secondary="user_roles", back_populates="users", lazy="selectin")
    active_commerce = db.relationship("Commerce", foreign_keys=[active_commerce_id], post_update=True)
    favoris = db.relationship("Favori", back_populates="user", lazy="selectin", cascade="all, delete-orphan")
    vues_emises = db.relationship("VueProfile", back_populates="user", lazy="selectin")
    commentaires_ecrits = db.relationship("Commentaire", back_populates="auteur", lazy="selectin", foreign_keys="[Commentaire.auteur_id]")
    commentaires_moderes = db.relationship("Commentaire", back_populates="moderateur", lazy="selectin", foreign_keys="[Commentaire.moderated_by]")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles)

    def has_permission(self, permission_codename):
        return any(
            perm.codename == permission_codename
            for role in self.roles
            for perm in role.permissions
        )

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_verified": self.is_verified,
            "is_active": self.is_active,
            "active_commerce_id": self.active_commerce_id,
            "roles": [r.name for r in self.roles],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
