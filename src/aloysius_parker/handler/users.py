"""Handle functions for /blueprints/users.py."""

from http import HTTPStatus

from sqlalchemy.exc import SQLAlchemyError

from aloysius_parker.database.db import database
from aloysius_parker.database.user import User


def get_users():
    """Retrieve all users."""
    if users := database.session.query(User).all():
        return [user.to_json() for user in users]

    return "", HTTPStatus.NO_CONTENT


def create_user(data: dict):
    """Create a new user."""
    name: str = data.get("name")
    email: str = data.get("email")

    try:
        user: User = User(name, email)
    except ValueError as e:
        return {"error": f"user validation error: {e}"}, HTTPStatus.BAD_REQUEST
    except SQLAlchemyError as e:
        return {"error": f"database error: {e}"}, HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        return {
            "error": f"internal server error: {e}"
        }, HTTPStatus.INTERNAL_SERVER_ERROR
    else:
        with database.session.begin():
            database.session.add(user)

    return user.to_json()
