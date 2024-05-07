"""Test message sending functionality."""
from datetime import datetime
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
        self.content: str = "Ate a weird fruit, now I'm feeling a little... ex-posed."


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

        # Update the resources with the created user
        if account["name"] == "Adam":
            resources.adam = User.from_json(response.text)
        elif account["name"] == "Eve":
            resources.eve = User.from_json(response.text)


def test_002_send_message(flask_client: testing.FlaskClient,
                          resources: SharedResources) -> None:
    """Send a message from Adam to Eve."""
    # Arrange

    message: dict[str, str] = {
        "author_id": resources.adam.id,
        "content": resources.content,
    }

    # Act
    response = flask_client.post(
        f"/user/{resources.eve.id}/messages", json=message
    )

    # Assert the message was created and that the content is in the response
    assert response.status_code == HTTPStatus.CREATED
    assert resources.content in response.text

    # Assert the timestamp of the message is not far off current time
    date_without_time = datetime.now().isoformat()[:10]
    assert "timestamp" in response.json
    assert date_without_time in response.json["timestamp"]


def test_003_fetch_messages(flask_client: testing.FlaskClient,
                            resources: SharedResources) -> None:
    """Fetch messages for Eve."""
    # Act
    response = flask_client.get(f"/user/{resources.eve.id}/messages")

    # Assert that there's only 1 message
    assert len(response.json) == 1

    # Assert that it's from Adam
    print(response.json)
    assert response.json[0]["author_id"] == resources.adam.id

    # Assert that the content is the same
    assert resources.content == response.json[0]["content"]
