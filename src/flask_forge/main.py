"""Entry point for the Flask API."""

from flask import Flask

from flask_forge.config import monitoring


def create_app():
    """Create the Flask app."""
    new_app = Flask(__name__)
    monitoring.configure_monitoring(new_app)
    return new_app


def run():
    """Run the Flask app."""
    app = create_app()
    app.run()
