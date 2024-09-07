#!/usr/bin/env python3
"""Authentication Management Module DonDocDoc DocDocDoc"""

from flask import request
from typing import List, TypeVar
import os

User = TypeVar('User')


class Auth:
    """a class for authentication mangement"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determine if authentication is required for the given path.
        Always returns False in this template.
        """
        if path is None:
            return True
        if not excluded_paths:
            return True
        normalized_path = path if path.endswith('/') else path + '/'
        # Check if the normalized path is in the excluded_paths list
        for excluded_path in excluded_paths:
            if normalized_path.startswith(excluded_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Get the authorization header from the request.
        Always returns None in this template.
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> User:
        """
        Get the current user from the request.
        Always returns None in this template.
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns the value of the session cookie from a request.

        Args:
            request: The incoming HTTP request object.

        Returns:
            The value of the cookie named by the environment variable
            SESSION_NAME or None if not present.
        """
        if request is None:
            return None

        session_name = os.getenv('SESSION_NAME')
        if session_name is None:
            return None

        return request.cookies.get(session_name)
