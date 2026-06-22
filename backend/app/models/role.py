from ..extensions import db
from .base import BaseModel


user_roles = db.Table(
    "user_roles",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
)

role_permissions = db.Table(
    "role_permissions",
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
    db.Column("permission_id", db.Integer, db.ForeignKey("permissions.id"), primary_key=True),
)


class Role(BaseModel):
    __tablename__ = "roles"

    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    users = db.relationship("User", secondary=user_roles, back_populates="roles")
    permissions = db.relationship("Permission", secondary=role_permissions, back_populates="roles")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "permissions": [p.to_dict() for p in self.permissions],
        }


class Permission(BaseModel):
    __tablename__ = "permissions"

    codename = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    roles = db.relationship("Role", secondary=role_permissions, back_populates="permissions")

    def to_dict(self):
        return {
            "id": self.id,
            "codename": self.codename,
            "name": self.name,
        }
