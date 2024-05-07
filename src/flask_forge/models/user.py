"""Defines the HTTP request schema for classes so that Swagger has more context."""
from marshmallow import Schema, fields


class UserSchema(Schema):
    """Defines the schema for the User object."""

    name = fields.String(
        required=True, metadata={"description": "The name of the user"}
    )

    email = fields.String(
        required=True, metadata={"description": "The email of the user"}
    )

    # TODO: consider moving validation checks here from db/user.py?
    # @validates("name")
    # def validate_name(self, value):
    #     """Ensure name is valid."""
    #     ...  # Do checks here!


class UserPatchSchema(Schema):
    """Defines the schema for patching the User object."""

    name = fields.String(
        required=False, metadata={"description": "The name of the user"}
    )

    email = fields.String(
        required=False, metadata={"description": "The email of the user"}
    )
