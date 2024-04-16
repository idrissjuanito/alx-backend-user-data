#!/usr/bin/env python3
"""Authentication module """
from flask import request


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ enforces authorization on routes
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Gets authorization header for request
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Gets current user making request
        """
        return None
