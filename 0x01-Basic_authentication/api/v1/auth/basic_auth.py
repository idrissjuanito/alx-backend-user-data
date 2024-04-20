#!/usr/bin/env python3
""" Basic Auth module """
from api.v1.auth.auth import Auth
import base64


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
