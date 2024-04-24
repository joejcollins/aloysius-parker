from sqlalchemy import Column, String

from flask_forge.examples.sqlalchemy.db import database


class UserModel(database.Model):
    __tablename__ = "users"

    uuid: str = Column(String, primary_key=True)
    name: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False)
