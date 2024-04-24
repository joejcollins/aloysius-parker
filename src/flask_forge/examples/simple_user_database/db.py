from typing import Any

from flask_forge.examples.simple_user_database.user import User

# Simple in-memory database
database: dict[str, Any] = {
    "users": {}
}

users: dict[str, User] = database["users"]
