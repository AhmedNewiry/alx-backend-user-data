#!/usr/bin/env python3
"""
This module provides functionality for managing
authentication in a Flask application.
"""

from flask import request
from typing import List, TypeVar
import os

User = TypeVar('User')


class Auth:
    """
    A class for handling authentication-related operations.
    Methods:
    - require_auth(path: str, excluded_paths: List[str]) -> bool
    : Determines if authentication is required for the given path.
    - authorization_header(request=None) -> str: Retrieves the
    authorization header from the request.
    - current_user(request=None) -> User: Retrieves the current
    user from the request.
    - session_cookie(request=None) -> str: Retrieves
    the session cookie value from the request.
    """
    
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determine if authentication is required for the given path.
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
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> User:
        """
        Get the current user from the request.
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns the value of the session cookie from a request.
        """
        if request is None:
            return None

        session_name = os.getenv('SESSION_NAME')
        if session_name is None:
            return None
        return request.cookies.get(session_name)
