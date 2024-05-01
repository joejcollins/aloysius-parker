"""Run up the flask api and confirm that it does not break by checking a URL."""

from http import HTTPStatus
from typing import Generator

import pytest
from flask_forge.extensions import retrying_http_client

from tests.e2e import subprocess


@pytest.fixture(autouse=True)
def start_flask_server() -> Generator:
    """Start the server just like you would on the command line.

    This is really a kind of smoke test since it confirms that the API will run.  The
    pytest_flask fixtures does include live_server which starts a separate server
    process.
    """
    yield from subprocess.run_subprocess(
        [
            ".venv/bin/python",
            "src/flask_forge/main.py",
        ]
    )


def test_server_is_up_and_running() -> None:
    """Confirm that the server runs and you can access the documents."""
    http_client = retrying_http_client.RetryingHttpClient()
    response = http_client.get("http://127.0.0.1:5000")
    assert response.status_code == HTTPStatus.OK
