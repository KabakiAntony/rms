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
from app.api.view.ui import rms as ui_blueprint
from app.api.view.project import rms as project_blueprint
from app.api.view.budget import rms as budget_blueprint
from app.api.view.employees import rms as employee_blueprint
from app.api.view.user import rms as user_blueprint
from app.api.view.payments import rms as payment_blueprint


migrate = Migrate(compare_type=True)


def create_app():
    """
    this is my app factory
    """
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    from app.api.model import db, ma
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(company_blueprint)
    app.register_blueprint(ui_blueprint)
    app.register_blueprint(project_blueprint)
    app.register_blueprint(budget_blueprint)
    app.register_blueprint(employee_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(payment_blueprint)
    app.app_context().push()

    return app
