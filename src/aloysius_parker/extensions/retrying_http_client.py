"""Retrying HTTP client to deal with intermittent connections etc..."""

import logging
from http import HTTPStatus
from typing import Any, Callable

import requests
from requests import adapters
from urllib3.util import Retry

LOG = logging.getLogger(__name__)
LOG.propagate = True


def retry_increment_log(original_increment_func: Callable) -> Any:
    """Log the function call to the Retry.increment method to monitor failures.

    There is some logging built into the Retry.increment method but is it only for
    debugging purposes.  Wrapping the method like this gives us the opportunity to
    customize the message and logging level.
    """

    def wrapper(*args, **kwargs) -> Any:
        """Wrap the Retry.increment method."""
        previous_response = "Not known"
        if "error" in kwargs:  # we probably didn't make it to the server.
            previous_response = kwargs["error"].args[0]
        if "response" in kwargs:  # the server responded but not positively.
            previous_response = kwargs["response"].reason
        LOG.info("Retrying because %s", previous_response)
        # Call the original function
        result = original_increment_func(*args, **kwargs)
        # Log the result
        LOG.info("%s retries left", result.total)
        return result

    return wrapper


# Replace the Retry.increment method with the wrapped version.
Retry.increment = retry_increment_log(Retry.increment)  # type: ignore


class RetryingHttpClient:
    """Retrying HTTP client.

    We are using the requests library rather than urllib3 directly because we can test
    it with the responses library which is specifically designed for testing requests.
    Other than this there is no difference between this and the urllib3 version.
    """

    def __init__(self, max_retries: int = 3, backoff_factor: int = 1) -> None:
        """Initialise the HTTP client with the number of retries and backoff factor."""
        self.session = requests.Session()
        # List the HTTP status codes that we want to retry.
        self.status_forcelist = [
            HTTPStatus.REQUEST_TIMEOUT,
            HTTPStatus.TOO_EARLY,
            HTTPStatus.TOO_MANY_REQUESTS,
            HTTPStatus.INTERNAL_SERVER_ERROR,
            HTTPStatus.BAD_GATEWAY,
            HTTPStatus.SERVICE_UNAVAILABLE,
            HTTPStatus.GATEWAY_TIMEOUT,
        ]
        self.retries = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=self.status_forcelist,
        )
        self.adapter = adapters.HTTPAdapter(max_retries=self.retries)
        self.session.mount("http://", self.adapter)
        self.session.mount("https://", self.adapter)
        LOG.info("Initialized RetryingHttpClient with max_retries=%s", max_retries)

    def get(self, url: str, **kwargs) -> requests.Response:
        """Send a GET request to the specified URL."""
        return self.session.get(url, **kwargs)
