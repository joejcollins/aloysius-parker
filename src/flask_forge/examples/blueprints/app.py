from datetime import datetime

from flask import Flask, Response, jsonify
from flask_smorest import Api

from flask_forge.examples.blueprints.errors import ErrorSchema
from flask_forge.examples.blueprints.views import blueprint as user_blueprint


def create_app():
    config: dict[str, str | bool] = {
        "PROPAGATE_EXCEPTIONS": True,
        "API_TITLE": "User Management API",
        "API_VERSION": "v1",
        "OPENAPI_VERSION": "3.0.3",
        "OPENAPI_URL_PREFIX": "/",
        "OPENAPI_SWAGGER_UI_PATH": "/swagger-ui",
        "OPENAPI_SWAGGER_UI_URL": "https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
    }

    new_app = Flask(__name__)
    new_app.config.update(config)
    return new_app


START_TIME: datetime = datetime.now()
APP: Flask = create_app()

API: Api = Api(APP)
API.ERROR_SCHEMA = ErrorSchema
API.register_blueprint(user_blueprint)


# Defines what the path "/" will do
@APP.route("/")
def home() -> Response:
    endpoints = [rule.rule for rule in APP.url_map.iter_rules()]
    return jsonify(
        name=__name__, endpoints=endpoints, uptime=str(datetime.now() - START_TIME)
    )


if __name__ == "__main__":
    APP.run()
