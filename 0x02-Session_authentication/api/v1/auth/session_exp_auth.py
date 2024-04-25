#!/usr/bin/env python3
""" Session Auth Exporation Module """
from datetime import datetime, time, timedelta
from api.v1.auth.session_auth import SessionAuth
from os import getenv


class SessionExpAuth(SessionAuth):
    """ Session Exp class """

    def __init__(self):
        self.session_duration = int(getenv('SESSION_DURATION')) or 0

    def create_session(self, user_id=None):
        """ Create new session with expiration """
        sess_id = super().create_session(user_id)
        if sess_id is None:
            return None
        self.user_id_by_session_id[sess_id] = {
                'user_id': user_id,
                'created_at': datetime.now()
            }
        return sess_id

    def user_id_for_session_id(self, session_id: None):
        """ returns user's session info """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id.keys():
            return None
        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        if 'created_at' not in session_dict.keys():
            return None
        sess_dur_delta = timedelta(seconds=self.session_duration)
        sess_exp = session_dict['created_at'] + sess_dur_delta
        if datetime.now() > sess_exp:
            return None
        return session_dict['user_id']
