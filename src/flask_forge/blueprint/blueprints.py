"""List of all the blueprints are stored here."""

from flask_smorest import Blueprint

USER_BLUEPRINT = Blueprint("users", __name__, description="User management API")
