"""Handle functions for /blueprints/user.py."""

from flask_forge.database.db import database
from flask_forge.database.message import Message
from flask_forge.database.user import User

GET_MESSAGES_MIN_LIMIT: int = 1
GET_MESSAGES_MAX_LIMIT: int = 100


def fetch_user(user_id: str):
    """Fetch a user based on id."""
    if user := database.session.get(User, user_id):
        return user.to_json()
    else:
        return {"error": "user not found"}, 404


def delete_user(user_id: str):
    """Delete a user based on id."""
    if database.session.filter_by(User, id=user_id).delete():
        return "", 204

    return {"error": "user not found"}, 404


def get_user_messages(user_id: str, args: dict):
    """Retrieve all messages for a user based on id."""
    limit: int = args.get("limit", 50)

    if user := database.session.query(User).filter_by(id=user_id).limit(limit).first():
        return (
            [message.to_json() for message in messages]
            if (messages := user.fetch_messages())
            else ("", 204)
        )

    return {"error": "User not found"}, 404


def edit_user(user_id: str, data: dict):
    """Update a user based on id."""
    if "name" not in data and "email" not in data:
        return {"error": "either name or email must be provided"}, 400

    if user := database.session.query(User).get(user_id):
        user.name = data.get("name", user.name)
        user.email = data.get("email", user.email)
        database.session.commit()
        return user.to_json()

    return {"error": "user not found"}, 404


def send_user_message(author_id: str, recipient_id: str, content: str):
    """Send a new message with content from author_id to recipient_id."""
    author: User = database.session.query(User).get(author_id)
    if not author:
        return {"error": "Invalid author"}, 404

    recipient: User = database.session.query(User).get(recipient_id)
    if not recipient_id:
        return {"error": "Recipient not found"}, 404

    try:
        message = Message(
            author_id=author.id, recipient_id=recipient.id, message=content
        )
    except ValueError as e:
        return {"error": e}, 400

    # Commit message to database
    database.session.add(message)
    database.session.commit()

    return message.to_json(), 201


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
