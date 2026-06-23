import os
from flask import Flask, jsonify
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
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    limiter.init_app(app)

    if not app.config.get("TESTING"):
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

    from .services.oauth_service import init_oauth
    init_oauth(app)

    return app
