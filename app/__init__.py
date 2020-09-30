from flask import Flask
from config import Testing


def create_app():
    """
    this is my app factory
    """
    app = Flask(__name__)
    app.config.from_object(Testing())

    return app
