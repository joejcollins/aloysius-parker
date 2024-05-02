"""Defines the HTTP request schema for classes so that Swagger has more context."""
from marshmallow import Schema, fields


class UserSchema(Schema):
    """Defines the schema for the User object."""

    name = fields.String(required=True, description="The name of the user")
    email = fields.String(required=True, description="The email of the user")
