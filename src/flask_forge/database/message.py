"""Message class representing a message in the database."""

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from flask_forge.database.db import database

MAX_MESSAGE_LENGTH: int = 250


class Message(database.Model):
    """User class represents a user in the database.

    The class holds information about the message content, the sender,
    and the recipient. It also contains a timestamp noting when it was sent.
    """

    __tablename__ = "messages"

    id: Column[String] = Column(String, primary_key=True)
    content: Column[String] = Column(String(MAX_MESSAGE_LENGTH), nullable=False)
    author_id: Column[String] = Column(String, ForeignKey("users.id"))
    recipient_id: Column[String] = Column(String, ForeignKey("users.id"))
    timestamp: Column[DateTime] = Column(DateTime, default=datetime.utcnow)

    def __init__(self, author_id: str, recipient_id: str, content: str):
        """Create a new Message object."""
        self.id: str = uuid4().hex
        self.author_id: str = author_id
        self.recipient_id: str = recipient_id
        self.content: str = content
        self.timestamp: datetime = datetime.now(timezone.utc)

    author = relationship("User", foreign_keys=[author_id])
    recipient = relationship("User", foreign_keys=[recipient_id])

    def to_json(self) -> dict:
        """Return a JSON representation of the message."""
        return {
            "id": self.id,
            "author_id": self.author_id,
            "recipient_id": self.recipient_id,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
        }
