"""Run up the flask api and confirm that it does not break by checking a URL."""
from http import HTTPStatus
from typing import Generator

import pytest
from flask_forge.extensions import retrying_http_client

from tests.integration import subprocess


@pytest.fixture(autouse=True)
def start_flask_server() -> Generator:
    """Start the server just like you would on the command line.

    This is really a kind of smoke test since it confirms that the API will run.  The
    pytest_flask fixtures does include live_server which starts a separate server
    process.
    """
    yield from integration.run_subprocess(
        [
            ".venv/bin/flask",
            "--app",
            "flask_api_v1_v2.main:FLASK_API",
            "run",
            "--host=0.0.0.0",
            "--port=5000",
        ]
    )


def test_server_is_up_and_running() -> None:
    """Confirm that the server runs and you can access the documents."""
    http_client = retrying_http_client.RetryingHttpClient()
    response = http_client.get(f"{TESTS.flask_api_url}/ui-swagger/")
    assert response.status_code == HTTPStatus.OK
