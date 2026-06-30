from flask import Blueprint, jsonify
import os
import json

auth_mobile_bp = Blueprint('auth_mobile', __name__)

PAGE = os.path.join(os.path.dirname(__file__), '..', 'templates', 'google_mobile_signin.html')

@auth_mobile_bp.route('/auth/google/mobile')
def google_mobile_signin():
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
button { display: flex; align-items: center; justify-content: center; gap: 10px; width: 100%; padding: 12px 20px; border: 1px solid #ddd; border-radius: 8px; background: white; font-size: 15px; cursor: pointer; }
button:hover { background: #f9f9f9; }
.loading { display: none; margin-top: 20px; color: #666; font-size: 14px; }
.error { display: none; margin-top: 16px; color: #e74c3c; font-size: 13px; padding: 10px; background: #fdf0ef; border-radius: 8px; }
</style>
</head>
<body>
<div class="card">
  <h1>ZAWANI</h1>
  <p>Connectez-vous avec Google</p>
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

// On vérifie si on revient d'une redirection Firebase
auth.getRedirectResult().then(function(result) {
  if (result.user) {
    document.getElementById('googleBtn').style.display = 'none';
    document.getElementById('loading').style.display = 'block';
    document.getElementById('loading').textContent = 'Authentification reussie, retour a l\\'application...';
    return result.user.getIdToken().then(function(idToken) {
      window.location.href = 'zawani://auth?token=' + encodeURIComponent(idToken);
    });
  }
  // Pas de résultat de redirect = premier chargement, on attend le clic
}).catch(function(err) {
  if (err.code !== 'auth/popup-closed-by-user') {
    document.getElementById('error').textContent = 'Erreur: ' + err.message;
    document.getElementById('error').style.display = 'block';
  }
});

document.getElementById('googleBtn').onclick = function() {
  document.getElementById('googleBtn').style.display = 'none';
  document.getElementById('loading').style.display = 'block';
  var provider = new firebase.auth.GoogleAuthProvider();
  // signInWithRedirect (pas popup) — reste dans le Chrome Custom Tab
  auth.signInWithRedirect(provider);
};
</script>
</body>
</html>'''
    return html, 200, {'Content-Type': 'text/html; charset=utf-8'}