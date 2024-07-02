"""User class represents a user in the database."""

import uuid
from json import loads

from marshmallow import ValidationError
from sqlalchemy import Column, String

from aloysius_parker.database.db import database
from aloysius_parker.database.message import Message


class User(database.Model):
    """User class represents a user in the database.

    The class holds information about the user's name and email,
    and contains validation logic for those fields.
    """

    __tablename__ = "users"

    id: str = Column(String, primary_key=True)
    name: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False)

    def __init__(self, name: str | None, email: str | None, id: str = None):
        """Create a new User object with a provided name and email."""
        # If an existing ID is provided, validate it
        if id:
            try:
                uuid.UUID(hex=id, version=4)
            except ValueError as e:
                raise ValidationError("Invalid existing user ID") from e

        self.id: str = id or uuid.uuid4().hex
        self.name: str = name
        self.email: str = email

    @classmethod
    def from_json(cls, data) -> "User":
        """Create a new User object from a JSON string."""
        # If the data is already a dictionary, use it as-is
        if isinstance(data, str):
            data = loads(data)

        return cls(**data)

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
