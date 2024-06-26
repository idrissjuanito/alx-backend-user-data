#!/usr/bin/env python3
""" Basic Auth module """
from api.v1.auth.auth import Auth
from typing import TypeVar
import base64
from models.user import User


class BasicAuth(Auth):
    """ Basic authentication class """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ extracts basic authorization header """
        ah = authorization_header
        if ah is None or type(ah) is not str:
            return None
        if not ah.startswith("Basic"):
            return None
        return ah.split()[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Validates and decodes base64 authorization header """
        ah = base64_authorization_header  # shorter var name
        if ah is None or type(ah) is not str:
            return None
        try:
            dcoded = base64.b64decode(ah)
            return dcoded.decode("utf8")
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ extract credentials fron decoded base64 header """
        d_ah = decoded_base64_authorization_header
        if d_ah is None or type(d_ah) is not str:
            return None, None
        if ":" not in d_ah:
            return None, None
        credentials = tuple(d_ah.split(":"))
        return credentials[0], ":".join(credentials[1:])

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ returns the user object corresponding to email and password """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        users = User.search({"email": user_email})
        if len(users) == 0:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """ gets the current user """
        auth_header = self.authorization_header(request)
        b64_header = self.extract_base64_authorization_header(auth_header)
        dcoded = self.decode_base64_authorization_header(b64_header)
        user_cred = self.extract_user_credentials(dcoded)
        return self.user_object_from_credentials(user_cred[0], user_cred[1])
