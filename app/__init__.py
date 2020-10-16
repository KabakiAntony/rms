from flask import Flask
from flask_migrate import Migrate
from app.api.view.views import rms


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
    app.register_blueprint(rms)

    return app
