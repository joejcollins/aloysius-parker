from email.utils import parseaddr
from json import loads
from uuid import uuid4


class User:
    MIN_USERNAME_LENGTH: int = 2
    MAX_USERNAME_LENGTH: int = 16
    ALLOWED_EMAIL_PROVIDER_DOMAINS: set[str] = {"gmail.com", "mail.ru", "outlook.com"}

    def __init__(self, name: str, email: str):
        if not name:
            raise ValueError("Name cannot be empty")

        if not email:
            raise ValueError("Email cannot be empty")

        self.uuid: str = uuid4().hex

        # Username checking logic
        if len(name) < self.MIN_USERNAME_LENGTH or len(name) > self.MAX_USERNAME_LENGTH:
            raise ValueError(
                f"Username must be between {self.MIN_USERNAME_LENGTH} and "
                f"{self.MAX_USERNAME_LENGTH} characters long"
            )

        # Email checking logic.
        # parseaddr() return a tuple of (name, email), we only need the email part
        email = parseaddr(email)[1]
        domain = email.split("@")[1]
        if domain not in self.ALLOWED_EMAIL_PROVIDER_DOMAINS:
            raise ValueError(
                f"Email provider {domain} is not allowed. "
                f"Only {', '.join(self.ALLOWED_EMAIL_PROVIDER_DOMAINS)} are allowed."
            )

        self.name: str = name
        self.email: str = email

    @classmethod
    def from_json(cls, json_str):
        json_dict = loads(json_str)
        return cls(**json_dict)

    def __hash__(self):
        return hash(self.uuid)
