"""Test the dummy."""

from flask import app
from flask_forge import main


def test_dummy() -> None:
    """Confirm return."""
    # ACT
    the_app = main.create_app()
    # ASSERT
    assert isinstance(the_app, app.Flask)
