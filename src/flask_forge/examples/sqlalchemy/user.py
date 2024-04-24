from email.utils import parseaddr
from json import loads
from uuid import uuid4

from flask.views import MethodView

from flask_forge.examples.sqlalchemy.models.user import UserModel

users = UserModel.query


class User(MethodView):
    MIN_USERNAME_LENGTH: int = 2
    MAX_USERNAME_LENGTH: int = 16
    MAX_EMAIL_LENGTH: int = 64
    ALLOWED_EMAIL_PROVIDER_DOMAINS: set[str] = {"gmail.com", "mail.ru", "outlook.com"}
    EMAIL_SPLIT_EXPECTED_LENGTH: int = 2

    def __init__(self, name: str | None, email: str | None):
        if not name:
            raise ValueError("Name cannot be empty")

        # Username checking logic
        if len(name) < self.MIN_USERNAME_LENGTH or len(name) > self.MAX_USERNAME_LENGTH:
            raise ValueError(
                f"Username must be between {self.MIN_USERNAME_LENGTH} and "
                f"{self.MAX_USERNAME_LENGTH} characters long"
            )

        if len(email) > self.MAX_EMAIL_LENGTH:
            raise ValueError(
                f"Email must be less than {self.MAX_EMAIL_LENGTH} characters long"
            )

        # Email checking logic.
        # parseaddr() return a tuple of (name, email), we only need the email part
        email: str = parseaddr(email)[1]
        email_split: list[str] = email.split("@")

        if (len(email_split) != self.EMAIL_SPLIT_EXPECTED_LENGTH
                or not email_split[0] or not email_split[1]):
            raise ValueError("Invalid email address")

        domain: str = email_split[1]

        if domain not in self.ALLOWED_EMAIL_PROVIDER_DOMAINS:
            raise ValueError(
                f"Email provider {domain} is not allowed. "
                f"Only {', '.join(self.ALLOWED_EMAIL_PROVIDER_DOMAINS)} are allowed."
            )

        self.uuid: str = uuid4().hex
        self.name: str = name
        self.email: str = email

    @classmethod
    def from_json(cls, json_str):
        json_dict = loads(json_str)
        return cls(**json_dict)

    def __hash__(self):
        return hash(self.uuid)
