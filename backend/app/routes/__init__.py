def register_routes(app):
    from .health import health_bp
    from .auth import auth_bp
    from .oauth import oauth_bp
    from .admin import admin_bp
    from .commerce import commerce_bp
    from .diagram import diagram_bp
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(oauth_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/api")
    app.register_blueprint(commerce_bp, url_prefix="/api")
    app.register_blueprint(diagram_bp, url_prefix="/api")
