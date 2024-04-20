#!/usr/bin/env python3
""" Authentication module """
from flask import request
from typing import List, TypeVar


class Auth:
    """ authentication class """
    def __init__(self):
        """ class constructor function"""
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ enforces authorization on routes
        """
        if path is None or excluded_paths is None:
            return True
        path = path if path.endswith("/") else path + "/"
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Gets authorization header for request
        """
        if request is None:
            return None
        print(request.headers)
        auth_header = request.authorization
        if auth_header is None:
            return None
        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """ Gets current user making request
        """
        return None
