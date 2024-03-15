"""Test the dummy."""

from src import dummy


def test_dummy() -> None:
    """Confirm return."""
    # ACT
    result = dummy.dummy()
    # ASSERT
    assert result == "dummy"
