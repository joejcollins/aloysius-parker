from flask import jsonify

from flask_forge.database.db import database
from flask_forge.database.user import User


def fetch_user(uuid: str):
    """Fetch a user based on UUID."""
    if user := database.session.get(User, uuid):
        return user.to_json()
    else:
        return jsonify(error="user not found"), 404


def delete_user(uuid: str):
    """Delete a user based on UUID."""
    if database.session.filter_by(User, uuid=uuid).delete():
        return "", 204
    else:
        return jsonify(error="user not found"), 404
