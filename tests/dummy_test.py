"""Test the dummy."""

from flask_forge import dummy


def test_dummy() -> None:
    """Confirm return."""
    # ACT
    result = dummy.dummy()
    # ASSERT
    assert result == "dummy"


def test_dummy2() -> None:
    """Confirm return."""
    # ASSERT
    assert "dummy" == "dummy2"
