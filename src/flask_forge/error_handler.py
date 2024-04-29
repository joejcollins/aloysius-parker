"""Error handling and customisation."""
from flask import jsonify


def handle_error(error):
    """Handle errors and return a JSON response with the error message."""
    code = error.code if hasattr(error, "code") else 500

    if isinstance(error, TypeError):
        code = 400

    return (
        jsonify(
            {
                "code": code,
                "error": str(error),
                "type": error.__class__.__name__,
            }
        ),
        code,
    )
