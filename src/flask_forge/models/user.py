"""Defines the HTTP request schema for classes so that Swagger has more context."""
import re
from email.utils import parseaddr

from marshmallow import Schema, ValidationError, fields, validates


class UserSchema(Schema):
    """Defines the schema for the User object."""

    _MIN_USERNAME_LENGTH: int = 2
    _MAX_USERNAME_LENGTH: int = 16
    _MAX_EMAIL_LENGTH: int = 64
    _ALLOWED_EMAIL_PROVIDER_DOMAINS: set[str] = {"gmail.com", "mail.ru", "outlook.com"}
    _EMAIL_REGEX = re.compile(r"([^@]+)@([^@]+\.[^@]+)$")

    name = fields.String(
        required=True, metadata={"description": "The name of the user"}
    )

    email = fields.String(
        required=True, metadata={"description": "The email of the user"}
    )

    @validates("name")
    def validate_name(self, value):
        """Ensure name is valid."""
        if (
                not value
                or len(value) < self._MIN_USERNAME_LENGTH
                or len(value) > self._MAX_USERNAME_LENGTH
        ):
            raise ValidationError(
                f"Username must be between {self._MIN_USERNAME_LENGTH} and "
                f"{self._MAX_USERNAME_LENGTH} characters long"
            )

    @validates("email")
    def validate_email(self, value):
        """Ensure email is valid."""
        if len(value) > self._MAX_EMAIL_LENGTH:
            raise ValidationError(
                f"Email must be less than {self._MAX_EMAIL_LENGTH} characters long"
            )

        # Validate email format and extract domain using precompiled regex
        match = self._EMAIL_REGEX.match(parseaddr(value)[1])
        if not match:
            raise ValidationError("Invalid email address")

        user, domain = match.groups()

        if domain not in self._ALLOWED_EMAIL_PROVIDER_DOMAINS:
            raise ValidationError(
                f"Email provider {domain} is not allowed. "
                f"Only {', '.join(self._ALLOWED_EMAIL_PROVIDER_DOMAINS)} are allowed."
            )


class UserPatchSchema(UserSchema):
    """Defines the schema for patching the User object."""

    name = fields.String(
        required=False, metadata={"description": "The name of the user"}
    )

    email = fields.String(
        required=False, metadata={"description": "The email of the user"}
    )

    @validates("name")
    def validate_name(self, value):
        """Ensure name is valid."""
        super().validate_name(value)

    @validates("email")
    def validate_email(self, value):
        """Ensure email is valid."""
        super().validate_email(value)
