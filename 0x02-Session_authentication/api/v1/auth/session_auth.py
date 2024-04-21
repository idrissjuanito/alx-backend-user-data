#!/usr/bin/env python3
""" Session Auth Module """
from uuid import uuid4
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ Session auth class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates a new session """
        if user_id is None or type(user_id) is not str:
            return None
        sess_id = str(uuid4())
        self.user_id_by_session_id[sess_id] = user_id
        return sess_id
