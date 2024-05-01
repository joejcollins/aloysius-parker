"""Add a user to the database and confirm it was added.

By default, pytest will run the tests in alpha numeric order so each test should be
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
        self.uuid = None
        self.name = "example"
        self.email = "example@gmail.com"

    def payload(self):
        """Return an example payload for a user."""
        return {
            "name": self.name,
            "email": self.email,
        }


@pytest.fixture(name="resources", scope="module")
def shared_resources() -> SharedResources:
    """Return the shared resources object."""
    return SharedResources()


@pytest.fixture(scope="module", name="flask_client")
def create_flask_client() -> Generator:
    """Create a flask test client."""
    flask_api = main.create_app()
    with flask_api.test_client() as client:
        yield client


def is_user_same(user: dict[str, str], resources: SharedResources) -> bool:
    """Return True if the user and payload are the same."""
    return (
        user.get("name") == resources.name
        and user.get("email") == resources.email
        and (user.get("uuid") == resources.uuid or not resources.uuid)
    )


def test_001_get_empty_user_list(flask_client: testing.FlaskClient) -> None:
    """Test if GET request to /users with 0 users responds with 204 No content."""
    # Act
    response = flask_client.get("/users")

    # Assert response code is 204
    assert response.status_code == HTTPStatus.NO_CONTENT

    # Assert response is actually empty
    assert not response.text


def test_002_add_user(
    flask_client: testing.FlaskClient, resources: SharedResources
) -> None:
    """Test if we can successfully add a user to the database."""
    # Act
    response = flask_client.post("/users", json=resources.payload())

    # Assert status code is 201
    assert response.status_code == HTTPStatus.CREATED

    # Assert response data (JSON) is not empty
    assert response.json

    # Assert that response data matches our request
    assert is_user_same(response.json, resources)

    # Save UUID for later tests
    resources.uuid = response.json.get("uuid")


def test_003_get_user(
    flask_client: testing.FlaskClient, resources: SharedResources
) -> None:
    """Test if we can successfully retrieve the user from the database."""
    # Act
    response = flask_client.get(f"/user/{resources.uuid}")

    # Assert response code is 200 now that there's a user
    assert response.status_code == HTTPStatus.OK

    # Assert response is not empty
    assert response.json

    # Assert the user data matches the data we added
    assert is_user_same(response.json, resources)


def test_004_get_user_list(
    flask_client: testing.FlaskClient, resources: SharedResources
) -> None:
    """Test if the user is included in the global user list."""
    # Act
    response = flask_client.get("/users")

    # Assert response code is 200 now that there's a user
    assert response.status_code == HTTPStatus.OK

    # Assert response is not empty
    assert response.json

    # Assert the amount of users is 1
    assert len(response.json) == 1

    # Assert the user data matches the data we added
    first_user: dict[str] = response.json[0]
    assert is_user_same(first_user, resources)
