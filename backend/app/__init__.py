from flask import Flask
from .config import config
from .extensions import db, migrate, jwt, cors, swagger

def create_app(env="default"):
    app = Flask(__name__)
    app.config.from_object(config[env])

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    # Swagger uniquement hors testing
    if not app.config.get("TESTING"):
        swagger.init_app(app)

    # Register blueprints
    from .routes import register_routes
    register_routes(app)

    return app
