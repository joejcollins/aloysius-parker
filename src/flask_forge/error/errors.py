"""Logic concerning error handling for requests."""
from enum import Enum

from marshmallow import Schema, fields


# TODO: Standardise the error handling with flask_smorest
class ErrorEnum(Enum):
    """Unique error codes for the application. Unused for now."""

    USER_NOT_FOUND = 1001
    USER_ALREADY_EXISTS = 1002
    USER_INVALID_NAME = 1003
    USER_INVALID_EMAIL = 1004
    USER_INVALID_USERNAME_LENGTH = 1005
    USER_INVALID_EMAIL_PROVIDER = 1006


class ErrorSchema(Schema):
    """Global error schema for the application."""

    code: ErrorEnum = fields.Enum(ErrorEnum, description="Unique error code")
    message: str = fields.String(description="Error message details")
