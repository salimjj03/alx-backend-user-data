#!/usr/bin/env python3
"""
takes in a password string arguments and returns bytes.
"""

import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import User


def _hash_password(password: str) -> bytes:
    """
    takes in a password string arguments and returns bytes.
    """

    password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        should take mandatory email and password string
        arguments and return a User object.
        """

        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists.".format(email))
        except NoResultFound:
            password = _hash_password(password)
            user = self._db.add_user(email, password)
            return user
