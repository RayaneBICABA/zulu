def register_routes(app):
    from .health import health_bp
    app.register_blueprint(health_bp, url_prefix="/api")
