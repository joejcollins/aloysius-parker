"""Handles requests to /users endpoint."""

import flask_smorest
from flask import views

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
        return users.create_user(data)
