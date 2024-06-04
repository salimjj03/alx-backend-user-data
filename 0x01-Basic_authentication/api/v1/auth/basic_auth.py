#!/usr/bin/env python3
"""
BasicAuth that inherits from Auth
"""

from api.v1.auth.auth import Auth
import base64


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
