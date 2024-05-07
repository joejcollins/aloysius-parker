"""Handle requests to /user/ endpoint."""

import flask_smorest
from flask import views

from flask_forge.handler import user
from flask_forge.models.message import MessageSchema

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

    # This doesn't work as of now:
    # - TypeError: UserEndpoint.patch() got multiple values for argument 'id'

    # @SMOREST_USER_BLUEPRINT.response(200)
    # @SMOREST_USER_BLUEPRINT.arguments(UserPatchSchema)
    # def patch(self, id: str, data: UserPatchSchema):
    #     """Update an existing user based on id."""
    #     if not data.name and not data.email:
    #         return jsonify(error="either name or email must be provided"), 400
    #
    #     if user := database.session.query(User).get(id):
    #         user.name = data.name
    #         user.email = data.email
    #         database.session.commit()
    #         return user.to_json()
    #
    #     return jsonify(error="user not found"), 404


@SMOREST_USER_BLUEPRINT.route("/user/<string:user_id>/messages")
class UserMessagesEndpoint(views.MethodView):
    """Define the endpoint for /users/<id>/messages.

    This endpoint is used to retrieve all messages for a user and send a new message.
    """

    # TODO: Add history/limit parameter to fetch only the last N messages
    @SMOREST_USER_BLUEPRINT.response(200)
    def get(self, user_id: str):
        """GET all messages for a user."""
        return user.get_user_messages(user_id)

    # todo: consider specifying location="json" for each blueprint arg
    @SMOREST_USER_BLUEPRINT.response(201)
    @SMOREST_USER_BLUEPRINT.arguments(MessageSchema)
    def post(self, data: dict, user_id: str):
        """POST a new message to an existing user."""
        return user.send_user_message(data["author_id"], user_id, data["content"])
