"""Handle functions for /blueprints/convenience.py."""

from aloysius_parker.database.db import database
from aloysius_parker.database.user import User


def create_example_user():
    """Automatically create a dummy user."""
    user = User("Username", "Email@gmail.com")
    with database.session.begin():
        database.session.add(user)

    return user.to_json()
