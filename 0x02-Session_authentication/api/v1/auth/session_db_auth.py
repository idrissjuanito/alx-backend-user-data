#!/usr/bin/env python3
""" Session DB Module """
from datetime import timedelta, datetime
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Session db auth class """

    def create_session(self, user_id=None):
        """ Creates new user session """
        sess_id = super().create_session(user_id)
        if sess_id is None:
            return None
        user = UserSession(user_id=user_id, session_id=sess_id)
        user.save()
        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """ gets user from database and returns  """
        session_list = UserSession.search({'session_id': session_id})
        if len(session_list) == 0:
            return None
        user_session = session_list[0]
        if self.session_duration <= 0:
            return user_session.user_id
        if not hasattr(user_session, 'created_at'):
            return None
        duration_delta = timedelta(seconds=self.session_duration)
        session_exp = getattr(user_session, 'created_at') + duration_delta
        if datetime.now() > session_exp:
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """ Destroys a session in the database """
        user = self.current_user(request)
        if user is None:
            return False
        user.remove()
        return True
