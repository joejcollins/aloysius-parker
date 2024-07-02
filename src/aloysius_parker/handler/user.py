"""Handle functions for /blueprints/user.py."""

from http import HTTPStatus

from aloysius_parker.database.db import database
from aloysius_parker.database.message import Message
from aloysius_parker.database.user import User
from aloysius_parker.database.user_repository import UserRepository

USERS = UserRepository(database)
GET_MESSAGES_MIN_LIMIT: int = 1
GET_MESSAGES_MAX_LIMIT: int = 100


def fetch_user(user_id: str):
    """Fetch a user based on id."""
    if user := USERS.get_user(user_id):
        return user.to_json()

    return {"error": "user not found"}, HTTPStatus.NOT_FOUND


def delete_user(user_id: str):
    """Delete a user based on id."""
    if USERS.delete_user(user_id):
        return "", HTTPStatus.NO_CONTENT

    return {"error": "user not found"}, HTTPStatus.NOT_FOUND


def get_user_messages(user_id: str, args: dict):
    """Retrieve all messages for a user based on id."""
    limit: int = args.get("limit", 50)

    if not USERS.get_user(user_id):
        return {"error": "user not found"}, HTTPStatus.NOT_FOUND

    if not (messages := USERS.get_user_messages(user_id, limit)):
        return "", HTTPStatus.NO_CONTENT

    return [message.to_json() for message in messages]


def edit_user(user_id: str, data: dict):
    """Update a user based on their ID and new data provided."""
    new_user: User = User.from_json(data)
    if not (user := USERS.update_user(user_id, new_user)):
        return {"error": "user not found"}, HTTPStatus.NOT_FOUND

    return user.to_json()


def send_user_message(author_id: str, recipient_id: str, content: str):
    """Send a new message with content from author_id to recipient_id."""
    if author_id == recipient_id:
        return {"error": "find some friends"}, HTTPStatus.UPGRADE_REQUIRED
    elif not (USERS.get_user(author_id) and USERS.get_user(recipient_id)):
        return {"error": "author or recipient not found"}, HTTPStatus.NOT_FOUND

    message: Message = USERS.send_user_message(author_id, recipient_id, content)
    return message.to_json(), HTTPStatus.CREATED


def delete_user_message(recipient_id: str, args: dict):
    """Delete a message sent to the recipient with the provided message ID."""
    message_id: str = args.get("message_id")

    if not USERS.get_user(recipient_id):
        return {"error": "recipient not found"}, HTTPStatus.NOT_FOUND

    if not USERS.delete_user_message(recipient_id, message_id):
        return {"error": "message not found"}, HTTPStatus.NOT_FOUND

    return "", HTTPStatus.NO_CONTENT

    # if (
    #     message := database.session.query(Message)
    #     .filter_by(id=message_id, recipient_id=recipient_id)
    #     .first()
    # ):
    #     database.session.delete(message)
    #     database.session.commit()
    #     return "", 204
