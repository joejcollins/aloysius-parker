"""Handle requests to /user/ endpoint."""

import flask_smorest
from flask import views

from flask_forge.handler import user

SMOREST_USER_BLUEPRINT = flask_smorest.Blueprint(
    "user", __name__, description="Management of individual users."
)


@SMOREST_USER_BLUEPRINT.route("/user/<string:uuid>")
class UserEndpoint(views.MethodView):
    """Define the endpoint for /users/<uuid>.

    This endpoint is used to retrieve and delete an existing user.
    """

    @SMOREST_USER_BLUEPRINT.response(200)
    def get(self, uuid: str):
        """Retrieve user information based on UUID."""
        return user.fetch_user(uuid)

    @SMOREST_USER_BLUEPRINT.response(204)
    def delete(self, uuid: str):
        """Delete an existing user based on UUID."""
        return user.delete_user(uuid)

    # This doesn't work as of now:
    # - TypeError: UserEndpoint.patch() got multiple values for argument 'uuid'

    # @SMOREST_USER_BLUEPRINT.response(200)
    # @SMOREST_USER_BLUEPRINT.arguments(UserPatchSchema)
    # def patch(self, uuid: str, data: UserPatchSchema):
    #     """Update an existing user based on UUID."""
    #     if not data.name and not data.email:
    #         return jsonify(error="either name or email must be provided"), 400
    #
    #     if user := database.session.query(User).get(uuid):
    #         user.name = data.name
    #         user.email = data.email
    #         database.session.commit()
    #         return user.to_json()
    #
    #     return jsonify(error="user not found"), 404
