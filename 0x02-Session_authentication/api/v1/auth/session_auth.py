#!/usr/bin/env python3
""" Session Auth Module """
from uuid import uuid4
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ Session auth class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates a new session with session id as key """
        if user_id is None or type(user_id) is not str:
            return None
        sess_id = str(uuid4())
        self.user_id_by_session_id[sess_id] = user_id
        return sess_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ gets a user id from session id """
        if session_id is None or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)
