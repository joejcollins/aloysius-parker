"""Flask application for rapid deployment via Docker."""

from datetime import datetime

from flask import Flask, Response, jsonify
from flask_smorest import Api

from flask_forge.blueprint.blueprints import USER_BLUEPRINT
from flask_forge.config import monitoring
from flask_forge.database.db import database
from flask_forge.error.errors import ErrorSchema


def create_app() -> Flask:
    """Create a flask application with pre-defined configurations."""
    config: dict[str, str | bool] = {
        "PROPAGATE_EXCEPTIONS": True,
        "API_TITLE": "User Management API",
        "API_VERSION": "v1",
        "OPENAPI_VERSION": "3.0.3",
        "OPENAPI_URL_PREFIX": "/",
        "OPENAPI_SWAGGER_UI_PATH": "/swagger-ui",
        "OPENAPI_SWAGGER_UI_URL": "https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    }

    # Initialise Flask app with the configurations
    app = Flask(__name__)
    app.config.update(config)

    # Set up the database
    database.init_app(app)
    with app.app_context():
        database.create_all()

    # Configure Prometheus monitoring
    monitoring.configure_monitoring(app)

    return app


START_TIME: datetime = datetime.now()
APP: Flask = create_app()

API: Api = Api(APP)
API.register_blueprint(USER_BLUEPRINT)
API.ERROR_SCHEMA = ErrorSchema


@APP.route("/")
def home() -> Response:
    """Return a JSON response with the name of the app, endpoints, and the uptime."""
    endpoints = [rule.rule for rule in APP.url_map.iter_rules()]
    return jsonify(
        name=__name__, endpoints=endpoints, uptime=str(datetime.now() - START_TIME)
    )


def run():
    """Run the Flask app."""
    app = create_app()
    app.run()
