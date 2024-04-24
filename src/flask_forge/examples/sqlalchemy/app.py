from datetime import datetime

from flask import Flask, Response, jsonify
from flask_smorest import Api

from flask_forge.examples.sqlalchemy.db import database
from .errors import ErrorSchema
from .user import blueprint as UserBlueprint

# This is an example API server that features simple user registration, user retrieval,
# and user deletion


def create_app() -> Flask:
    config: dict[str, str | bool] = {
        "PROPAGATE_EXCEPTIONS": True,
        "API_TITLE": "User Management API",
        "API_VERSION": "v1",
        "OPENAPI_VERSION": "3.0.3",
        "OPENAPI_URL_PREFIX": "/",
        "OPENAPI_SWAGGER_UI_PATH": "/swagger-ui",
        "OPENAPI_SWAGGER_UI_URL": "https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # sqlite:///data.db
    }

    app: Flask = Flask(__name__)
    app.config.update(config)
    api: Api = Api(app)
    api.ERROR_SCHEMA = ErrorSchema

    api.register_blueprint(UserBlueprint)
    database.create_all()

    return app


START_TIME: datetime = datetime.now()
APP: Flask = create_app()


# Defines what the path "/" will do
@APP.route("/")
def home() -> Response:
    endpoints = [rule.rule for rule in APP.url_map.iter_rules()]
    return jsonify(
        name=__name__, endpoints=endpoints, uptime=str(datetime.now() - START_TIME)
    )
