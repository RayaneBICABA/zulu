import logging
from flask import current_app
from itsdangerous import URLSafeTimedSerializer

logger = logging.getLogger(__name__)


def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"], salt="email-verify"
    )
    return serializer.dumps(email)


def confirm_verification_token(token, expiration=86400):
    serializer = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"], salt="email-verify"
    )
    try:
        email = serializer.loads(token, max_age=expiration)
        return email
    except Exception:
        return None


def send_email(to, subject, body):
    logger.info(f"[EMAIL] To: {to} | Subject: {subject}")
    logger.info(f"[EMAIL] Body: {body}")
