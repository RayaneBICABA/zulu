from flask import current_app
from authlib.integrations.flask_client import OAuth
from ..extensions import db
from ..models.user import User
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta

oauth = OAuth()


def init_oauth(app):
    oauth.init_app(app)
    google_client_id = app.config.get("GOOGLE_CLIENT_ID")
    google_client_secret = app.config.get("GOOGLE_CLIENT_SECRET")
    if google_client_id and google_client_secret:
        oauth.register(
            name="google",
            client_id=google_client_id,
            client_secret=google_client_secret,
            server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
            client_kwargs={"scope": "openid email profile"},
        )


class OAuthService:
    def google_login(self, userinfo):
        email = userinfo.get("email")
        if not email:
            raise ValueError("Email non fourni par Google.")

        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(
                email=email,
                first_name=userinfo.get("given_name"),
                last_name=userinfo.get("family_name"),
                is_verified=True,
            )
            user.set_password(email)
            user.save()

        if not user.is_active:
            raise ValueError("Ce compte est desactive.")

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"email": user.email, "is_verified": user.is_verified},
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
