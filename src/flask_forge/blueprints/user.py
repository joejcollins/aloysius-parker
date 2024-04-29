"""Handle requests to /user/ endpoint."""

import flask_smorest
from flask import jsonify, make_response, views

from flask_forge.database.user import User
from flask_forge.model.user import UserSchema

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
        if user := User.query.get(uuid):
            return user.to_json()
        else:
            return make_response(jsonify(error="user not found"), 404)

    @SMOREST_USER_BLUEPRINT.response(204)
    def delete(self, uuid: str):
        """Delete an existing user based on UUID."""
        if User.query.filter_by(uuid=uuid).delete():
            return "", 204

        return make_response(jsonify(error="user not found"), 404)

    def patch(self, uuid: str, data: UserSchema):
        """Update an existing user based on UUID."""
        raise NotImplementedError("PATCH method not implemented yet")
