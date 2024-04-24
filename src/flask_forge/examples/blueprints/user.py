from email.utils import parseaddr
from json import loads
from uuid import uuid4

from flask.views import MethodView
from marshmallow import Schema, fields

from flask_forge.examples.blueprints.db import database

users: dict[str] = database["users"]


class User(MethodView):
    MIN_USERNAME_LENGTH: int = 2
    MAX_USERNAME_LENGTH: int = 16
    MAX_EMAIL_LENGTH: int = 64
    ALLOWED_EMAIL_PROVIDER_DOMAINS: set[str] = {"gmail.com", "mail.ru", "outlook.com"}
    EMAIL_SPLIT_EXPECTED_LENGTH: int = 2

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

        if len(email_split) != self.EMAIL_SPLIT_EXPECTED_LENGTH or not email_split[0] or not email_split[1]:
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
