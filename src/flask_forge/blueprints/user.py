"""Handle requests to /user/ endpoint."""

import flask_smorest
from flask import views

from flask_forge.handler import user
from flask_forge.models.message import (
    DeleteMessageSchemaArguments,
    GetMessageSchemaArguments,
    PostMessageSchema,
)
from flask_forge.models.user import UserPatchSchema

SMOREST_USER_BLUEPRINT = flask_smorest.Blueprint(
    "user", __name__, description="Management of individual users."
)


@SMOREST_USER_BLUEPRINT.route("/user/<string:user_id>")
class UserEndpoint(views.MethodView):
    """Define the endpoint for /users/<id>.

    This endpoint is used to retrieve and delete an existing user.
    """

    @SMOREST_USER_BLUEPRINT.response(200)
    def get(self, user_id: str):
        """Retrieve user information based on id."""
        return user.fetch_user(user_id)

    @SMOREST_USER_BLUEPRINT.response(204)
    def delete(self, user_id: str):
        """Delete an existing user based on id."""
        return user.delete_user(user_id)

    @SMOREST_USER_BLUEPRINT.response(200)
    @SMOREST_USER_BLUEPRINT.arguments(UserPatchSchema)
    def patch(self, data: dict, user_id: str):
        """Update an existing user based on id."""
        return user.edit_user(user_id, data)


@SMOREST_USER_BLUEPRINT.route("/user/<string:user_id>/messages")
class UserMessagesEndpoint(views.MethodView):
    """Define the endpoint for /users/<id>/messages.

    This endpoint is used to retrieve all messages for a user and send a new message.
    """

    @SMOREST_USER_BLUEPRINT.response(200)
    @SMOREST_USER_BLUEPRINT.arguments(GetMessageSchemaArguments, location="query")
    def get(self, args: dict, user_id: str):
        """GET all messages for a user."""
        return user.get_user_messages(user_id, args)

    # todo: consider specifying location="json" for each blueprint arg
    @SMOREST_USER_BLUEPRINT.response(201)
    @SMOREST_USER_BLUEPRINT.arguments(PostMessageSchema)
    def post(self, data: dict, user_id: str):
        """POST a new message to an existing user."""
        return user.send_user_message(data["author_id"], user_id, data["content"])

    @SMOREST_USER_BLUEPRINT.response(204)
    @SMOREST_USER_BLUEPRINT.arguments(DeleteMessageSchemaArguments, location="query")
    def delete(self, args: dict, user_id: str):
        """Delete a message for a user."""
        return user.delete_user_message(user_id, args)
