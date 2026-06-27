from ..extensions import db, jwt
from ..models.user import User
from ..models.role import Role
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta
from .email_service import (
    generate_verification_token,
    confirm_verification_token,
    generate_reset_token,
    confirm_reset_token,
    send_verification_email,
    send_reset_password_email,
)
from flask import current_app


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

        client_role = Role.query.filter_by(name="client").first()
        if client_role:
            user.roles.append(client_role)
            user.save()

        token = generate_verification_token(email)
        try:
            send_verification_email(email, token)
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(f"Email verification failed for {email}: {e}")
        return user

    def verify_email(self, token):
        email = confirm_verification_token(token)
        if not email:
            raise ValueError("Token invalide ou expire.")

        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValueError("Utilisateur introuvable.")

        if user.is_verified:
            raise ValueError("Email deja verifie.")

        user.is_verified = True
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
            additional_claims={
                "email": user.email,
                "is_verified": user.is_verified,
                "roles": [r.name for r in user.roles],
            },
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
            additional_claims={
                "email": user.email,
                "is_verified": user.is_verified,
                "roles": [r.name for r in user.roles],
            },
            expires_delta=timedelta(minutes=15),
        )
        return {"access_token": access_token}

    def me(self, user_id):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("Utilisateur introuvable.")
        return user.to_dict()

    def forgot_password(self, email):
        user = User.query.filter_by(email=email).first()
        if not user:
            return

        token = generate_reset_token(email)
        send_reset_password_email(email, token)

    def reset_password(self, token, new_password):
        email = confirm_reset_token(token)
        if not email:
            raise ValueError("Token invalide ou expire.")

        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValueError("Utilisateur introuvable.")

        user.set_password(new_password)
        user.save()
        return user
