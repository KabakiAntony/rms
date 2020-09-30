from flask import Flask
# from config import TestingConfig


def create_app():
    """
    this is my app factory
    """
    app = Flask(__name__)
    app.config.from_object('config.TestingConfig')

    return app
