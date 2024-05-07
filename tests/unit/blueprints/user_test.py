"""Test the user blueprint."""

from http import HTTPStatus
from typing import Any

import flask
import pytest
from _pytest.monkeypatch import MonkeyPatch
from flask import app as flask_app
from flask.testing import FlaskClient
from flask_forge import main
from flask_forge.database import user
from sqlalchemy.orm import scoping


@pytest.fixture()
def app() -> flask_app.Flask:
    """Create a test fixture Flask application."""
    test_app = main.create_app()
    test_app.config["TESTING"] = True  # so we get better error messages.
    return test_app


def test_get_user_found(client: FlaskClient, monkeypatch: MonkeyPatch) -> None:
    """Test the retrieval of a user."""
    # ARRANGE
    bogus_user_data: dict = {
        "name": "Joe Bloggs",
        "email": "joebloggs@gmail.com",
    }
    bogus_user: user.User = user.User(**bogus_user_data)
    monkeypatch.setattr(
        scoping.scoped_session, "get", lambda self, entity, id: bogus_user
    )
    url = flask.url_for("user.UserEndpoint", id="7e557495d9104520a017773b9fc7bd5e")

    # ACT
    response = client.get(url)

    # ASSERT
    assert response.status_code == HTTPStatus.OK
    assert response.json["email"] == "joebloggs@gmail.com"


@pytest.mark.parametrize("invalid_id", ["joe_bloggs", " ", 1])
def test_get_user_not_found(invalid_id: Any, client: FlaskClient) -> None:
    """Test the retrieval of a user with an invalid id."""
    # ARRANGE
    url = flask.url_for("user.UserEndpoint", id=invalid_id)

    # ACT
    response = client.get(url)

    # ASSERT
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert "not found" in response.json["error"]


def test_create_user_invalid_email(client: FlaskClient) -> None:
    """Test the creation of a user with an invalid email."""
    # ARRANGE
    invalid_user_data: dict = {
        "name": "Joe Bloggs",
        "email": "joebloggsgmail.com",  # No @ in the email
    }
    url = flask.url_for("users.UsersEndpoint")

    # ACT
    response = client.post(url, json=invalid_user_data)

    # ASSERT
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "Invalid email address" in response.json["error"]


def test_create_user_username_too_long(client: FlaskClient) -> None:
    """Test the creation of a user with an invalid username."""
    # ARRANGE
    invalid_user_data: dict = {
        "name": "Joe" * 100,
        "email": "joebloggs@gmail.com",
    }

    url = flask.url_for("users.UsersEndpoint")
    # ACT
    response = client.post(url, json=invalid_user_data)

    # ASSERT
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "Username must be between" in response.json["error"]


def test_create_user_bad_email_provider(client: FlaskClient) -> None:
    """Test the creation of a user with an invalid email provider."""
    # ARRANGE
    invalid_user_data: dict = {
        "name": "Joe Bloggs",
        "email": "joebloggs@invalid.com",  # Invalid email provider
    }
    url = flask.url_for("users.UsersEndpoint")

    # ACT
    response = client.post(url, json=invalid_user_data)

    # ASSERT
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "user validation error:" in response.json["error"]
    # TODO: Consider error codes in the future..?


@pytest.mark.parametrize("data", [
    ({"name": "", "email": "joebloggs@gmail.com"}),
    ({"name": "Joe", "email": ""}),
    ({"name": "J", "email": "joebloggs@gmail.com"}),
    ({"name": "Joe", "email": "j"})
])
def test_create_user_invalid_email_or_username(data: dict, client: FlaskClient) -> None:
    """Test the creation of a user with an invalid email or username."""
    # ARRANGE
    url = flask.url_for("users.UsersEndpoint")

    # ACT
    response = client.post(url, json=data)

    # ASSERT
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert ("Username must be between" in response.json["error"]
            or "Invalid email address" in response.json["error"])
