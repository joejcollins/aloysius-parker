"""Test the user repository."""

from flask_forge.database import user_repository


def test_get_user():
    """Test if we can successfully retrieve the user from the database."""
    # Arrange
    the_repository = user_repository.UserRepository()
    user = user_repository.get_user("1")
    # Act
    user = user_repository.get_user("1")
    # Assert
