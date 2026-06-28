import os
import json
import logging
import firebase_admin
from firebase_admin import credentials, auth
from flask import current_app

logger = logging.getLogger(__name__)

_firebase_app = None


def init_firebase(app):
    global _firebase_app
    if _firebase_app:
        return

    key_path = os.path.join(app.root_path, '..', 'serviceAccountKey.json')
    if not os.path.exists(key_path):
        logger.warning("serviceAccountKey.json not found — Firebase Admin disabled")
        return

    cred = credentials.Certificate(key_path)
    _firebase_app = firebase_admin.initialize_app(cred)
    logger.info("Firebase Admin initialized")


def verify_token(token):
    try:
        decoded = auth.verify_id_token(token)
        return decoded
    except Exception as e:
        logger.error(f"Firebase token verification failed: {e}")
        return None


def get_user_by_firebase_uid(firebase_uid):
    try:
        return auth.get_user(firebase_uid)
    except Exception as e:
        logger.error(f"Firebase get_user failed: {e}")
        return None
