"""Handles requests to /users endpoint."""

import flask_smorest
from flask import jsonify, views
from sqlalchemy.exc import SQLAlchemyError

from flask_forge.handler import users
from flask_forge.models.user import UserSchema

SMOREST_USERS_BLUEPRINT = flask_smorest.Blueprint(
    "users", __name__, description="Management of the users."
)


@SMOREST_USERS_BLUEPRINT.route("/users")
class UsersEndpoint(views.MethodView):
    """Define the endpoint for /users.

    This endpoint is used to create a new user via a POST request.
    It's separate from UserEndpoint as this endpoint does not accept an ID.
    """

    @SMOREST_USERS_BLUEPRINT.response(200)
    def get(self):
        """Retrieve all users."""
        return users.get_users()

    @SMOREST_USERS_BLUEPRINT.response(201)
    @SMOREST_USERS_BLUEPRINT.arguments(UserSchema)
    def post(self, data: dict):
        """Create a new user via a POST request."""
        name = data.get("name")
        email = data.get("email")

        try:
            return users.create_user(name, email)
        except ValueError as e:
            return {"error": f"user validation error: {e}"}, 400
        except SQLAlchemyError as e:
            return {"error": f"database error: {e}"}, 500
        except Exception as e:
            return {"error": f"internal server error: {e}"}, 500
