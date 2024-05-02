"""Set up the blueprints."""

import flask_smorest
from flask import app

from flask_forge.blueprints import home, user, users
from flask_forge.models import errors


def configure_blueprints(flask_api: app.Flask) -> None:
    """Register the blueprints and the error schema with the Flask app."""
    flask_api.register_blueprint(home.BLUEPRINT)
    flask_api: flask_smorest.Api = flask_smorest.Api(flask_api)
    flask_api.register_blueprint(user.SMOREST_USER_BLUEPRINT)
    flask_api.register_blueprint(users.SMOREST_USERS_BLUEPRINT)
    flask_api.ERROR_SCHEMA = errors.ErrorSchema
