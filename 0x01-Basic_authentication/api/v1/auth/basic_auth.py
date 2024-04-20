#!/usr/bin/env python3
""" Basic Auth module """
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic authentication class """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        ah = authorization_header
        if ah is None or type(ah) is not str:
            return None
        if not ah.startswith("Basic"):
            return None
        return ah.split()[1]
