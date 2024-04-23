"""Run the Flask app."""

from flask_forge.examples.blueprints.app import APP


def runserver():
    """Run the Flask application."""
    APP.run(host="127.0.0.1", port=5000)
