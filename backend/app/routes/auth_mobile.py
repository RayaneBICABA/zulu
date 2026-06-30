from flask import Blueprint, redirect, request, current_app
import os
import json
import urllib.parse
import urllib.request

from ..services.firebase_auth import verify_token, create_custom_token

auth_mobile_bp = Blueprint('auth_mobile', __name__)


@auth_mobile_bp.route('/auth/google/mobile')
def google_mobile_signin():
    """Redirect direct vers Google OAuth — pas de Firebase dans le navigateur."""
    client_id = current_app.config.get("GOOGLE_CLIENT_ID")

    if not client_id:
        return _firebase_fallback()

    # Construire l'URL de callback
    callback_url = _build_callback_url()

    params = {
        'client_id': client_id,
        'redirect_uri': callback_url,
        'response_type': 'code',
        'scope': 'openid email profile',
        'access_type': 'offline',
        'prompt': 'select_account',
    }

    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)
    return redirect(auth_url)


@auth_mobile_bp.route('/auth/google/mobile/callback')
def google_mobile_callback():
    """Google redirige ici avec un code. On l'échange contre un ID token."""
    code = request.args.get('code')
    error = request.args.get('error')

    if error:
        return _error_page(f"Google erreur: {error}")

    if not code:
        return _error_page("Code d'autorisation manquant.")

    client_id = current_app.config.get("GOOGLE_CLIENT_ID")
    client_secret = current_app.config.get("GOOGLE_CLIENT_SECRET")
    callback_url = _build_callback_url()

    if not client_id or not client_secret:
        return _error_page("Google OAuth non configuré côté serveur.")

    # Échanger le code contre des tokens
    try:
        token_data = urllib.parse.urlencode({
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': callback_url,
            'grant_type': 'authorization_code',
        }).encode()

        req = urllib.request.Request(
            'https://oauth2.googleapis.com/token',
            data=token_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            tokens = json.loads(resp.read().decode())
    except Exception as e:
        return _error_page(f"Erreur token exchange: {e}")

    id_token = tokens.get('id_token')
    if not id_token:
        return _error_page("ID token manquant dans la réponse Google.")

    # Vérifier le token avec Firebase Admin et créer un custom token
    decoded = verify_token(id_token)
    if not decoded:
        return _error_page("Token Google invalide ou non autorisé par Firebase.")

    firebase_uid = decoded.get('uid')
    if not firebase_uid:
        return _error_page("UID Firebase manquant dans le token.")

    custom_token = create_custom_token(firebase_uid)
    if not custom_token:
        return _error_page("Impossible de créer le token d'authentification.")

    # Redirect vers le deep link de l'app avec le custom token Firebase
    deep_link = "zawani://auth?token=" + urllib.parse.quote(custom_token)
    return redirect(deep_link)


def _build_callback_url():
    """Construire l'URL de callback publique."""
    # Utiliser l'URL configurée ou la déduire de la requête
    backend_url = current_app.config.get("BACKEND_URL")
    if backend_url:
        return backend_url.rstrip('/') + "/api/auth/google/mobile/callback"
    return request.scheme + "://" + request.host + "/api/auth/google/mobile/callback"


def _error_page(msg):
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Erreur</title></head>
<body style="display:flex;align-items:center;justify-content:center;min-height:100vh;
font-family:sans-serif;background:#f5f5f5;margin:0;">
<div style="background:#fff;padding:32px;border-radius:16px;text-align:center;
box-shadow:0 2px 12px rgba(0,0,0,0.08);max-width:320px;width:90%;">
<h3 style="color:#e74c3c;margin-bottom:12px;">Erreur</h3>
<p style="color:#666;font-size:14px;margin-bottom:20px;">{msg}</p>
<p style="color:#999;font-size:12px;">Fermez cette fenêtre et réessayez.</p>
</div></body></html>""", 400


def _firebase_fallback():
    """Fallback si Google OAuth n'est pas configuré côté serveur."""
    firebase_config = {
        'apiKey': os.environ.get('FIREBASE_API_KEY', 'AIzaSyBbeyWpC0nEEuZIuK5eONt0LDGYuKm038Q'),
        'authDomain': os.environ.get('FIREBASE_AUTH_DOMAIN', 'zawani-aeba8.firebaseapp.com'),
        'projectId': os.environ.get('FIREBASE_PROJECT_ID', 'zawani-aeba8'),
        'appId': os.environ.get('FIREBASE_APP_ID', '1:720010119224:web:5ec800f4f49883bbb43ecd'),
    }
    html = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Connexion ZAWANI</title>
<script src="https://www.gstatic.com/firebasejs/11.6.0/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/11.6.0/firebase-auth-compat.js"></script>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; display: flex; align-items: center; justify-content: center; min-height: 100vh; background: #f5f5f5; }
.card { background: white; border-radius: 16px; padding: 32px; text-align: center; box-shadow: 0 2px 12px rgba(0,0,0,0.08); width: 320px; }
h1 { font-size: 20px; margin-bottom: 8px; color: #1a1a2e; }
p { font-size: 14px; color: #666; margin-bottom: 24px; }
.warn { color: #e67e22; font-size: 12px; margin-bottom: 16px; background: #fef5e7; padding: 8px; border-radius: 8px; }
button { display: flex; align-items: center; justify-content: center; gap: 10px; width: 100%; padding: 12px 20px; border: 1px solid #ddd; border-radius: 8px; background: white; font-size: 15px; cursor: pointer; }
button:hover { background: #f9f9f9; }
.loading { display: none; margin-top: 20px; color: #666; font-size: 14px; }
.error { display: none; margin-top: 16px; color: #e74c3c; font-size: 12px; padding: 10px; background: #fdf0ef; border-radius: 8px; word-break: break-word; text-align: left; }
</style>
</head>
<body>
<div class="card">
  <h1>ZAWANI</h1>
  <p>Connectez-vous avec Google</p>
  <div class="warn">Mode fallback Firebase (moins fiable sur mobile)</div>
  <button id="googleBtn">
    <svg width="18" height="18" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
    Se connecter avec Google
  </button>
  <div class="loading" id="loading">Connexion en cours...</div>
  <div class="error" id="error"></div>
</div>
<script>
var config = ''' + json.dumps(firebase_config) + ''';
firebase.initializeApp(config);
var auth = firebase.auth();
auth.languageCode = 'fr';

auth.getRedirectResult().then(function(result) {
  if (result.user) {
    document.getElementById('loading').textContent = 'Authentification reussie...';
    return result.user.getIdToken().then(function(idToken) {
      window.location.href = 'zawani://auth?token=' + encodeURIComponent(idToken);
    });
  }
}).catch(function(err) {
  if (err.code !== 'auth/popup-closed-by-user' && err.code !== 'auth/cancelled-popup-request') {
    document.getElementById('error').textContent = 'Erreur: ' + err.message;
    document.getElementById('error').style.display = 'block';
  }
});

document.getElementById('googleBtn').onclick = function() {
  document.getElementById('googleBtn').style.display = 'none';
  document.getElementById('loading').style.display = 'block';
  var provider = new firebase.auth.GoogleAuthProvider();
  auth.signInWithRedirect(provider).catch(function(err) {
    document.getElementById('error').textContent = 'Erreur: ' + err.message;
    document.getElementById('error').style.display = 'block';
    document.getElementById('loading').style.display = 'none';
    document.getElementById('googleBtn').style.display = 'flex';
  });
};
</script>
</body>
</html>'''
    return html, 200, {'Content-Type': 'text/html; charset=utf-8'}