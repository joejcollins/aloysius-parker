"""Handles requests to /users endpoint."""

from typing import Any

from flask import jsonify, make_response
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError

from flask_forge.blueprint.blueprints import USER_BLUEPRINT
from flask_forge.database.db import database
from flask_forge.database.user import User
from flask_forge.model.user import UserSchema


@USER_BLUEPRINT.route("/users")
class UsersEndpoint(MethodView):
    """Define the endpoint for /users.

    This endpoint is used to create a new user via a POST request.
    It's separate from UserEndpoint as this endpoint does not accept a UUID.
    """

    @USER_BLUEPRINT.response(200)
    def get(self):
        """Retrieve all users."""
        if users := [user.to_json() for user in User.query.all()]:
            return users

        return "", 204

    @USER_BLUEPRINT.response(201)
    @USER_BLUEPRINT.arguments(UserSchema)
    def post(self, data: dict[str, Any]):
        """Create a new user via a POST request."""
        name = data.get("name")
        email = data.get("email")

        try:
            with database.session.begin():
                user = User(name, email)
                database.session.add(user)
        except ValueError as e:
            return make_response(jsonify(error=str(e)), 400)  # TODO: turn into jsonify instead of make_response()
        except SQLAlchemyError as e:
            return make_response(jsonify(error=f"database error: {e}"), 500)
        except Exception as e:
            return make_response(jsonify(error=f"internal server error: {e}"), 500)

        return user.to_json()
