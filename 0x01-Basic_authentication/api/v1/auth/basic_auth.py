#!/usr/bin/env python3
"""Basic Authentication Module"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Basic Authentication class, inherits from Auth"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extract the Base64 part from the Authorization header.
        Args:
            authorization_header (str): The Authorization header.
        Returns:
            str: The Base64 part of the Authorization header, or None
            if the input is invalid.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]
