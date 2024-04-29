"""Flask application for rapid deployment via Docker."""

from flask import Flask

from flask_forge.config import blueprints, monitoring, open_api
from flask_forge.error_handler import handle_error


def create_app() -> Flask:
    """Create a flask application with pre-defined configurations."""
    the_app = Flask(__name__)
    open_api.configure_open_api(the_app)
    blueprints.configure_blueprints(the_app)
    monitoring.configure_monitoring(the_app)
    the_app.register_error_handler(Exception, handle_error)
    return the_app


def run():
    """Run the Flask app."""
    app = create_app()
    app.run()

run()
