"""Defines the schema for the Message object."""

import uuid

from marshmallow import Schema, ValidationError, fields, validates


class PostMessageSchema(Schema):
    """Schema for the POST request to create a message."""

    _MAX_CONTENT_LENGTH: int = 250

    content = fields.String(
        required=True, metadata={"description": "The content of the message"}
    )

    author_id = fields.String(
        required=True, metadata={"description": "The author of the message"}
    )

    @validates("author_id")
    def validate_author_id(self, value):
        """Ensure author_id is a valid UUID."""
        try:
            uuid.UUID(hex=value, version=4)
        except ValueError as e:
            raise ValidationError("Invalid author ID") from e

    @validates("content")
    def validate_content(self, value):
        """Ensure content is not empty."""
        if len(value) > self._MAX_CONTENT_LENGTH:
            raise ValidationError(
                f"Content must not exceed {self._MAX_CONTENT_LENGTH} characters"
            )


class GetMessageSchemaArguments(Schema):
    """Schema for the GET request to retrieve messages with a limit."""

    _LIMIT_MIN_VALUE: int = 1
    _LIMIT_MAX_VALUE: int = 100

    limit = fields.Integer(
        required=False, metadata={"description": "Amount of messages to retrieve"}
    )

    @validates("limit")
    def validate_limit(self, value):
        """Ensure limit is within boundaries is valid."""
        if not self._LIMIT_MIN_VALUE <= value <= self._LIMIT_MAX_VALUE:
            raise ValidationError(
                f"Limit must be between "
                f"{self._LIMIT_MIN_VALUE} and {self._LIMIT_MAX_VALUE}"
            )


class DeleteMessageSchemaArguments(Schema):
    """Schema for the DELETE request to delete a message."""

    message_id = fields.String(
        required=True, metadata={"description": "The ID of the message to delete"}
    )
