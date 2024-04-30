"""Add a user to the database and confirm it was added.

By default pytest will run the tests in alpha numeric order so each test should be
named test_001, test_002, test_003, etc.
"""

from http import HTTPStatus
from typing import Generator

import pytest
from flask import testing
from flask_forge import main


class SharedResources:
    """Resources shared between the tests.

    We could use module scoped variables, but the linters like them to be in CAPITALS
    since they look like constants.  This seems like a convenient way to pass the shared
    variables around between tests.
    """

    def __init__(self) -> None:
        """Initialize the tokens."""
        self.user_id = "Not set"


@pytest.fixture(name="flask_client")
def create_flask_client() -> Generator:
    """Create a flask test client."""
    flask_api = main.create_app()
    with flask_api.test_client() as client:
        yield client


def test_001_get_empty_user_list(flask_client: testing.FlaskClient) -> None:
    """Post a new redirect using the V2 API."""
    # Act
    response = flask_client.get("/users")
    # Assert
    # The list should be empty.
    assert response.status_code == HTTPStatus.NO_CONTENT
