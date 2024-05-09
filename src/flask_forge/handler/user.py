"""Handle functions for /blueprints/user.py."""

from flask import jsonify

from flask_forge.database.db import database
from flask_forge.database.message import Message
from flask_forge.database.user import User
from flask_forge.database.user_repository import UserRepository

USERS = UserRepository(database)
GET_MESSAGES_MIN_LIMIT: int = 1
GET_MESSAGES_MAX_LIMIT: int = 100


def fetch_user(user_id: str):
    """Fetch a user based on id."""
    if user := USERS.get_user(user_id):
        return user.to_json()

    return {"error": "user not found"}, 404


def delete_user(user_id: str):
    """Delete a user based on id."""
    if USERS.delete_user(user_id):
        return "", 204

    return {"error": "user not found"}, 404


def get_user_messages(user_id: str, args: dict):
    """Retrieve all messages for a user based on id."""
    limit: int = args.get("limit", 50)

    if not USERS.get_user(user_id):
        return {"error": "user not found"}, 404

    if not (messages := USERS.get_user_messages(user_id, limit)):
        return "", 204

    return [message.to_json() for message in messages]


def edit_user(user_id: str, data: dict):
    """Update a user based on their ID and new data provided."""
    new_user: User = User.from_json(data)
    if not (user := USERS.update_user(user_id, new_user)):
        return {"error": "user not found"}, 404

    return user.to_json()


def send_user_message(author_id: str, recipient_id: str, content: str):
    """Send a new message with content from author_id to recipient_id."""
    return USERS.send_user_message(author_id, recipient_id, content), 201


def delete_user_message(recipient_id: str, args: dict):
    """Delete a message sent to the recipient with the provided message ID."""
    message_id: str = args.get("message_id")
    if (
        message := database.session.query(Message)
        .filter_by(id=message_id, recipient_id=recipient_id)
        .first()
    ):
        database.session.delete(message)
        database.session.commit()
        return "", 204

    return {"error": "message not found"}, 404
