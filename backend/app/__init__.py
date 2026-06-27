import os
from flask import Flask, jsonify
from flask_cors import CORS
from .config import config
from .extensions import db, migrate, jwt, cors, swagger, limiter
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


def create_app(env=None):
    if env is None:
        env = os.getenv("FLASK_ENV", "production")
        if env not in config:
            env = "production"
    app = Flask(__name__)
    app.config.from_object(config[env])

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors_origins = [
        app.config.get("FRONTEND_URL", "http://localhost:5173"),
        "http://localhost:5173",
        "http://localhost:4173",
        "http://localhost:8100",
        "capacitor://localhost",
        "https://localhost",
        "https://localhost:8100",
        "ionic://localhost",
        "https://zawani.app",
        "https://www.zawani.app",
        r"https://.*\.vercel\.app",
        r"https://.*\.onrender\.com",
    ]
    cors.init_app(app, resources={r"/api/*": {"origins": cors_origins, "supports_credentials": True}})
    limiter.init_app(app)

    import cloudinary
    cloudinary.config(
        cloud_name=app.config["CLOUDINARY_CLOUD_NAME"],
        api_key=app.config["CLOUDINARY_API_KEY"],
        api_secret=app.config["CLOUDINARY_API_SECRET"],
    )

    if not app.config.get("TESTING"):
        app.config["SWAGGER"] = {
            "title": "Zulu API",
            "description": "API pour la plateforme Zulu — annuaire d'artisans",
            "version": "1.0.0",
            "securityDefinitions": {
                "Bearer": {
                    "type": "apiKey",
                    "name": "Authorization",
                    "in": "header",
                    "description": "JWT token. Format: Bearer <token>",
                }
            },
            "security": [{"Bearer": []}],
        }
        swagger.init_app(app)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"error": "Token expire."}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"error": "Token invalide."}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"error": "Token manquant."}), 401

    @app.errorhandler(429)
    def ratelimit_handler(error):
        return jsonify({"error": "Trop de tentatives. Reessayez dans une minute."}), 429

    from .routes import register_routes
    register_routes(app)

    from .commands import seed_roles
    app.cli.add_command(seed_roles)

    from .services.oauth_service import init_oauth
    init_oauth(app)

    return app
