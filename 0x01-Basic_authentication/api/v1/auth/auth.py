#!/usr/bin/env python3
"""
class to manage the API authentication.
"""

from flask import request
from typing import List, TypeVar


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

        for i in excluded_paths:
            if i[-1] == "*":
                if i in path:
                    return False

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
