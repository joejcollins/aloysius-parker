"""Handle functions for /blueprints/user.py."""
from flask import jsonify

from flask_forge.database.db import database
from flask_forge.database.message import Message
from flask_forge.database.user import User


def fetch_user(user_id: str):
    """Fetch a user based on id."""
    if user := database.session.get(User, user_id):
        return user.to_json()
    else:
        return jsonify(error="user not found"), 404


def delete_user(user_id: str):
    """Delete a user based on id."""
    if database.session.filter_by(User, id=user_id).delete():
        return "", 204
    else:
        return jsonify(error="user not found"), 404


def get_user_messages(user_id: str):
    """Retrieve all messages for a user based on id."""
    # Fetch the user from the database
    user: User = database.session.query(User).get(user_id)
    if not user:
        return {"error": "User not found"}, 404

    # Fetch all messages for the user
    messages: list[Message] = user.fetch_messages()
    if not messages:
        return "", 204

    return [message.to_json() for message in messages]


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
