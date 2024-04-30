"""Error handling and customisation."""
import http.client

from flask import jsonify


def handle_error(error):
    """Handle errors and return a JSON response with the error message."""
    code = error.code if hasattr(error, "code") else 500

    # Yes 422 is more specific than 403, but most people do not know what 422 means
    if error.code == http.client.UNPROCESSABLE_ENTITY:
        code = http.client.FORBIDDEN
    elif isinstance(error, TypeError):
        code = http.client.FORBIDDEN

    return (
        jsonify(
            {
                "error": str(error),
                "type": error.__class__.__name__,
            }
        ),
        code,
    )
