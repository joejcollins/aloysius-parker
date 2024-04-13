from typing import Dict, Any
from .user import User

# Simple in-memory database
database: dict[str, Any] = {
    "users": {}
}

users: Dict[str, User] = database["users"]
