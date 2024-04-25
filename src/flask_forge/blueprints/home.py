"""The home/landing endpoint providing some convenience methods about the endpoints."""

from datetime import datetime

import flask

START_TIME: datetime = datetime.now()
BLUEPRINT = flask.Blueprint("home", __name__)


@BLUEPRINT.route("/")
def home() -> flask.Response:
    """Return a JSON response with the name of the app, endpoints, and the uptime."""
    the_app = flask.current_app
    endpoints = [rule.rule for rule in the_app.url_map.iter_rules()]
    return flask.jsonify(
        name=__name__, endpoints=endpoints, uptime=str(datetime.now() - START_TIME)
    )
