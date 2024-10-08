#!/usr/bin/env python3
"""Authentication Management Module"""

from flask import request
from typing import List, TypeVar


User = TypeVar('User')


class Auth:
    """Auth clas"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determine if authentication is required for the given path.
        Always returns False in this template.
        """
        if path is None:
            return True
        if not excluded_paths:
            return True
        path = path if path.endswith('/') else path + '/'
        # Check if the normalized path is in the excluded_paths list
        for excluded_path in excluded_paths:
            # Handle wildcard (*) at the end of the excluded path
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path.rstrip('*')):
                    return False
            else:
                # Match the path exactly (with trailing slash stripped)
                if path == excluded_path.rstrip('/'):
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
