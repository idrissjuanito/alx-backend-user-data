#!/usr/bin/env python3
from uuid import uuid4
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from typing import TypeVar


def _hash_password(password: str) -> bytes:
    """ hashes a password using bcrypt module """
    h_pwd = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return h_pwd


def _generate_uuid() -> str:
    """ generates new uuid and cast value to str """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def create_session(self, email: str) -> str:
        """ Creates a new session id for user """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            return session_id
        except NoResultFound:
            return None

    def register_user(self, email: str, password: str) -> TypeVar("User"):
        """ registers a new user to the db """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            h_pwd = _hash_password(password).decode("utf-8")
            return self._db.add_user(email=email, hashed_password=h_pwd)

    def valid_login(self, email: str, password: str) -> bool:
        """ validates a users login credentials """
        try:
            user = self._db.find_user_by(email=email)
            h_pwd = user.hashed_password.encode("utf-8")
            return bcrypt.checkpw(password.encode("utf-8"), h_pwd)
        except NoResultFound:
            return False

    def get_user_from_session_id(self, session_id: str) -> TypeVar("User"):
        """ gets a user given it's session id """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        """ finds a user and sets it's session id none """
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """ generates a reset token for a user """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password) -> None:
        """ updates a user's password """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            h_pwd = _hash_password(password).decode("utf-8")
            self._db.update_user(
                    user.id,
                    hashed_password=h_pwd,
                    reset_token=None)
            return None
        except NoResultFound:
            raise ValueError
