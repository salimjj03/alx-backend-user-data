#!/usr/bin/env python3
"""
inherits from SessionAuth in the
file api/v1/auth/session_exp_auth.py
"""

from api.v1.auth. session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    inherits from SessionAuth in the
    file api/v1/auth/session_exp_auth.py
    """

    def __init__(self):
        """
        the custructor method
        """

        atr = getenv("SESSION_DURATION")
        if atr is not None:
            try:
                self.session_duration = int(atr)
            except Exception:
                self.session_duration = 0
        else:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        return session_id
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
                "user_id": user_id,
                "created_at": datetime.now()
                }
        SessionAuth.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        return user_id from the session dictionary
        """

        if session_id is None:
            return None

        if session_id not in self.user_id_by_session_id.keys():
            return None
        dic = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return dic["user_id"]
        if "created_at" not in dic:
            return None
        create_time = dic["created_at"]
        time_delta = timedelta(seconds=self.session_duration)
        if (create_time + time_delta) < datetime.now():
            return None
        return dic["user_id"]
