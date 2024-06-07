#!/usr/bin/env python3
"""
BasicAuth that inherits from Auth
"""

from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    BasicAuth that inherits from Auth
    """

    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """
    BasicAuth that inherits from Auth
    """

        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if len(authorization_header) < 6:
            return None
        if authorization_header[:6] != "Basic ":
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:

        """
        returns the decoded value of a Base64 strin
        base64_authorization_header
        """

        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            return base64.b64decode(
                    base64_authorization_header
                    ).decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> (str, str):
        """
        returns the user email and password from the
        Base64 decoded value.
        """

        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)

        user = decoded_base64_authorization_header.split(":")[0]
        ln = len(user) + 1
        passwd = decoded_base64_authorization_header[ln:]
        return (user, passwd)

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
            ) -> TypeVar('User'):
        """
        returns the User instance based on his email and password.
        """

        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        overloads Auth and retrieves the User instance for a request
        """

        auth_header = self.authorization_header(request)
        if auth_header:
            extract_header = self.extract_base64_authorization_header(
                    auth_header
                    )
            if extract_header:
                decode_base = self.decode_base64_authorization_header(
                        extract_header
                        )
                if decode_base:
                    user_details = self.extract_user_credentials(decode_base)
                    if user_details:
                        user_name = user_details[0]
                        user_pass = user_details[1]
                        user = self.user_object_from_credentials(
                                user_name,
                                user_pass
                                )
                        if user:
                            return user
        return None
