"""Handle functions for /blueprints/users.py."""
from sqlalchemy.exc import SQLAlchemyError

from flask_forge.database.db import database
from flask_forge.database.user import User


def get_users():
    """Retrieve all users."""
    if users := database.session.query(User).all():
        return [user.to_json() for user in users]

    return "", 204


def create_user(data: dict):
    """Create a new user."""
    name: str = data.get("name")
    email: str = data.get("email")

    try:
        user: User = User(name, email)
    except ValueError as e:
        return {"error": f"user validation error: {e}"}, 400
    except SQLAlchemyError as e:
        return {"error": f"database error: {e}"}, 500
    except Exception as e:
        return {"error": f"internal server error: {e}"}, 500
    else:
        with database.session.begin():
            database.session.add(user)

    return user.to_json()
