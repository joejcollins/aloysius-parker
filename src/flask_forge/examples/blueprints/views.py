from typing import Any

from flask import make_response, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint

from flask_forge.examples.blueprints.user import users, UserSchema, User

blueprint = Blueprint("users", "users", description="User management API")


@blueprint.route("/users")
class UsersEndpoint(MethodView):

    @blueprint.response(201)
    @blueprint.arguments(UserSchema)
    def post(self, data: dict[str, Any]):
        name = data.get("name")
        email = data.get("email")

        try:
            user = User(name, email)
            print(f"[{user.uuid}] {user.name} has been created")
        except ValueError as e:
            return make_response(jsonify(error=str(e)), 400)
        except Exception as e:
            return make_response(jsonify(error=f"internal server error: {e}"), 500)

        users[user.uuid] = user
        return user.__dict__


@blueprint.route("/users/<string:uuid>")
class UserEndpoint(MethodView):

    # Retrieve user information
    @blueprint.response(200)
    def get(self, uuid: str):
        if user := users.get(uuid):
            return user.__dict__
        else:
            return make_response(jsonify(error="user not found"), 404)

    # Delete an existing user
    @blueprint.response(204)
    def delete(self, uuid: str):
        if users.get(uuid):
            del users[uuid]
        else:
            return make_response(jsonify(error="user not found"), 404)
