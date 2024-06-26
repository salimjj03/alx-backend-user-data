#!/usr/bin/env python3
"""
takes in a password string arguments and returns bytes.
"""

import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """
    takes in a password string arguments and returns bytes.
    """

    password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    return hashed_password


def _generate_uuid() -> str:
    """
    return a string representation of a new UUID
    """

    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """
        It should expect email and password required argument
        and return a boolean.

        locating the user by email. If it exists, check the
        password with bcrypt.checkpw. If it matches return
        True. In any other case, return False
        """

        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode("utf-8"), user.hashed_password):
                return True
            else:
                return False
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """
        takes an email string argument and returns
        the session ID as a string.

        find the user corresponding to the email, generate a new
        UUID and store it in the database as the user’s session_id,
        then return the session ID.
        """

        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        t takes a single session_id string argument and returns
        the corresponding User or None.

        If the session ID is None or no user is found, return
        None. Otherwise return the corresponding user.
        """

        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        takes a single user_id integer argument and returns None.

        The method updates the corresponding user’s session ID
        to None
        """

        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        take an email string argument and returns a string.

        Find the user corresponding to the email. If the
        user does not exist, raise a ValueError exception.
        If it exists, generate a UUID and update the user’s
        reset_token database field. Return the token.
        """

        u_id = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, reset_token=u_id)
            return u_id
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        takes reset_token string argument and a password string
        argument and returns None.

        Use the reset_token to find the corresponding user.
        If it does not exist, raise a ValueError exception.

        Otherwise, hash the password and update the user’s
        hashed_password field with the new hashed password
        and the reset_token field to None.
        """

        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hash_pass = _hash_password(password)
            self._db.update_user(
                    user.id,
                    hashed_password=hash_pass,
                    reset_token=None
                    )
            return None
        except Exception:
            raise ValueError
