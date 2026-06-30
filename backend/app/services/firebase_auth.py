import os
import json
import logging
import urllib.request
import firebase_admin
from firebase_admin import credentials, auth
from flask import current_app
logger = logging.getLogger(__name__)
_firebase_app = None

def init_firebase(app):
    global _firebase_app
    if _firebase_app:
        return

    cred_json = os.environ.get('FIREBASE_CREDENTIALS_JSON')
    if cred_json:
        cred_dict = json.loads(cred_json)
        cred = credentials.Certificate(cred_dict)
    else:
        key_path = os.path.join(app.root_path, '..', 'serviceAccountKey.json')
        if not os.path.exists(key_path):
            logger.warning("Firebase credentials not found (neither env var nor file) — Firebase Admin disabled")
            return
        cred = credentials.Certificate(key_path)

    _firebase_app = firebase_admin.initialize_app(cred)
    logger.info("Firebase Admin initialized")

def _verify_google_token(token):
    """Vérifier un Google ID token via l'endpoint tokeninfo de Google."""
    try:
        url = f"https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={token}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        # Vérifier l'audience (notre client OAuth)
        expected_aud = current_app.config.get("GOOGLE_CLIENT_ID")
        if expected_aud and data.get('aud') != expected_aud:
            logger.error(f"Google token audience mismatch: {data.get('aud')}")
            return None
        # Normaliser les champs : sub -> uid (comme Firebase Admin le fait)
        data['uid'] = data.get('sub')
        return data
    except Exception as e:
        logger.error(f"Google token verification failed: {e}")
        return None

def verify_token(token):
    # 1) Essayer Firebase Admin d'abord
    if _firebase_app:
        try:
            decoded = auth.verify_id_token(token)
            return decoded
        except Exception as e:
            logger.warning(f"Firebase verify_id_token failed, trying Google fallback: {e}")
    else:
        logger.warning("Firebase Admin not initialized, trying Google verification only")

    # 2) Fallback : vérifier comme Google ID token
    return _verify_google_token(token)

def get_user_by_firebase_uid(firebase_uid):
    try:
        return auth.get_user(firebase_uid)
    except Exception as e:
        logger.error(f"Firebase get_user failed: {e}")
        return None

def create_custom_token(uid):
    if not _firebase_app:
        logger.error("Firebase Admin not initialized — cannot create custom token")
        return None
    try:
        return auth.create_custom_token(uid).decode()
    except Exception as e:
        logger.error(f"Firebase create_custom_token failed: {e}")
        return None