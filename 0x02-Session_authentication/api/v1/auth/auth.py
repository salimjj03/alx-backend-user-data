#!/usr/bin/env python3
"""
class to manage the API authentication.
"""

from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """
    class to manage the API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        that returns False - path and excluded_paths
        will be used later, now, you don’t need to take
        care of them
        """

        if path is not None:
            last = path[-1]
            if last != "/":
                path += "/"

        if path is None or excluded_paths is None:
            return True

        if path not in excluded_paths:

            return True
        return False

    def authorization_header(self, request=None) -> str:
        """
        that returns None - request will be the Flask request object
        """

        if request is None:
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """
        that returns None - request will be the Flask request object
        """

        return None

    def session_cookie(self, request=None):
        """
        returns a cookie value from a request.
        """

        if request is None:
            return None

        cookie = getenv("SESSION_NAME")
        return request.cookies.get(cookie)
