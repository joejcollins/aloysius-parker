"""User class represents a user in the database."""

import uuid
from email.utils import parseaddr
from json import loads

from sqlalchemy import Column, String

from flask_forge.database.db import database
from flask_forge.database.message import Message


class User(database.Model):
    """User class represents a user in the database.

    The class holds information about the user's name and email,
    and contains validation logic for those fields.
    """

    __tablename__ = "users"

    id: str = Column(String, primary_key=True)
    name: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False)

    MIN_USERNAME_LENGTH: int = 2
    MAX_USERNAME_LENGTH: int = 16
    MAX_EMAIL_LENGTH: int = 64
    ALLOWED_EMAIL_PROVIDER_DOMAINS: set[str] = {"gmail.com", "mail.ru", "outlook.com"}
    EMAIL_SPLIT_EXPECTED_LENGTH: int = 2

    def __init__(self, name: str | None, email: str | None, id: str = None):
        """Create a new User object with a provided name and email."""
        # If an existing ID is provided, validate it
        if id:
            try:
                uuid.UUID(hex=id, version=4)
            except ValueError as e:
                raise ValueError("Invalid existing user ID") from e

        # Username checking logic
        if (
            not name
            or len(name) < self.MIN_USERNAME_LENGTH
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

        if (
            len(email_split) != self.EMAIL_SPLIT_EXPECTED_LENGTH
            or not email_split[0]
            or not email_split[1]
        ):
            raise ValueError("Invalid email address")

        domain: str = email_split[1]

        if domain not in self.ALLOWED_EMAIL_PROVIDER_DOMAINS:
            raise ValueError(
                f"Email provider {domain} is not allowed. "
                f"Only {', '.join(self.ALLOWED_EMAIL_PROVIDER_DOMAINS)} are allowed."
            )

        self.id: str = id or uuid.uuid4().hex
        self.name: str = name
        self.email: str = email

    @classmethod
    def from_json(cls, json_str) -> "User":
        """Create a new User object from a JSON string."""
        json_dict = loads(json_str)
        return cls(**json_dict)

    def send_message(self, recipient: "User", message: str):
        """Send a message to another user."""
        message = Message(self, recipient, message)

        with database.session.begin():
            database.session.add(message)

    def fetch_messages(self, contains: str = None) -> list[Message]:
        """Fetch messages sent to this user."""
        query = database.session.query(Message).filter(Message.recipient_id == self.id)
        if contains:
            query = query.filter(Message.content.contains(contains))

        return query.all()

    def to_json(self) -> dict:
        """Return a JSON representation of the User object."""
        return {"id": self.id, "name": self.name, "email": self.email}

    def __hash__(self) -> int:
        """Return a hash of the user's id."""
        return hash(self.id)
