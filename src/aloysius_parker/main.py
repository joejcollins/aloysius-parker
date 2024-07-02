"""Flask application for rapid deployment via Docker."""

from flask import Flask

from aloysius_parker.config import blueprints, monitoring, open_api
from aloysius_parker.database.db import database


def create_app() -> Flask:
    """Create a flask application with pre-defined configurations."""
    the_app = Flask(__name__)
    open_api.configure_open_api(the_app)
    blueprints.configure_blueprints(the_app)
    monitoring.configure_monitoring(the_app)
    database.init_app(the_app)
    with the_app.app_context():
        database.create_all()
    return the_app


def run():
    """Run the Flask app."""
    app = create_app()
    app.run(host="0.0.0.0")


if __name__ == "__main__":
    run()
