"""Handle functions for /blueprints/users.py."""
from flask_forge.database.db import database
from flask_forge.database.user import User


def get_users():
    """Retrieve all users."""
    if users := database.session.query(User).all():
        return [user.to_json() for user in users]

    return "", 204


def create_user(name: str, email: str):
    """Create a new user."""
    user = User(name, email)
    with database.session.begin():
        database.session.add(user)

    return user.to_json()
