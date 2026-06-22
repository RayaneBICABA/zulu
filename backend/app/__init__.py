from flask import Flask, jsonify
from .config import config
from .extensions import db, migrate, jwt, cors, swagger
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


def create_app(env="default"):
    app = Flask(__name__)
    app.config.from_object(config[env])

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

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

    from .routes import register_routes
    register_routes(app)

    return app
