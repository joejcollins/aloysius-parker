"""User class represents a user in the database."""
from email.utils import parseaddr
from json import loads
from uuid import uuid4

from sqlalchemy import Column, String

from flask_forge.examples.user_database.db import database


class User(database.Model):
    """User class represents a user in the database.

    The class holds information about the user's name and email,
    and contains validation logic for those fields.
    """

    __tablename__ = "users"

    uuid: Column[String] = Column(String, primary_key=True)
    name: Column[String] = Column(String, nullable=False)
    email: Column[String] = Column(String, nullable=False)

    MIN_USERNAME_LENGTH: int = 2
    MAX_USERNAME_LENGTH: int = 16
    MAX_EMAIL_LENGTH: int = 64
    ALLOWED_EMAIL_PROVIDER_DOMAINS: set[str] = {"gmail.com", "mail.ru", "outlook.com"}
    EMAIL_SPLIT_EXPECTED_LENGTH: int = 2

    def __init__(self, name: str | None, email: str | None):
        """Create a new User object with a provided name and email."""
        # Username checking logic
        if (
            not name or
            len(name) < self.MIN_USERNAME_LENGTH
            or len(name) > self.MAX_USERNAME_LENGTH
        ):
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

        if (len(email_split) != self.EMAIL_SPLIT_EXPECTED_LENGTH
                or not email_split[0] or not email_split[1]):
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
        """Create a new User object from a JSON string."""
        json_dict = loads(json_str)
        return cls(**json_dict)

    def to_json(self):
        """Return a JSON representation of the User object."""
        return {
            "uuid": self.uuid,
            "name": self.name,
            "email": self.email
        }

    def __hash__(self):
        """Return a hash of the user's UUID."""
        return hash(self.uuid)
