"""Add the OpenAPI configuration."""

from flask import app


def configure_open_api(flask_api: app.Flask) -> None:
    """Add the OpenAPI configuration to the Flask app so flask_smorest can use it."""
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
    flask_api.config.update(config)
