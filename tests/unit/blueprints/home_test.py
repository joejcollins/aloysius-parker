"""Confirm that the home endpoint works."""

from http import HTTPStatus

import flask
import pytest
from flask import app as flask_app
from flask.testing import FlaskClient
from flask_forge import main


@pytest.fixture()
def app() -> flask_app.Flask:
    """Create a test fixture Flask application."""
    test_app = main.create_app()
    test_app.config["TESTING"] = True  # so we get better error messages.
    return test_app


def test_json_returns(client: FlaskClient) -> None:
    """Just check that the endpoint returns a JSON response."""
    # ARRANGE
    url = flask.url_for("home.home")
    # ACT
    response = client.options(url)
    # ASSERT
    assert response.status_code == HTTPStatus.OK
