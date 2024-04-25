"""Confirm that the retrying_http_client module is working as expected."""

import http
import logging

import requests
import responses
from _pytest.logging import LogCaptureFixture
from flask_forge.extensions import retrying_http_client


@responses.activate
def test_requests_retries(caplog: LogCaptureFixture) -> None:
    """Confirm that the RetryingHttpClientRequests class is working as expected."""
    # ARRANGE
    caplog.set_level(logging.INFO)
    responses.get(
        url="https://not.a.real.url/", status=http.HTTPStatus.INTERNAL_SERVER_ERROR
    )
    responses.get(
        url="https://not.a.real.url/", status=http.HTTPStatus.SERVICE_UNAVAILABLE
    )
    responses.get(
        url="https://not.a.real.url/", json={"key": "value"}, status=http.HTTPStatus.OK
    )
    http_client = retrying_http_client.RetryingHttpClient()
    # ACT
    response = http_client.get("https://not.a.real.url/")
    # ASSERT
    assert response.status_code == http.HTTPStatus.OK
    assert "Initialized" in caplog.records[0].message


@responses.activate
def test_requests_with_no_retry() -> None:
    """Test plain requests with no retry to demonstrate the use of `responses`."""
    # ARRANGE
    responses.get(
        url="https://not.a.real.url/", status=http.HTTPStatus.INTERNAL_SERVER_ERROR
    )
    responses.get(
        url="https://not.a.real.url/", json={"key": "value"}, status=http.HTTPStatus.OK
    )
    # ACT
    response1 = requests.get("https://not.a.real.url/", timeout=0.1)
    response2 = requests.get("https://not.a.real.url/", timeout=0.1)
    # ASSERT
    assert response1.status_code == http.HTTPStatus.INTERNAL_SERVER_ERROR
    assert response2.status_code == http.HTTPStatus.OK
