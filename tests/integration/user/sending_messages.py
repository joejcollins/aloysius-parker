"""Test message sending functionality."""

from http import HTTPStatus
from typing import Generator

import pytest
from flask import testing
from flask_forge import main
from flask_forge.database.user import User


# region Fixtures and helper functions
class SharedResources:
    """Resources shared between the tests."""

    def __init__(self) -> None:
        """Initialize the tokens."""
        self.adam = None
        self.eve = None


@pytest.fixture(name="resources", scope="module")
def shared_resources() -> SharedResources:
    """Return the shared resources object."""
    return SharedResources()


@pytest.fixture(scope="module", name="flask_client")
def create_flask_client() -> Generator:
    """Create a flask test client."""
    flask_api = main.create_app()
    flask_api.config["TESTING"] = True
    with flask_api.test_client() as client:
        yield client


# endregion


def test_001_create_users(flask_client: testing.FlaskClient,
                          resources: SharedResources) -> None:
    """Create the first ever humans in flask-forge-land."""
    # Arrange 2 user accounts
    data_user_1 = {"name": "Adam", "email": "adam@gmail.com"}
    data_user_2 = {"name": "Eve", "email": "eve@mail.ru"}

    # Create the 2 users sequentially
    for account in (data_user_1, data_user_2):
        response = flask_client.post("/users", json=account)

        # Assert the resource is created and response is not empty
        assert response.status_code == HTTPStatus.CREATED
        assert response.text

    resources.adam = User.from_json(response.text)
    resources.eve = User.from_json(response.text)


def test_002_send_message(flask_client: testing.FlaskClient,
                          resources: SharedResources) -> None:
    """Send a message from Adam to Eve."""
    # Arrange

    message = {
        "author_id": resources.adam.id,
        "content": "Hello, Eve!"
    }

    # Act
    response = flask_client.post(
        f"/user/{resources.eve.id}/messages", json=message
    )

    # Assert
    print(response.json)
    assert response.status_code == HTTPStatus.CREATED
    assert response.text
