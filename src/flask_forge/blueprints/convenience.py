"""Convenience functions to test the flask application."""

import flask_smorest
from flask import views

from flask_forge.handler import convenience

SMOREST_CONVENIENCE_BLUEPRINT = flask_smorest.Blueprint(
    "convenience", __name__, description="Quality of life convenience functionality"
)


@SMOREST_CONVENIENCE_BLUEPRINT.route("/convenience")
class ConvenienceEndpoint(views.MethodView):
    """Define the endpoint for /convenience.

    This endpoint is used to automatically perform repetitive tasks for testing.
    Examples include creating a new user.
    """

    @SMOREST_CONVENIENCE_BLUEPRINT.response(200)
    def post(self):
        """Automatically create a dummy user via a POST request."""
        return convenience.create_example_user()
