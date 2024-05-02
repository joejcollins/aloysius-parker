"""Attempt to add a new user but continually get it wrong.

These are really separate user stories so could be split into separate test modules, but
for the sake of convenience, they are all in one test module.
"""

from http import HTTPStatus
from typing import Any, Generator

import pytest
from flask import testing
from flask_forge import main
from werkzeug import test


# region Fixtures and helper functions
def is_bad_response(response: test.TestResponse) -> Any:
    """Return True if the code is in the 4XX zone and JSON is present."""
    is_a_400_code = (
        HTTPStatus.BAD_REQUEST
        <= response.status_code
        < HTTPStatus.INTERNAL_SERVER_ERROR
    )
    has_json = response.json
    return is_a_400_code and has_json


@pytest.fixture(scope="module", name="flask_client")
def create_flask_client() -> Generator:
    """Create a flask test client."""
    flask_api = main.create_app()
    flask_api.config["TESTING"] = True
    with flask_api.test_client() as client:
        yield client


# endregion


def test_001_add_user_empty_fields(flask_client: testing.FlaskClient) -> None:
    """Add a user to the database."""
    # Act
    response = flask_client.post("/users", json={})

    # Assert that the request was rejected
    assert is_bad_response(response)


def test_002_add_user_empty_values(flask_client: testing.FlaskClient) -> None:
    """Add a user to the database."""
    # Act
    data = {"name": "", "email": ""}
    response = flask_client.post("/users", json=data)

    # Assert that the request was rejected
    assert is_bad_response(response)


def test_003_add_user_missing_fields(flask_client: testing.FlaskClient) -> None:
    """Add a user to the database."""
    # Act
    data = {"name": "Good username"}
    response = flask_client.post("/users", json=data)

    # Assert that the request was rejected
    assert is_bad_response(response)


def test_004_add_user_invalid_email(flask_client: testing.FlaskClient) -> None:
    """Add a user to the database."""
    # Act
    data = {"name": "Good username", "email": "Bad email"}
    response = flask_client.post("/users", json=data)

    # Assert that the request was rejected
    assert is_bad_response(response)


def test_004_add_user_length_username(flask_client: testing.FlaskClient) -> None:
    """Test if requests with extremely long usernames fail."""
    # Act
    data = {"name": "I like buffer overflows" * 100, "email": "yes@gmail.com"}
    response = flask_client.post("/users", json=data)

    # Assert that the request was rejected
    assert is_bad_response(response)


def test_005_add_user_bad_email_provider(flask_client: testing.FlaskClient) -> None:
    """Add a user to the database."""
    # Act
    data = {"name": "Good username", "email": "yes@tempmail.com"}
    response = flask_client.post("/users", json=data)

    # Assert that the request was rejected
    assert is_bad_response(response)


def test_006_add_user_excess_fields(flask_client: testing.FlaskClient) -> None:
    """Add a user to the database."""
    # Act
    data = {
        "name": "Good username",
        "email": "yes@gmail.com",
        "extra": "I shouldn't be here",
    }
    response = flask_client.post("/users", json=data)

    # Assert that the request was rejected
    assert is_bad_response(response)


def test_007_add_user_send_form_data(flask_client: testing.FlaskClient) -> None:
    """Test if POST requests with form data rather than JSON fail."""
    # Act
    data = {"name": "Good username", "email": "yes@gmail.com"}
    response = flask_client.post("/users", data=data)

    # Assert that the request was rejected
    assert is_bad_response(response)


def test_008_add_user_short_username(flask_client: testing.FlaskClient) -> None:
    """Test if requests with short fields fail."""
    # Act
    data = {"name": "1", "email": "yes@gmail.com"}
    response = flask_client.post("/users", json=data)

    # Assert that the request was rejected
    assert is_bad_response(response)
