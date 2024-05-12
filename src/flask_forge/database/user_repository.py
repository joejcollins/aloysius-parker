from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Result

from flask_forge.database.db import database
from flask_forge.database.message import Message
from flask_forge.database.user import User


class UserRepository:
    """Repository class for user database operations."""

    def __init__(self, db: SQLAlchemy):
        """Define the database this repository will use."""
        self.db = db

    def get_user(self, user_id: str) -> User | None:
        """Fetch a user based on their ID."""
        return self.db.session.query(User).get(user_id)

    def get_users(self) -> [User]:
        """Fetch all users from the database."""
        return self.db.session.query(User).all()

    def create_user(self, user: User) -> None:
        """Insert a User object into the database."""
        self.db.session.add(user)
        self.db.session.commit()

    def delete_user(self, user_id: str) -> bool:
        """Delete a user based on their ID. Returns true if user was deleted."""
        if not (user := self.get_user(user_id)):
            return False

        self.db.session.delete(user)
        self.db.session.commit()
        return True

    def update_user(self, user_id: str, new_user: User) -> User | None:
        """Update a user based on their ID. Returns true if user was updated."""
        user: User = self.get_user(user_id)
        if not user:
            return

        user.name = new_user.name or user.name
        user.email = new_user.email or user.email
        self.db.session.commit()
        return user

    def get_user_messages(self, user_id: str, limit: int) -> [Message]:
        """Fetch messages sent to a user based on their ID.

        "limit" specifies the maximum number of messages to return.
        """
        query: Result = (
            self.db.session.query(Message)
            .filter(Message.recipient_id == user_id)
            .limit(limit)
        )

        return query.all()

    def send_user_message(
        self, author_id: str, recipient_id: str, content: str
    ) -> Message:
        """Send a message from author_id to recipient_id."""
        message: Message = Message(author_id, recipient_id, content)
        self.db.session.add(message)
        self.db.session.commit()
        return message

    def delete_user_message(self, recipient_id: str, message_id: str) -> bool:
        """Delete a message sent to the recipient with the provided message ID."""
        if (
            message := self.db.session.query(Message)
            .filter_by(id=message_id, recipient_id=recipient_id)
            .first()
        ):
            self.db.session.delete(message)
            self.db.session.commit()
            return True

        return False
