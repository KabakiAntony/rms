"""
this is my application
factory
"""
from flask import Flask
# this is to force config
# to be loaded on startup
from config import Config
from flask_migrate import Migrate
from app.api.view.company import rms as company_blueprint
from app.api.view.user import rms as user_blueprint
from app.api.view.ui import rms as ui_blueprint


migrate = Migrate()


def create_app():
    """
    this is my app factory
    """
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    from app.api.model.models import db, ma
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(company_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(ui_blueprint)
    app.app_context().push()

    return app
