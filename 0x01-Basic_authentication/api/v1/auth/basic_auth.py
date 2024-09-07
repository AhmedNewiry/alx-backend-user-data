#!/usr/bin/env python3
"""Basic Authentication Module"""

from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


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
        except (TypeError, base64.binascii.Error):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts user email and password from the decoded Base64
        authorization header.
        """
        if (decoded_base64_authorization_header is None or
                not isinstance(decoded_base64_authorization_header, str)):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns a User instance based on email and password.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        users = User.search({'email': user_email})
        if not users:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieve the User instance for a request.
        """
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None
        base64_auth_header = self.extract_base64_authorization_header(
            auth_header)
        if not base64_auth_header:
            return None
        decoded_auth = self.decode_base64_authorization_header(
            base64_auth_header)
        if not decoded_auth:
            return None
        user_email, user_pwd = self.extract_user_credentials(decoded_auth)
        if not user_email or not user_pwd:
            return None
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
