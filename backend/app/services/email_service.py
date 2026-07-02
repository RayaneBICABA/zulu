import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app

logger = logging.getLogger(__name__)

from itsdangerous import URLSafeTimedSerializer


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
        raise


def send_verification_email(to, token):
    link = f"{current_app.config['FRONTEND_URL']}/verifier-email?token={token}"
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin:0;padding:0;background-color:#f7f7f7;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
      <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f7f7f7;padding:40px 20px;">
        <tr>
          <td align="center">
            <table width="100%" cellpadding="0" cellspacing="0" style="max-width:480px;background-color:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,0.06);">

              <tr>
                <td style="padding:40px 32px 24px;text-align:center;">
                  <h1 style="margin:0 0 8px;font-size:28px;font-weight:800;color:#c94301;letter-spacing:-0.5px;">ZAWANI</h1>
                  <p style="margin:0;font-size:13px;color:#999999;">Votre plateforme d'artisans</p>
                </td>
              </tr>

              <tr>
                <td style="padding:0 32px;">
                  <div style="height:1px;background-color:#f0f0f0;"></div>
                </td>
              </tr>

              <tr>
                <td style="padding:32px;">
                  <h2 style="margin:0 0 16px;font-size:20px;font-weight:700;color:#1a1a1a;">Verifiez votre email</h2>
                  <p style="margin:0 0 8px;font-size:15px;color:#555555;line-height:1.6;">
                    Bonjour,
                  </p>
                  <p style="margin:0 0 24px;font-size:15px;color:#555555;line-height:1.6;">
                    Merci pour votre inscription sur Zawani. Cliquez sur le bouton ci-dessous pour activer votre compte :
                  </p>

                  <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                      <td align="center" style="padding:0 0 24px;">
                        <a href="{link}" style="display:inline-block;background-color:#c94301;color:#ffffff;font-size:15px;font-weight:600;text-decoration:none;padding:14px 32px;border-radius:10px;">
                          Verifier mon email
                        </a>
                      </td>
                    </tr>
                  </table>

                  <p style="margin:0 0 8px;font-size:13px;color:#999999;line-height:1.5;">
                    Ou copiez ce lien dans votre navigateur :
                  </p>
                  <p style="margin:0 0 24px;font-size:12px;color:#c94301;word-break:break-all;line-height:1.5;">
                    {link}
                  </p>
                </td>
              </tr>

              <tr>
                <td style="padding:0 32px;">
                  <div style="height:1px;background-color:#f0f0f0;"></div>
                </td>
              </tr>

              <tr>
                <td style="padding:24px 32px 32px;text-align:center;">
                  <p style="margin:0;font-size:12px;color:#bbbbbb;line-height:1.5;">
                    Ce lien expire dans 24 heures.<br>
                    Si vous n'avez pas cree de compte, ignorez cet email.
                  </p>
                </td>
              </tr>

            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """
    _send_smtp(to, "ZAWANI — Verifiez votre email", html)


def send_reset_password_email_sendgrid(to, reset_link):
    import requests

    sg_api_key = current_app.config.get("SENDGRID_API_KEY", "")
    if not sg_api_key:
        raise RuntimeError("SENDGRID_API_KEY non configure. L'envoi d'email est impossible.")

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin:0;padding:0;background-color:#f7f7f7;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
      <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f7f7f7;padding:40px 20px;">
        <tr>
          <td align="center">
            <table width="100%" cellpadding="0" cellspacing="0" style="max-width:480px;background-color:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,0.06);">

              <tr>
                <td style="padding:40px 32px 24px;text-align:center;">
                  <h1 style="margin:0 0 8px;font-size:28px;font-weight:800;color:#c94301;letter-spacing:-0.5px;">ZAWANI</h1>
                  <p style="margin:0;font-size:13px;color:#999999;">Votre plateforme d'artisans</p>
                </td>
              </tr>

              <tr>
                <td style="padding:0 32px;">
                  <div style="height:1px;background-color:#f0f0f0;"></div>
                </td>
              </tr>

              <tr>
                <td style="padding:32px;">
                  <h2 style="margin:0 0 16px;font-size:20px;font-weight:700;color:#1a1a1a;">Reinitialisation de mot de passe</h2>
                  <p style="margin:0 0 8px;font-size:15px;color:#555555;line-height:1.6;">
                    Bonjour,
                  </p>
                  <p style="margin:0 0 24px;font-size:15px;color:#555555;line-height:1.6;">
                    Vous avez demande la reinitialisation de votre mot de passe. Cliquez sur le bouton ci-dessous :
                  </p>

                  <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                      <td align="center" style="padding:0 0 24px;">
                        <a href="{reset_link}" style="display:inline-block;background-color:#c94301;color:#ffffff;font-size:15px;font-weight:600;text-decoration:none;padding:14px 32px;border-radius:10px;">
                          Reinitialiser mon mot de passe
                        </a>
                      </td>
                    </tr>
                  </table>

                  <p style="margin:0 0 8px;font-size:13px;color:#999999;line-height:1.5;">
                    Ou copiez ce lien dans votre navigateur :
                  </p>
                  <p style="margin:0 0 24px;font-size:12px;color:#c94301;word-break:break-all;line-height:1.5;">
                    {reset_link}
                  </p>
                </td>
              </tr>

              <tr>
                <td style="padding:0 32px;">
                  <div style="height:1px;background-color:#f0f0f0;"></div>
                </td>
              </tr>

              <tr>
                <td style="padding:24px 32px 32px;text-align:center;">
                  <p style="margin:0;font-size:12px;color:#bbbbbb;line-height:1.5;">
                    Ce lien expire dans 1 heure.<br>
                    Si vous n'avez pas demande cette reinitialisation, ignorez cet email.
                  </p>
                </td>
              </tr>

            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """

    headers = {
        "Authorization": f"Bearer {sg_api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "personalizations": [{"to": [{"email": to}]}],
        "from": {"email": current_app.config.get("SENDGRID_FROM_EMAIL", "rayanebicaba.dev@gmail.com")},
        "subject": "ZAWANI — Reinitialisation de mot de passe",
        "content": [{"type": "text/html", "value": html}],
    }

    try:
        response = requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            json=payload,
            headers=headers,
            timeout=30,
        )
        response.raise_for_status()
        logger.info(f"[SENDGRID] Password reset email sent to {to}, status={response.status_code}")
    except Exception as e:
        logger.error(f"[SENDGRID] Failed to send to {to}: {e}")
        raise


def send_reset_password_email(to, token):
    link = f"{current_app.config['FRONTEND_URL']}/reinitialiser-mot-de-passe?token={token}"
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin:0;padding:0;background-color:#f7f7f7;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
      <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f7f7f7;padding:40px 20px;">
        <tr>
          <td align="center">
            <table width="100%" cellpadding="0" cellspacing="0" style="max-width:480px;background-color:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,0.06);">

              <tr>
                <td style="padding:40px 32px 24px;text-align:center;">
                  <h1 style="margin:0 0 8px;font-size:28px;font-weight:800;color:#c94301;letter-spacing:-0.5px;">ZAWANI</h1>
                  <p style="margin:0;font-size:13px;color:#999999;">Votre plateforme d'artisans</p>
                </td>
              </tr>

              <tr>
                <td style="padding:0 32px;">
                  <div style="height:1px;background-color:#f0f0f0;"></div>
                </td>
              </tr>

              <tr>
                <td style="padding:32px;">
                  <h2 style="margin:0 0 16px;font-size:20px;font-weight:700;color:#1a1a1a;">Reinitialisation de mot de passe</h2>
                  <p style="margin:0 0 8px;font-size:15px;color:#555555;line-height:1.6;">
                    Bonjour,
                  </p>
                  <p style="margin:0 0 24px;font-size:15px;color:#555555;line-height:1.6;">
                    Vous avez demande la reinitialisation de votre mot de passe. Cliquez sur le bouton ci-dessous :
                  </p>

                  <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                      <td align="center" style="padding:0 0 24px;">
                        <a href="{link}" style="display:inline-block;background-color:#c94301;color:#ffffff;font-size:15px;font-weight:600;text-decoration:none;padding:14px 32px;border-radius:10px;">
                          Reinitialiser mon mot de passe
                        </a>
                      </td>
                    </tr>
                  </table>

                  <p style="margin:0 0 8px;font-size:13px;color:#999999;line-height:1.5;">
                    Ou copiez ce lien dans votre navigateur :
                  </p>
                  <p style="margin:0 0 24px;font-size:12px;color:#c94301;word-break:break-all;line-height:1.5;">
                    {link}
                  </p>
                </td>
              </tr>

              <tr>
                <td style="padding:0 32px;">
                  <div style="height:1px;background-color:#f0f0f0;"></div>
                </td>
              </tr>

              <tr>
                <td style="padding:24px 32px 32px;text-align:center;">
                  <p style="margin:0;font-size:12px;color:#bbbbbb;line-height:1.5;">
                    Ce lien expire dans 1 heure.<br>
                    Si vous n'avez pas demande cette reinitialisation, ignorez cet email.
                  </p>
                </td>
              </tr>

            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """
    _send_smtp(to, "ZAWANI — Reinitialisation de mot de passe", html)
