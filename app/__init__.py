# -*- coding=utf-8 -*-

from flask import Flask
from app.config import load_configurations, configure_logging
from .views import webhook_blueprint


def create_app():
    app = Flask(__name__)

    # Load configurations and logging settings
    configure_logging(app)
    load_configurations(app)

    # Import and register the blueprint
    app.register_blueprint(webhook_blueprint)

    return app
