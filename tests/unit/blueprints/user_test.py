"""Test the user blueprint."""

from http import HTTPStatus
from typing import Any

import flask
import pytest
from _pytest.monkeypatch import MonkeyPatch
from flask import app as flask_app
from flask.testing import FlaskClient
from aloysius_parker import main
from aloysius_parker.database import user
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
    # Patch over the get on the session so it always returns the bogus user.
    bogus_user_data: dict = {
        "name": "Joe Bloggs",
        "email": "joebloggs@gmail.com",
    }
    bogus_user: user.User = user.User(**bogus_user_data)
    monkeypatch.setattr(
        scoping.scoped_session, "get", lambda self, entity, id: bogus_user
    )
    url = flask.url_for("user.UserEndpoint", user_id="7e557495d9104520a017773b9fc7bd5e")
    # ACT
    response = client.get(url)
    # ASSERT
    assert response.status_code == HTTPStatus.OK
    assert response.json["email"] == "joebloggs@gmail.com"


@pytest.mark.parametrize("invalid_id", ["joe_bloggs", " ", 1])
def test_get_user_not_found(invalid_id: Any, client: FlaskClient) -> None:
    """Test the retrieval of a user with an invalid uuid."""
    # ARRANGE
    url = flask.url_for("user.UserEndpoint", user_id=invalid_id)
    # ACT
    response = client.get(url)
    # ASSERT
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert "not found" in response.json["error"]
