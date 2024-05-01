"""Represent a series of unfortunate yet bad sign-up attempts."""
from http import HTTPStatus
from typing import Generator

import pytest
import werkzeug.test
from flask import testing

from flask_forge import main


def is_bad_response(response: werkzeug.test.TestResponse) -> bool:
    """Return True if the code is in the 4XX zone and JSON is present."""
    return (HTTPStatus.BAD_REQUEST <= response.status_code <
            HTTPStatus.INTERNAL_SERVER_ERROR and response.json)


@pytest.fixture(scope="module", name="flask_client")
def create_flask_client() -> Generator:
    """Create a flask test client."""
    flask_api = main.create_app()
    with flask_api.test_client() as client:
        yield client


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
    data = {
        "name": "I like buffer overflows" * 100,
        "email": "yes@gmail.com"
    }
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
