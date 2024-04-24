"""An example Flask API server that uses SQLAlchemy to manage a user database.

The following endpoints are supported:
-   GET /users
-   POST /users
-   GET /users/<uuid>
-   DELETE /users/<uuid>.

SQLAlchemy uses an SQLite database to store user information.
This is currently stored in memory
"""
