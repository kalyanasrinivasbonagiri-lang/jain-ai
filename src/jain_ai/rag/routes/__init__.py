from .admin import admin_bp
from .api import api_bp
from .health import health_bp
from .web import web_bp


def register_blueprints(app):
    app.register_blueprint(web_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)
