from email.utils import parseaddr
from json import loads
from typing import Any
from uuid import uuid4

from flask import jsonify, make_response
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import Schema, fields

from .db import database

users: dict[str] = database["users"]

blueprint = Blueprint("users", "users", description="User management API")


@blueprint.route("/users/<string:uuid>")
class User(MethodView):
    MIN_USERNAME_LENGTH: int = 2
    MAX_USERNAME_LENGTH: int = 16
    MAX_EMAIL_LENGTH: int = 64
    ALLOWED_EMAIL_PROVIDER_DOMAINS: set[str] = {"gmail.com", "mail.ru", "outlook.com"}

    # Retrieve user information
    @blueprint.response(200)
    def get(self, uuid: str):
        user = users.get(uuid, None)
        if not user:
            return make_response(jsonify(error="user not found"), 404)

        return user.__dict__

    # Delete an existing user
    @blueprint.response(204)
    def delete(self, uuid: str):
        user = users.get(uuid, None)
        if not user:
            return make_response(jsonify(error="user not found"), 404)

        del users[uuid]

    def __init__(self, name: str | None, email: str | None):
        if not name:
            raise ValueError("Name cannot be empty")

        # Username checking logic
        if len(name) < self.MIN_USERNAME_LENGTH or len(name) > self.MAX_USERNAME_LENGTH:
            raise ValueError(
                f"Username must be between {self.MIN_USERNAME_LENGTH} and "
                f"{self.MAX_USERNAME_LENGTH} characters long"
            )

        if len(email) > self.MAX_EMAIL_LENGTH:
            raise ValueError(
                f"Email must be less than {self.MAX_EMAIL_LENGTH} characters long"
            )

        # Email checking logic.
        # parseaddr() return a tuple of (name, email), we only need the email part
        email: str = parseaddr(email)[1]
        email_split: list[str] = email.split("@")

        if len(email_split) != 2 or not email_split[0] or not email_split[1]:
            raise ValueError("Invalid email address")

        domain: str = email_split[1]

        if domain not in self.ALLOWED_EMAIL_PROVIDER_DOMAINS:
            raise ValueError(
                f"Email provider {domain} is not allowed. "
                f"Only {', '.join(self.ALLOWED_EMAIL_PROVIDER_DOMAINS)} are allowed."
            )

        self.uuid: str = uuid4().hex
        self.name: str = name
        self.email: str = email

    @classmethod
    def from_json(cls, json_str):
        json_dict = loads(json_str)
        return cls(**json_dict)

    def __hash__(self):
        return hash(self.uuid)


class UserSchema(Schema):
    name = fields.String(required=True, description="The name of the user")
    email = fields.String(required=True, description="The email of the user")


@blueprint.route("/users")
class Users(MethodView):
    # Register a new user
    @blueprint.response(201)
    @blueprint.arguments(UserSchema)
    def post(self, data: dict[str, Any]):
        name = data.get("name", None)
        email = data.get("email", None)

        try:
            user = User(name, email)
            print(f"[{user.uuid}] {user.name} has been created")
        except ValueError as e:
            return make_response(jsonify(error=str(e)), 400)
        except Exception as e:
            return make_response(jsonify(error=f"internal server error: {e}"), 500)

        users[user.uuid] = user
        return user.__dict__
