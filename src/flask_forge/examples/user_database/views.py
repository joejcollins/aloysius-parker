"""Define the views for the user database API.

Flask's MethodView maps HTTP methods to functions that handle the requests.
"""
from typing import Any

from flask import jsonify, make_response
from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy.exc import SQLAlchemyError

from flask_forge.examples.user_database.db import database
from flask_forge.examples.user_database.schemas import UserSchema
from flask_forge.examples.user_database.user import User

blueprint = Blueprint("users", __name__, description="User management API")


@blueprint.route("/users")
class UsersEndpoint(MethodView):
    """Define the endpoint for /users.

    This endpoint is used to create a new user via a POST request.
    It's separate from UserEndpoint as this endpoint does not accept a UUID.
    """

    @blueprint.response(200)
    def get(self):
        """Retrieve all users."""
        if users := [user.to_json() for user in User.query.all()]:
            return users
        else:
            return "", 204

    @blueprint.response(201)
    @blueprint.arguments(UserSchema)
    def post(self, data: dict[str, Any]):
        """Create a new user via a POST request."""
        name = data.get("name")
        email = data.get("email")

        try:
            with database.session.begin():
                user = User(name, email)
                database.session.add(user)
        except ValueError as e:
            return make_response(jsonify(error=str(e)), 400)
        except SQLAlchemyError as e:
            return make_response(jsonify(error=f"database error: {e}"), 500)
        except Exception as e:
            return make_response(jsonify(error=f"internal server error: {e}"), 500)

        return user.to_json()


@blueprint.route("/users/<string:uuid>")
class UserEndpoint(MethodView):
    """Define the endpoint for /users/<uuid>.

    This endpoint is used to retrieve and delete an existing user.
    """

    @blueprint.response(200)
    def get(self, uuid: str):
        """Retrieve user information based on UUID."""
        if user := User.query.get(uuid):
            return user.to_json()
        else:
            return make_response(jsonify(error="user not found"), 404)

    @blueprint.response(204)
    def delete(self, uuid: str):
        """Delete an existing user based on UUID."""
        if User.query.filter_by(uuid=uuid).delete():
            return "", 204

        return make_response(jsonify(error="user not found"), 404)
