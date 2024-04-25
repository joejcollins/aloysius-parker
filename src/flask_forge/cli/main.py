"""Run the Flask app."""
import os

from flask_forge.main import APP

PORT: int = os.getenv("PORT") or 5000


def run():
    """Run the Flask application."""
    APP.run(host="127.0.0.1", port=PORT)
