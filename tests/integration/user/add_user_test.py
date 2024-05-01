"""Add a user to the database and confirm it was added.

By default, pytest will run the tests in alpha numeric order so each test should be
named test_001, test_002, test_003, etc.
"""

from http import HTTPStatus
from typing import Generator

import pytest
from flask import testing
from flask_forge import main


# region Fixtures and helper functions
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


# endregion


def test_001_get_empty_user_list(flask_client: testing.FlaskClient) -> None:
    """Test if GET request to /users with 0 users responds with 204 No content."""
    # Act
    response = flask_client.get("/users")
    # Assert
    # There should be no content because there are no users.
    assert response.status_code == HTTPStatus.NO_CONTENT
    # as a result, the response should be empty
    assert not response.text


def test_002_add_a_new_user(
    flask_client: testing.FlaskClient, resources: SharedResources
) -> None:
    """Test if we can successfully add a user to the database."""
    # Act
    response = flask_client.post("/users", json=resources.payload())
    # Assert
    # The status should confirm the user was added.
    assert response.status_code == HTTPStatus.CREATED
    # and the returned user should be the same as the one sent.
    assert is_user_same(response.json, resources)
    # Store UUID for later tests
    resources.uuid = response.json.get("uuid")


def test_003_get_the_new_user_back_again(
    flask_client: testing.FlaskClient, resources: SharedResources
) -> None:
    """Test if we can successfully retrieve the user from the database."""
    # Act
    response = flask_client.get(f"/user/{resources.uuid}")
    # Assert
    # Confirm the user was found.
    assert response.status_code == HTTPStatus.OK
    # and the user is the same as the one we added.
    assert is_user_same(response.json, resources)


def test_004_check_that_there_is_only_one_user(
    flask_client: testing.FlaskClient, resources: SharedResources
) -> None:
    """Test if the user is included in the global user list."""
    # Act
    response = flask_client.get("/users")
    # Assert
    # Confirm that the end point responses.
    assert response.status_code == HTTPStatus.OK
    # and that there is only one user in the list.
    assert len(response.json) == 1
    # Confirm that the user data matches the data we added.
    first_user: dict[str, str] = response.json[0]
    assert is_user_same(first_user, resources)
