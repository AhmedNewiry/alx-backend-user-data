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


    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decode the Base64 authorization header.
        Args:
            base64_authorization_header (str): The Base64 string.
        Returns:
            str: The decoded value as UTF-8 string, or None if the input
            is invalid or decoding fails.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (binascii.Error, ValueError):
            return None
