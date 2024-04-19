from datetime import datetime

from flask import Flask, jsonify, Response
from flask_smorest import Api

from .errors import ErrorSchema
from .user import blueprint as UserBlueprint

# This is an example API server that features simple user registration, user retrieval, and user deletion
START_TIME: datetime = datetime.now()
APP: Flask = Flask(__name__)

CONFIG: dict[str, str | bool] = {
    "PROPAGATE_EXCEPTIONS": True,
    "API_TITLE": "User Management API",
    "API_VERSION": "v1",
    "OPENAPI_VERSION": "3.0.3",
    "OPENAPI_URL_PREFIX": "/",
    "OPENAPI_SWAGGER_UI_PATH": "/swagger-ui",
    "OPENAPI_SWAGGER_UI_URL": "https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
}

APP.config.update(CONFIG)
API: Api = Api(APP)
API.ERROR_SCHEMA = ErrorSchema


# Defines what the path "/" will do
@APP.route("/")
def home() -> Response:
    endpoints = [rule.rule for rule in APP.url_map.iter_rules()]
    return jsonify(name=__name__, endpoints=endpoints, uptime=str(datetime.now() - START_TIME))


API.register_blueprint(UserBlueprint)
