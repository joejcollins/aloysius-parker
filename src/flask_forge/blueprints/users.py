"""Handles requests to /users endpoint."""

from typing import Any

import flask_smorest
from flask import jsonify
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError

from flask_forge.database.db import database
from flask_forge.database.user import User
from flask_forge.model.user import UserSchema

SMOREST_USERS_BLUEPRINT = flask_smorest.Blueprint(
    "users", __name__, description="Management of the users."
)


@SMOREST_USERS_BLUEPRINT.route("/users")
class UsersEndpoint(MethodView):
    """Define the endpoint for /users.

    This endpoint is used to create a new user via a POST request.
    It's separate from UserEndpoint as this endpoint does not accept a UUID.
    """

    @SMOREST_USERS_BLUEPRINT.response(200)
    def get(self):
        """Retrieve all users."""
        if users := [user.to_json() for user in User.query.all()]:
            return users

        return "", 204

    @SMOREST_USERS_BLUEPRINT.response(201)
    @SMOREST_USERS_BLUEPRINT.arguments(UserSchema)
    def post(self, data: dict[str, Any]):
        """Create a new user via a POST request."""
        name = data.get("name")
        email = data.get("email")

        try:
            with database.session.begin():
                user = User(name, email)
                database.session.add(user)
        except ValueError as e:
            return jsonify(error=str(e)), 400
        except SQLAlchemyError as e:
            return jsonify(error=f"database error: {e}"), 500
        except Exception as e:
            return jsonify(error=f"internal server error: {e}"), 500

        return user.to_json()
