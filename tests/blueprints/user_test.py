"""Test the user blueprint."""

from http import HTTPStatus

import flask
import pytest
from _pytest.monkeypatch import MonkeyPatch
from flask import app as flask_app
from flask.testing import FlaskClient
from flask_forge import main
from flask_forge.database import user
from sqlalchemy.orm import query


@pytest.fixture()
def app() -> flask_app.Flask:
    """Create a test fixture Flask application."""
    test_app = main.create_app()
    test_app.config["TESTING"] = True  # so we get better error messages.
    return test_app


def test_user_get(client: FlaskClient, monkeypatch: MonkeyPatch) -> None:
    """Test the retrieval of a user."""
    # ARRANGE
    bogus_user_data: dict = {
        "name": "Joe Bloggs",
        "email": "joebloggs@gmail.com",
    }
    bogus_user: user.User = user.User(**bogus_user_data)
    monkeypatch.setattr(query.Query, "get", lambda self, uuid: bogus_user)
    url = flask.url_for("user.UserEndpoint", uuid="7e557495d9104520a017773b9fc7bd5e")
    # ACT
    response = client.get(url)
    # ASSERT
    assert response.status_code == HTTPStatus.OK
    assert response.json["email"] == "joebloggs@gmail.com"
