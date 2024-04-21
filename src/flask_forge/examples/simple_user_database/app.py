from datetime import datetime

from flask import Flask, jsonify, make_response, request

from .db import users
from .user import User

# This is an example API server that features simple user registration, user retrieval,
# and user deletion
START_TIME: datetime = datetime.now()
APP: Flask = Flask(__name__)


# Defines what the path "/" will do
@APP.route("/")
def home():
    endpoints = [rule.rule for rule in APP.url_map.iter_rules()]
    return jsonify(
        name=__name__, endpoints=endpoints, uptime=str(datetime.now() - START_TIME)
    )


@APP.get("/users/<string:uuid>")
def get_user(uuid: str):
    user = users.get(uuid, None)
    if not user:
        return make_response(jsonify(error="user not found"), 404)
    return user.__dict__  # Automatically turns into JSON content-type: application/json


@APP.delete("/users/<string:uuid>")
def unregister(uuid: str):
    user = users.get(uuid, None)
    if not user:
        return make_response(jsonify(error="user not found"), 404)

    del users[uuid]
    return "", 204  # Remember that this is a tuple


# Registration endpoint that only accepts POST requests
@APP.post("/users/register")
def register():
    # If the request content type is not application/json,
    # this will raise a 415 Unsupported Media Type error
    data = request.json

    # Get the name and email from the JSON data
    name = data.get("name", None)
    email = data.get("email", None)

    # Create a new user object. This will error if the class doesn't like the data
    try:
        user = User(name, email)
        print(f"[{user.uuid}] {user.name} has been created")
    except ValueError as e:
        return make_response(jsonify(error=str(e)), 400)

    # Add the user to the database
    users[user.uuid] = user

    # Return the user object as a JSON string
    return user.__dict__
