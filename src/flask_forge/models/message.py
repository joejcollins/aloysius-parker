"""Defines the schema for the Message object."""
from marshmallow import Schema, fields


class MessageSchema(Schema):
    """Defines the schema for the Message object."""

    content = fields.String(
        required=True, metadata={"description": "The content of the message"}
    )

    author_id = fields.String(
        required=True, metadata={"description": "The author of the message"}
    )
