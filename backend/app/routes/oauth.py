import logging
from flask import Blueprint, request, jsonify, redirect, current_app
from ..services.oauth_service import oauth, OAuthService
from ..extensions import limiter

logger = logging.getLogger(__name__)

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
    parameters:
      - in: query
        name: mobile
        type: boolean
        description: Si true, redirige vers le deep link zawani://
    responses:
      302:
        description: Redirection vers Google
    """
    if not _is_google_configured():
        return jsonify({"error": "Google OAuth non configure."}), 501

    redirect_uri = current_app.config.get("GOOGLE_REDIRECT_URI")
    if not redirect_uri:
        redirect_uri = f"{request.url_root.rstrip('/')}/api/auth/google/callback"

    is_mobile = request.args.get("mobile") == "1"
    if is_mobile:
        return oauth.google.authorize_redirect(redirect_uri, state="mobile")
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

    frontend_url = current_app.config.get("FRONTEND_URL", "http://localhost:5173")

    try:
        token = oauth.google.authorize_access_token()
        userinfo = oauth.google.parse_id_token(token)
        result = oauth_service.google_login(userinfo)

        is_mobile = request.args.get("state") == "mobile"
        if is_mobile:
            deep_link = (
                f"zawani://auth"
                f"?access_token={result['access_token']}"
                f"&refresh_token={result['refresh_token']}"
            )
            return _deep_link_page(deep_link, frontend_url, result)

        redirect_url = (
            f"{frontend_url}/auth/google/callback"
            f"?access_token={result['access_token']}"
            f"&refresh_token={result['refresh_token']}"
        )
        return redirect(redirect_url)
    except Exception as e:
        logger.exception(f"Google auth callback failed: {e}")
        return redirect(f"{frontend_url}/login?error=google_auth_failed")


def _deep_link_page(deep_link, fallback_url, result):
    access_token = result["access_token"]
    refresh_token = result["refresh_token"]
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Zawani Auth</title></head>
<body style="display:flex;justify-content:center;align-items:center;height:100vh;font-family:sans-serif;background:#fff;">
<script>
(function() {{
  var dl = '{deep_link}';
  var fb = '{fallback_url}/auth/google/callback?access_token={access_token}&refresh_token={refresh_token}';
  window.location.href = dl;
  setTimeout(function() {{ window.location.href = fb; }}, 3000);
}})();
</script>
<p style="color:#666;">Authentification en cours...</p>
</body></html>"""
    from flask import make_response
    resp = make_response(html)
    resp.headers["Content-Type"] = "text/html"
    return resp
