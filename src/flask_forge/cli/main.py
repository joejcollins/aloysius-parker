"""Run the Flask app."""

from flask_forge.examples.blueprints.app import APP


def runserver(host, port):
    """Run the Flask application"""
    print("Running the server...")
    APP.run(host=host, port=port)
