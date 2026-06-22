from ..extensions import db, jwt
from ..models.user import User
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta


class AuthService:
    def register(self, email, password, first_name=None, last_name=None):
        if User.query.filter_by(email=email).first():
            raise ValueError("Un compte avec cet email existe deja.")

        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save()
        return user

    def login(self, email, password):
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            raise ValueError("Email ou mot de passe incorrect.")

        if not user.is_active:
            raise ValueError("Ce compte est desactive.")

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"email": user.email},
            expires_delta=timedelta(minutes=15),
        )
        refresh_token = create_refresh_token(
            identity=str(user.id),
            expires_delta=timedelta(days=7),
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user.to_dict(),
        }

    def refresh(self, identity):
        user = User.query.get(int(identity))
        if not user or not user.is_active:
            raise ValueError("Utilisateur introuvable ou desactive.")

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"email": user.email},
            expires_delta=timedelta(minutes=15),
        )
        return {"access_token": access_token}

    def me(self, user_id):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("Utilisateur introuvable.")
        return user.to_dict()
