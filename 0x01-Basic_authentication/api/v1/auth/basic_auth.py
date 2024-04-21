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
            return dcoded
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
        return tuple(d_ah.split(":"))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ returns the user object corresponding to email and password """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        User.load_from_file()
        users = User.search({"email": user_email, "password": user_pwd})
        print(users)
        if len(users) == 0:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            print(user)
            return None
        return user
