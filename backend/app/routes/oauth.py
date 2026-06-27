from flask import Blueprint, request, jsonify, redirect, current_app
from ..services.oauth_service import oauth, OAuthService
from ..extensions import limiter

oauth_bp = Blueprint("oauth", __name__)
oauth_service = OAuthService()


def _is_google_configured():
    return bool(current_app.config.get("GOOGLE_CLIENT_ID") and current_app.config.get("GOOGLE_CLIENT_SECRET"))


@oauth_bp.route("/auth/google/login", methods=["GET"])
def google_login():
    """
    Rediriger vers Google pour l'authentification.
    ---
    tags:
      - OAuth
    responses:
      302:
        description: Redirection vers Google
    """
    if not _is_google_configured():
        return jsonify({"error": "Google OAuth non configure."}), 501

    redirect_uri = f"{request.host_url}api/auth/google/callback"
    return oauth.google.authorize_redirect(redirect_uri)


@oauth_bp.route("/auth/google/callback", methods=["GET"])
@limiter.limit("5 per minute")
def google_callback():
    """
    Callback apres authentification Google.
    ---
    tags:
      - OAuth
    responses:
      200:
        description: Authentification reussie
      401:
        description: Erreur d'authentification
    """
    if not _is_google_configured():
        return jsonify({"error": "Google OAuth non configure."}), 501

    try:
        token = oauth.google.authorize_access_token()
        userinfo = oauth.google.parse_id_token(token)
        result = oauth_service.google_login(userinfo)
        frontend_url = current_app.config.get("FRONTEND_URL", "http://localhost:5173")
        redirect_url = (
            f"{frontend_url}/auth/google/callback"
            f"?access_token={result['access_token']}"
            f"&refresh_token={result['refresh_token']}"
        )
        return redirect(redirect_url)
    except Exception as e:
        frontend_url = current_app.config.get("FRONTEND_URL", "http://localhost:5173")
        return redirect(f"{frontend_url}/login?error=google_auth_failed")
