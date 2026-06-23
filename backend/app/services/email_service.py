import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app, render_template
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


def _send_smtp(to, subject, html_body):
    config = current_app.config
    mail_password = config.get("MAIL_PASSWORD", "")

    if not mail_password:
        raise RuntimeError("MAIL_PASSWORD non configure. L'envoi d'email est impossible.")

    msg = MIMEMultipart("alternative")
    msg["From"] = config["MAIL_DEFAULT_SENDER"]
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        server = smtplib.SMTP(config["MAIL_SERVER"], config["MAIL_PORT"], timeout=5)
        if config.get("MAIL_USE_TLS", True):
            server.starttls()
        server.login(config["MAIL_USERNAME"], mail_password)
        server.sendmail(config["MAIL_DEFAULT_SENDER"], to, msg.as_string())
        server.quit()
        logger.info(f"[EMAIL] Sent to {to}")
    except Exception as e:
        logger.error(f"[EMAIL] Failed to send to {to}: {e}")


def send_verification_email(to, token):
    link = f"{current_app.config['FRONTEND_URL']}/verifier-email?token={token}"
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2>Verifiez votre email</h2>
        <p>Bonjour,</p>
        <p>Cliquez sur le lien ci-dessous pour activer votre compte :</p>
        <p><a href="{link}" style="background: #2563eb; color: #fff; padding: 10px 20px; text-decoration: none; border-radius: 6px; display: inline-block;">Verifier mon email</a></p>
        <p>Ou copiez ce lien dans votre navigateur :</p>
        <p style="word-break: break-all; color: #2563eb;">{link}</p>
        <p>Ce lien expire dans 24 heures.</p>
      </body>
    </html>
    """
    _send_smtp(to, "Zulu — Verification de votre email", html)


def send_reset_password_email(to, token):
    link = f"{current_app.config['FRONTEND_URL']}/reinitialiser-mot-de-passe?token={token}"
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2>Reinitialisation de mot de passe</h2>
        <p>Bonjour,</p>
        <p>Cliquez sur le lien ci-dessous pour reinitialiser votre mot de passe :</p>
        <p><a href="{link}" style="background: #2563eb; color: #fff; padding: 10px 20px; text-decoration: none; border-radius: 6px; display: inline-block;">Reinitialiser mon mot de passe</a></p>
        <p>Ou copiez ce lien dans votre navigateur :</p>
        <p style="word-break: break-all; color: #2563eb;">{link}</p>
        <p>Ce lien expire dans 1 heure. Si vous n'avez pas demande cette reinitialisation, ignorez cet email.</p>
      </body>
    </html>
    """
    _send_smtp(to, "Zulu — Reinitialisation de mot de passe", html)
