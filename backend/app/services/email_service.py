import logging
from flask import current_app
from itsdangerous import URLSafeTimedSerializer

logger = logging.getLogger(__name__)


def _get_serializer(salt):
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt=salt)


def generate_verification_token(email):
    return _get_serializer("email-verify").dumps(email)


def confirm_verification_token(token, expiration=86400):
    try:
        return _get_serializer("email-verify").loads(token, max_age=expiration)
    except Exception:
        return None


def generate_reset_token(email):
    return _get_serializer("password-reset").dumps(email)


def confirm_reset_token(token, expiration=3600):
    try:
        return _get_serializer("password-reset").loads(token, max_age=expiration)
    except Exception:
        return None


def send_email(to, subject, body):
    logger.info(f"[EMAIL] To: {to} | Subject: {subject}")
    logger.info(f"[EMAIL] Body: {body}")
